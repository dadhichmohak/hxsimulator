"""Utility functions — dimensionless numbers, LMTD, convergence checks, validation."""

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
