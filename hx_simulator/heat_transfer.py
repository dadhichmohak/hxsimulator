"""Heat transfer coefficient calculations.

Correlations implemented:
  - Tube-side:  Dittus-Boelter (turbulent), laminar Nu constants
  - Shell-side: Donohue equation for cross-flow across tube bundles
  - Overall U:  cylindrical wall with convection on both sides + fouling
  - Fins:       efficiency and overall surface effectiveness

All formulas from HTOA 2025 references (see specific equations in comments).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .fluids import FluidProperties
from .utils import (
    Re_D_from_mdot, Nu_D, Pr as Pr_num, h_from_Nu,
    check_convergence, validate_correlation_regime, validate_tube_geometry,
)


# ---------------------------------------------------------------------------
# Fouling resistances
# Ref: TEMA Standards, 10th Ed. (2019), Table RGP-T-2.4-2
#      Kern, D.Q., "Process Heat Transfer", McGraw-Hill, 1950, Ch. 18
#      Values in [m^2.K/W] per side (inner tube, outer shell)
# ---------------------------------------------------------------------------

FOULING_FACTORS: dict[str, tuple[float, float]] = {
    # (R_fi, R_fo) in [m^2.K/W]  — inner and outer
    "seawater":            (1.0e-4, 1.0e-4),
    "treated_cooling_water": (1.5e-4, 1.5e-4),
    "river_water":         (3.0e-4, 3.0e-4),
    "fuel_oil":            (9.0e-4, 9.0e-4),
    "steam":               (0.0,    0.0),
    "clean":               (0.0,    0.0),
    "none":                (0.0,    0.0),
}

# Human-readable descriptions for each fouling condition (with units and source)
# Ref: TEMA Standards 10th Ed., Table RGP-T-2.4-2
FOULING_DESCRIPTIONS: dict[str, str] = {
    "seawater": (
        "Rf = 0.0001 m²·K/W per side. Treated seawater with low sediment. "
        "TEMA Table RGP-T-2.4-2: seawater below 50°C, velocity > 1 m/s."
    ),
    "treated_cooling_water": (
        "Rf = 0.00015 m²·K/W per side. River/lake water after chemical treatment "
        "(filtration, biocide). TEMA Table RGP-T-2.4-2: cooling tower supply."
    ),
    "river_water": (
        "Rf = 0.0003 m²·K/W per side. Untreated river water with silt and organics. "
        "TEMA Table RGP-T-2.4-2: un-clarified raw river water."
    ),
    "fuel_oil": (
        "Rf = 0.0009 m²·K/W per side. Heavy fuel oil / residuum at > 50°C. "
        "TEMA Table RGP-T-2.4-2: No. 2 fuel oil and heavier."
    ),
    "steam": (
        "Rf = 0.0 m²·K/W (clean steam, no fouling expected). "
        "TEMA Table RGP-T-2.4-2: steam condensate, well-treated."
    ),
    "clean": (
        "Rf = 0.0 m²·K/W. Clean service, no fouling anticipated. "
        "Use for gas-gas or single-phase clean fluid services."
    ),
    "none": (
        "Rf = 0.0 m²·K/W. No fouling resistance applied. "
        "Idealized condition; real exchangers always have some fouling."
    ),
}

# Mapping from FOULING_FACTORS keys to TEMA_FOULING keys for fouling trend prediction
_FOULING_KEY_MAP: dict[str, str] = {
    "seawater": "cooling_water (sea)",
    "treated_cooling_water": "cooling_water (treated)",
    "river_water": "cooling_water (untreated)",
    "fuel_oil": "heavy fuel oil",
    "steam": "steam",
    "clean": "cooling_water (treated)",   # fallback
    "none": "cooling_water (treated)",    # fallback
}


@dataclass
class HTCoefficients:
    """Container for computed heat transfer results."""
    Re_i: float           # Tube-side Reynolds number
    Pr_i: float           # Tube-side Prandtl number
    Nu_i: float           # Tube-side Nusselt number
    h_i: float            # Tube-side heat transfer coefficient [W/(m^2.K)]
    Re_o: float           # Shell-side Reynolds number
    Pr_o: float           # Shell-side Prandtl number
    Nu_o: float           # Shell-side Nusselt number
    h_o: float            # Shell-side heat transfer coefficient [W/(m^2.K)]
    U_o: float            # Overall coefficient (ref outer area) clean [W/(m^2.K)]
    U_o_fouled: float     # Overall coefficient with fouling [W/(m^2.K)]
    warnings: list[str]   # Validity warnings


# ---------------------------------------------------------------------------
# Tube-side: Dittus-Boelter  (ref: 06_convection_internal.md §5)
# ---------------------------------------------------------------------------

def dittus_boelter(Re: float, Pr_val: float, heating: bool = True) -> float:
    """Dittus-Boelter correlation for fully developed turbulent pipe flow.

    Nu_D = 0.023 * Re_D^(4/5) * Pr^n
        n = 0.4 for heating (T_s > T_m)
        n = 0.3 for cooling (T_s < T_m)

    Validity: 0.6 <= Pr <= 160, Re_D >= 10000, L/D >= 10
    """
    n = 0.4 if heating else 0.3
    return 0.023 * Re ** 0.8 * Pr_val ** n


def laminar_Nu(heating: bool = True) -> float:
    """Fully developed laminar Nusselt number in a circular tube.

    Nu = 4.36 for constant heat flux (heating)
    Nu = 3.66 for constant wall temperature (cooling)
    """
    return 4.36 if heating else 3.66


def compute_h_tube(m_dot: float, D_i: float, L: float,
                   fluid: FluidProperties, heating: bool = True,
                   laminar_as_const_ts: bool = True) -> tuple[float, list[str]]:
    """Compute tube-side (internal) heat transfer coefficient.

    Returns (h_i, warnings_list).
    """
    warnings_list = []
    Re = Re_D_from_mdot(m_dot, D_i, fluid.mu)
    Pr_val = fluid.Pr

    if Re >= 10_000:
        # Turbulent — use Dittus-Boelter
        w = validate_correlation_regime(Re, Pr_val, L / D_i)
        warnings_list.extend(w)
        Nu = dittus_boelter(Re, Pr_val, heating)
    elif Re <= 2300:
        # Laminar
        Nu = laminar_Nu(not laminar_as_const_ts)
        warnings_list.append(
            f"Laminar flow (Re={Re:.0f}) — using Nu={Nu:.2f} (fully developed)"
        )
    else:
        # Transition — linear interpolation (approximate)
        Nu_lam = laminar_Nu(laminar_as_const_ts)
        Nu_turb = dittus_boelter(Re, Pr_val, heating)
        frac = (Re - 2300) / (10_000 - 2300)
        Nu = Nu_lam + frac * (Nu_turb - Nu_lam)
        warnings_list.append(
            f"Transition zone (Re={Re:.0f}) — interpolated Nu={Nu:.2f}"
        )

    h_i = h_from_Nu(Nu, fluid.k, D_i)
    return h_i, warnings_list


# ---------------------------------------------------------------------------
# Shell-side: Donohue equation  (ref: 08_heat_exchangers.md §3.2)
# ---------------------------------------------------------------------------

def shell_side_equivalent_diameter(D_shell: float, D_o: float,
                                   pitch: float | None = None) -> float:
    """Equivalent diameter for shell-side flow across tube bundle.

    For a triangular pitch: D_eq = 4*(pitch^2/2 - pi*D_o^2/8) / (pi*D_o/2)
    Simplified: D_eq ≈ D_shell for order-of-magnitude estimate.
    For the Donohue equation, we use D_o directly.
    """
    # Donohue uses D_o directly for Re and Nu
    return D_o


def shell_side_velocity(m_dot: float, D_shell: float, D_o: float,
                        N_tubes: float, pitch_ratio: float = 1.25) -> float:
    """Estimate shell-side cross-flow velocity.

    v_shell = m_dot / (rho * A_cross)
    A_cross = D_shell * (pitch - D_o) * (some fraction for baffle cut)
    Simplified: A_cross = D_shell * D_o * (pitch_ratio - 1) * 0.5  (50% baffle cut)
    """
    # Simplified cross-flow area at the shell centerline
    pitch = pitch_ratio * D_o
    A_cross = D_shell * (pitch - D_o) * 0.5  # approximate
    return m_dot / A_cross  # This gives mass flux, need to divide by rho later


def donohue(Re_shell: float, Pr_val: float) -> float:
    """Donohue equation for shell-side flow across tube bundles.

    Nu_Do = 0.2 * Re_Do^0.6 * Pr^0.33
    """
    return 0.2 * Re_shell ** 0.6 * Pr_val ** 0.33


def compute_h_shell(m_dot: float, D_o: float, D_shell: float,
                    L: float, N_tubes: float,
                    fluid: FluidProperties,
                    pitch_ratio: float = 1.25) -> tuple[float, float, list[str]]:
    """Compute shell-side heat transfer coefficient.

    Returns (h_o, Re_shell, warnings_list).
    """
    warnings_list = []

    # Shell-side cross-flow velocity
    pitch = pitch_ratio * D_o
    A_cross = D_shell * (pitch - D_o) * 0.5
    if A_cross <= 0:
        raise ValueError("Invalid shell geometry: cross-flow area <= 0")
    G_shell = m_dot / A_cross  # mass velocity [kg/(m^2.s)]
    v_shell = G_shell / fluid.rho  # mean velocity [m/s]

    # Reynolds number based on D_o
    Re_shell = fluid.rho * v_shell * D_o / fluid.mu

    # Nusselt (Donohue)
    Pr_val = fluid.Pr
    Nu = donohue(Re_shell, Pr_val)
    h_o = h_from_Nu(Nu, fluid.k, D_o)

    return h_o, Re_shell, warnings_list


# ---------------------------------------------------------------------------
# Overall heat transfer coefficient  (ref: 08_heat_exchangers.md §3, 02 §4c)
# ---------------------------------------------------------------------------

def U_clean(D_i: float, D_o: float, L: float,
            h_i: float, h_o: float,
            k_wall: float) -> float:
    """Clean overall heat transfer coefficient referenced to outer area.

    1/U_o = (D_o/D_i)/h_i + D_o*ln(D_o/D_i)/(2*k_wall) + 1/h_o

    Parameters
    ----------
    k_wall : float   Thermal conductivity of tube wall material [W/(m.K)]
    """
    R_tube_conv_i = (D_o / D_i) / h_i
    R_wall = D_o * math.log(D_o / D_i) / (2.0 * k_wall)
    R_tube_conv_o = 1.0 / h_o
    return 1.0 / (R_tube_conv_i + R_wall + R_tube_conv_o)


def U_fouled(U_clean_val: float, D_i: float, D_o: float,
             R_fi: float, R_fo: float) -> float:
    """Overall U with fouling resistances on both sides.

    1/U_f = 1/U_clean + R_fi*(A_o/A_i) + R_fo
    A_o/A_i = D_o/D_i
    """
    A_ratio = D_o / D_i
    return 1.0 / (1.0 / U_clean_val + R_fi * A_ratio + R_fo)


# ---------------------------------------------------------------------------
# Fins  (ref: 07_fins.md §2–§8)
# ---------------------------------------------------------------------------

@dataclass
class FinResult:
    """Result of a fin calculation."""
    m: float           # Fin parameter [1/m]
    eta_f: float       # Fin efficiency [-]
    q_f: float         # Heat transfer from fin [W]
    effectiveness: float  # Fin effectiveness [-]


def fin_analysis(h: float, P: float, A_c: float, k_fin: float,
                 L_fin: float, T_base: float, T_inf: float) -> FinResult:
    """Analyse a rectangular fin with adiabatic tip.

    Parameters
    ----------
    h      : Convection coefficient [W/(m^2.K)]
    P      : Fin perimeter [m]
    A_c    : Fin cross-sectional area [m^2]
    k_fin  : Fin material conductivity [W/(m.K)]
    L_fin  : Fin length [m]
    T_base : Base temperature [K]
    T_inf  : Fluid temperature [K]
    """
    # Fin parameter
    m_val = math.sqrt(h * P / (k_fin * A_c))

    # Fin efficiency (adiabatic tip)
    mL = m_val * L_fin
    if mL < 1e-10:
        eta_f = 1.0
    else:
        eta_f = math.tanh(mL) / mL

    # Heat transfer from fin
    theta_b = T_base - T_inf
    q_f = math.sqrt(h * P * k_fin * A_c) * theta_b * math.tanh(mL)

    # Fin effectiveness
    q_no_fin = h * A_c * theta_b
    effectiveness = q_f / q_no_fin if q_no_fin > 0 else 0.0

    return FinResult(m=m_val, eta_f=eta_f, q_f=q_f, effectiveness=effectiveness)


def overall_surface_efficiency(N_fins: float, A_fin: float,
                               A_unfinned: float, eta_f: float) -> float:
    """Overall surface efficiency for a finned surface.

    eta_o = 1 - (N*A_fin / A_total) * (1 - eta_f)
    """
    A_total = N_fins * A_fin + A_unfinned
    if A_total <= 0:
        return 1.0
    return 1.0 - (N_fins * A_fin / A_total) * (1.0 - eta_f)


# ---------------------------------------------------------------------------
# Convenience: full tube-side + shell-side + overall calculation
# ---------------------------------------------------------------------------

def compute_full_ht(
    m_dot_tube: float, D_i: float, D_o: float, L: float,
    fluid_tube: FluidProperties,
    m_dot_shell: float, D_shell: float, N_tubes: float,
    fluid_shell: FluidProperties,
    k_wall: float = 50.0,
    pitch_ratio: float = 1.25,
    fouling: str = "clean",
    heating: bool = True,
) -> HTCoefficients:
    """Run the full heat transfer coefficient calculation.

    Returns HTCoefficients with h_i, h_o, U_o (clean and fouled).
    """
    all_warnings: list[str] = []

    # Tube-side
    h_i, w_i = compute_h_tube(m_dot_tube, D_i, L, fluid_tube, heating)
    all_warnings.extend(w_i)

    # Shell-side
    h_o, Re_shell, w_o = compute_h_shell(
        m_dot_shell, D_o, D_shell, L, N_tubes, fluid_shell, pitch_ratio
    )
    all_warnings.extend(w_o)

    # Reynolds/Prandtl numbers for reporting
    Re_i = Re_D_from_mdot(m_dot_tube, D_i, fluid_tube.mu)
    Pr_i = fluid_tube.Pr
    Nu_i = Nu_D(h_i, D_i, fluid_tube.k)
    Pr_o = fluid_shell.Pr
    Nu_o = Nu_D(h_o, D_o, fluid_shell.k)

    # Overall U
    U_c = U_clean(D_i, D_o, L, h_i, h_o, k_wall)

    # Fouling
    R_fi, R_fo = FOULING_FACTORS.get(fouling, (0.0, 0.0))
    U_f = U_fouled(U_c, D_i, D_o, R_fi, R_fo)

    return HTCoefficients(
        Re_i=Re_i, Pr_i=Pr_i, Nu_i=Nu_i, h_i=h_i,
        Re_o=Re_shell, Pr_o=Pr_o, Nu_o=Nu_o, h_o=h_o,
        U_o=U_c, U_o_fouled=U_f,
        warnings=all_warnings,
    )
