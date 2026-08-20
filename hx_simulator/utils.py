"""Utility functions — dimensionless numbers, LMTD, ε-NTU, convergence, validation.

ε-NTU formulas from:
  - Incropera & DeWitt, "Fundamentals of Heat and Mass Transfer", 7th Ed., Wiley, 2011, Ch. 11
  - Kays & London, "Compact Heat Exchangers", 2nd Ed., McGraw-Hill, 1964
  - Kern, "Process Heat Transfer", McGraw-Hill, 1950
  - Bowman, Mueller & Nagle, "Mean Temperature Difference in Design", Trans. ASME, 1940
"""

import math
import warnings


# ---------------------------------------------------------------------------
# Dimensionless Numbers  (ref: 00_formula_cheatsheet.md, 06/05 modules)
# ---------------------------------------------------------------------------

def Re_D(rho: float, v: float, D: float, mu: float) -> float:
    """Reynolds number for internal flow: Re = rho * v * D / mu.

    Parameters
    ----------
    rho : float   Fluid density [kg/m^3]
    v   : float   Mean velocity [m/s]
    D   : float   Hydraulic diameter [m]
    mu  : float   Dynamic viscosity [Pa.s]
    """
    return rho * v * D / mu


def Re_D_from_mdot(m_dot: float, D: float, mu: float) -> float:
    """Reynolds number from mass flow rate: Re = 4*mdot / (pi*D*mu)."""
    return 4.0 * m_dot / (math.pi * D * mu)


def Nu_D(h: float, D: float, k: float) -> float:
    """Nusselt number: Nu = h * D / k."""
    return h * D / k


def h_from_Nu(Nu: float, k: float, D: float) -> float:
    """Convective coefficient from Nusselt: h = Nu * k / D."""
    return Nu * k / D


def Pr(mu: float, Cp: float, k: float) -> float:
    """Prandtl number: Pr = mu * Cp / k."""
    return mu * Cp / k


def Gr_L(g: float, beta: float, dT: float, L: float, nu: float) -> float:
    """Grashof number: Gr = g * beta * dT * L^3 / nu^2."""
    return g * beta * dT * L**3 / nu**2


def Ra_L(Gr: float, Pr_val: float) -> float:
    """Rayleigh number: Ra = Gr * Pr."""
    return Gr * Pr_val


def St(h: float, rho: float, v: float, Cp: float) -> float:
    """Stanton number: St = h / (rho * v * Cp)."""
    return h / (rho * v * Cp)


# ---------------------------------------------------------------------------
# Log Mean Temperature Difference  (ref: 08_heat_exchangers.md §2, §4b)
# ---------------------------------------------------------------------------

def LMTD(dT1: float, dT2: float) -> float:
    """Log-mean temperature difference.

    For parallel flow: dT1 = T_h,i - T_c,i,  dT2 = T_h,o - T_c,o
    For counter flow:  dT1 = T_h,i - T_c,o,  dT2 = T_h,o - T_c,i

    When dT1 == dT2 (within tolerance), returns dT1 directly to avoid
    the 0/0 singularity.
    """
    if abs(dT1 - dT2) < 1e-10:
        return dT1
    if dT1 <= 0 or dT2 <= 0:
        raise ValueError(
            f"LMTD requires positive temperature differences, got dT1={dT1}, dT2={dT2}"
        )
    return (dT1 - dT2) / math.log(dT1 / dT2)


# ---------------------------------------------------------------------------
# Effectiveness-NTU relations  (ref: 08_heat_exchangers.md §6)
# ---------------------------------------------------------------------------

def epsilon_NTU_counterflow(NTU: float, Cr: float) -> float:
    """Effectiveness for counter-flow HX.

    ε = [1 - exp(-NTU(1-Cr))] / [1 - Cr*exp(-NTU(1-Cr))]
    """
    if Cr == 1.0:
        return NTU / (1.0 + NTU)
    exp_term = math.exp(-NTU * (1.0 - Cr))
    return (1.0 - exp_term) / (1.0 - Cr * exp_term)


def epsilon_NTU_parallel(NTU: float, Cr: float) -> float:
    """Effectiveness for parallel-flow HX.

    ε = [1 - exp(-NTU(1+Cr))] / (1+Cr)
    """
    return (1.0 - math.exp(-NTU * (1.0 + Cr))) / (1.0 + Cr)


def epsilon_NTU_phase_change(NTU: float) -> float:
    """Effectiveness when one fluid undergoes phase change (Cr = 0).

    ε = 1 - exp(-NTU)
    """
    return 1.0 - math.exp(-NTU)


def NTU_from_epsilon_counterflow(epsilon: float, Cr: float) -> float:
    """Invert counter-flow ε-NTU to find required NTU.

    From ε = [1 - exp(-NTU(1-Cr))] / [1 - Cr*exp(-NTU(1-Cr))]:
      exp(-NTU(1-Cr)) = (1-ε)/(1-ε*Cr)
      NTU = -ln[(1-ε)/(1-ε*Cr)] / (1-Cr)   for Cr != 1
      NTU = ε/(1-ε)                          for Cr == 1
    """
    if epsilon <= 0 or epsilon >= 1:
        raise ValueError(f"epsilon must be in (0, 1), got {epsilon}")
    if Cr == 1.0:
        return epsilon / (1.0 - epsilon)
    arg = (1.0 - epsilon) / (1.0 - epsilon * Cr)
    if arg <= 0:
        raise ValueError("Cannot invert: log argument is non-positive.")
    return -math.log(arg) / (1.0 - Cr)


def NTU_from_epsilon_parallel(epsilon: float, Cr: float) -> float:
    """Invert parallel-flow ε-NTU to find required NTU.

    NTU = -ln[1 - ε(1+Cr)] / (1+Cr)
    """
    if epsilon <= 0 or epsilon >= 1:
        raise ValueError(f"epsilon must be in (0, 1), got {epsilon}")
    arg = 1.0 - epsilon * (1.0 + Cr)
    if arg <= 0:
        raise ValueError("Cannot invert: argument of log is non-positive.")
    return -math.log(arg) / (1.0 + Cr)


# ---------------------------------------------------------------------------
# Shell-and-tube ε-NTU  (ref: Incropera & DeWitt, Ch. 11, Table 11.3)
# For 1 shell pass, 2/4/6/... tube passes (TEMA E with multi-pass tubes)
# ---------------------------------------------------------------------------

def epsilon_NTU_shell_tube(NTU: float, Cr: float) -> float:
    """Effectiveness for shell-and-tube HX (1 shell pass, 2+ tube passes).

    ε = 2 * {1 + Cr + sqrt(1+Cr^2) * [1 + exp(-NTU*sqrt(1+Cr^2))] /
              [1 - exp(-NTU*sqrt(1+Cr^2))]}^(-1)

    Ref: Incropera & DeWitt, 7th Ed., Table 11.3, Row 5.
    Valid for Cr < 1. When Cr = 1, uses limiting form.
    """
    if Cr == 1.0:
        # Limiting case for Cr → 1
        E = math.exp(-NTU * math.sqrt(2.0))
        return 2.0 / (1.0 + Cr + math.sqrt(1.0 + Cr**2) * (1.0 + E) / (1.0 - E))
    sqrt_term = math.sqrt(1.0 + Cr**2)
    exp_term = math.exp(-NTU * sqrt_term)
    denom = 1.0 + Cr + sqrt_term * (1.0 + exp_term) / (1.0 - exp_term)
    return 2.0 / denom


def NTU_from_epsilon_shell_tube(epsilon: float, Cr: float) -> float:
    """Invert shell-and-tube ε-NTU to find required NTU.

    From ε = 2 / {1 + Cr + sqrt(1+Cr^2) * [1+exp(-NTU*sqrt(1+Cr^2))] /
              [1 - exp(-NTU*sqrt(1+Cr^2))]}:

    Let S = sqrt(1+Cr^2), then:
      F = 2/ε - 1 - Cr
      exp(-NTU*S) = (F - S) / (F + S)
      NTU = -ln[(F-S)/(F+S)] / S

    Ref: Incropera & DeWitt, 7th Ed., Table 11.3.
    """
    if epsilon <= 0 or epsilon >= 1:
        raise ValueError(f"epsilon must be in (0, 1), got {epsilon}")
    S = math.sqrt(1.0 + Cr**2)
    F = 2.0 / epsilon - 1.0 - Cr
    if F <= S:
        raise ValueError("Cannot invert shell-and-tube: F <= S, epsilon too high.")
    ratio = (F - S) / (F + S)
    if ratio <= 0:
        raise ValueError("Cannot invert shell-and-tube: log argument non-positive.")
    return -math.log(ratio) / S


# ---------------------------------------------------------------------------
# Cross-flow ε-NTU  (ref: Incropera & DeWitt, Ch. 11, Table 11.3)
# ---------------------------------------------------------------------------

def epsilon_NTU_crossflow_both_unmixed(NTU: float, Cr: float) -> float:
    """Effectiveness for cross-flow HX with BOTH fluids unmixed.

    ε = 1 - exp[(1/Cr) * NTU^0.22 * {exp(-Cr * NTU^0.78) - 1}]

    This is an approximate correlation. Exact: series solution.
    Ref: Incropera & DeWitt, 7th Ed., Table 11.3, Row 3.
    """
    if Cr == 0.0:
        return 1.0 - math.exp(-NTU)
    exp_inner = math.exp(-Cr * NTU**0.78)
    return 1.0 - math.exp((1.0 / Cr) * NTU**0.22 * (exp_inner - 1.0))


def epsilon_NTU_crossflow_one_mixed(NTU: float, Cr: float,
                                    mixed_side: str = "cold") -> float:
    """Effectiveness for cross-flow HX with ONE fluid mixed, one unmixed.

    If the mixed side is the cold fluid (C_c mixed, C_h unmixed):
      ε = (1 - exp(-Cr*(1 - exp(-NTU)))) / Cr     (Cr != 0)

    If the mixed side is the hot fluid (C_h mixed, C_c unmixed):
      ε = 1 - exp(-(1 - exp(-Cr*NTU)) / Cr)       (Cr != 0)

    When Cr = 0 (phase change): ε = 1 - exp(-NTU)

    Ref: Incropera & DeWitt, 7th Ed., Table 11.3, Rows 1 & 2.
          Kays & London, "Compact Heat Exchangers", 1964.
    """
    if Cr == 0.0:
        return 1.0 - math.exp(-NTU)
    if mixed_side == "cold":
        # C_c mixed, C_h unmixed
        return (1.0 - math.exp(-Cr * (1.0 - math.exp(-NTU)))) / Cr
    else:
        # C_h mixed, C_c unmixed
        return 1.0 - math.exp(-(1.0 - math.exp(-Cr * NTU)) / Cr)


def NTU_from_epsilon_crossflow_one_mixed(epsilon: float, Cr: float,
                                          mixed_side: str = "cold") -> float:
    """Invert cross-flow (one mixed) ε-NTU to find required NTU.

    For C_c mixed, C_h unmixed:
      ε = (1 - exp(-Cr*(1-exp(-NTU)))) / Cr
      => 1 - ε*Cr = exp(-Cr*(1-exp(-NTU)))
      => ln(1-ε*Cr)/(-Cr) = 1 - exp(-NTU)
      => exp(-NTU) = 1 + ln(1-ε*Cr)/Cr
      => NTU = -ln[1 + ln(1-ε*Cr)/Cr]

    For C_h mixed, C_c unmixed:
      ε = 1 - exp(-(1-exp(-Cr*NTU))/Cr)
      => ln(1-ε) = -(1-exp(-Cr*NTU))/Cr
      => exp(-Cr*NTU) = 1 + Cr*ln(1-ε)
      => NTU = -ln[1 + Cr*ln(1-ε)] / Cr

    Ref: Incropera & DeWitt, 7th Ed., Table 11.3.
    """
    if epsilon <= 0 or epsilon >= 1:
        raise ValueError(f"epsilon must be in (0, 1), got {epsilon}")
    if mixed_side == "cold":
        inner = 1.0 + math.log(1.0 - epsilon * Cr) / Cr
        if inner <= 0:
            raise ValueError("Cannot invert: argument of log is non-positive.")
        return -math.log(inner)
    else:
        inner = 1.0 + Cr * math.log(1.0 - epsilon)
        if inner <= 0:
            raise ValueError("Cannot invert: argument of log is non-positive.")
        return -math.log(inner) / Cr


def epsilon_NTU_crossflow_both_unmixed_exact(NTU: float, Cr: float) -> float:
    """Exact ε for cross-flow, both fluids unmixed (series solution).

    ε = 1 - exp(-NTU) * Σ_{n=0}^{∞} [Cr^n * NTU^n / (n!)^2 *
         Σ_{k=0}^{n} 1/(n-k+1) * (-1)^k * C(n,k) * exp(k*NTU)]

    Simplified to 50-term summation for accuracy.
    Ref: Kays & London, "Compact Heat Exchangers", 1964.
    """
    if Cr == 0.0:
        return 1.0 - math.exp(-NTU)
    total = 0.0
    for n in range(50):
        inner = 0.0
        for k in range(n + 1):
            binom = math.comb(n, k)
            sign = (-1) ** k
            inner += sign * binom * math.exp(k * NTU) / (n - k + 1)
        total += (Cr ** n) * (NTU ** n) / (math.factorial(n) ** 2) * inner
    return 1.0 - math.exp(-NTU) * total


# ---------------------------------------------------------------------------
# Energy balance helpers  (ref: 08_heat_exchangers.md §1)
# ---------------------------------------------------------------------------

def heat_capacity_rate(m_dot: float, Cp: float) -> float:
    """Heat capacity rate: C = m_dot * Cp [W/K]."""
    return m_dot * Cp


def q_max(C_min: float, Th_i: float, Tc_i: float) -> float:
    """Maximum possible heat transfer: q_max = C_min * (T_h,i - T_c,i)."""
    return C_min * (Th_i - Tc_i)


def Cr(C_min: float, C_max: float) -> float:
    """Heat capacity ratio: Cr = C_min / C_max, 0 <= Cr <= 1."""
    return C_min / C_max


# ---------------------------------------------------------------------------
# Convergence & validation helpers
# ---------------------------------------------------------------------------

def check_convergence(old: float, new: float, tol: float = 1e-4) -> bool:
    """Relative convergence check: |new - old| / |old| < tol."""
    if abs(old) < 1e-15:
        return abs(new) < tol
    return abs(new - old) / abs(old) < tol


def validate_correlation_regime(Re: float, Pr_val: float, L_D: float,
                                Re_min: float = 10_000,
                                Pr_range: tuple = (0.6, 160.0),
                                L_D_min: float = 10.0) -> list[str]:
    """Check validity of Dittus-Boelter correlation. Return list of warnings."""
    warnings_list = []
    if Re < Re_min:
        warnings_list.append(
            f"Re_D = {Re:.0f} < {Re_min} — Dittus-Boelter not valid (turbulent required)"
        )
    if not (Pr_range[0] <= Pr_val <= Pr_range[1]):
        warnings_list.append(
            f"Pr = {Pr_val:.2f} outside valid range [{Pr_range[0]}, {Pr_range[1]}]"
        )
    if L_D < L_D_min:
        warnings_list.append(
            f"L/D = {L_D:.1f} < {L_D_min} — Dittus-Boelter requires L/D >= {L_D_min}"
        )
    return warnings_list


def validate_tube_geometry(D_i: float, D_o: float, L: float) -> None:
    """Basic sanity checks on tube geometry."""
    if D_i <= 0 or D_o <= 0:
        raise ValueError(f"Diameters must be positive, got D_i={D_i}, D_o={D_o}")
    if D_o <= D_i:
        raise ValueError(f"Outer diameter ({D_o}) must exceed inner diameter ({D_i})")
    if L <= 0:
        raise ValueError(f"Length must be positive, got L={L}")


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def fmt(val: float, unit: str, width: int = 14) -> str:
    """Format a value with unit for table output."""
    if abs(val) >= 1e6 or (abs(val) < 0.01 and abs(val) > 0):
        return f"{val:>14.2e} {unit}"
    return f"{val:>14.4f} {unit}"


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def print_result_row(label: str, value: float, unit: str) -> None:
    """Print a single result row."""
    print(f"  {label:<35s} {value:>12.4f} {unit}")
