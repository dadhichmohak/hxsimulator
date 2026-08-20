"""Two-phase heat transfer correlations for condensation and boiling.

Covers:
  - Condensation: Nusselt (laminar film), Shah (turbulent), Kern
  - Boiling: Rohsenow (nucleate pool), Mostinski (convective), Forster-Zuber
  - Two-phase multipliers (Lockhart-Martinelli)

References:
  - Incropera & DeWitt, "Fundamentals of Heat and Mass Transfer"
  - Shah, M.M. "A General Correlation for Heat Transfer During Film Condensation", 1979
  - Rohsenow, W.M. "Boiling", Handbook of Heat Transfer, 1985
  - Mostinski, I.L. "Calculation of Heat Transfer and Burnout in沸腾液体", 1963
  - Kern, D.Q. "Process Heat Transfer"
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class TwoPhaseResult:
    """Result of a two-phase heat transfer calculation."""
    h_tp: float             # Two-phase heat transfer coefficient [W/m2K]
    method: str             # Correlation used
    regime: str             # Flow regime (laminar film, nucleate, convective)
    warnings: list[str]


# ---------------------------------------------------------------------------
# Condensation correlations
# ---------------------------------------------------------------------------

def nusselt_condensation(
    rho_l: float,      # Liquid density [kg/m^3]
    rho_v: float,      # Vapor density [kg/m^3]
    k_l: float,        # Liquid thermal conductivity [W/mK]
    mu_l: float,        # Liquid viscosity [Pa.s]
    h_fg: float,        # Latent heat of vaporization [J/kg]
    g: float = 9.81,    # Gravity [m/s^2]
    D_o: float = 0.025, # Tube outer diameter [m]
    vertical: bool = False,
) -> TwoPhaseResult:
    """Nusselt film condensation on a single tube.

    For vertical tubes: h = 0.943 * [g*rho_l*(rho_l-rho_v)*k_l^3*h_fg /
                          (mu_l*(T_sat-T_w)*D_o)]^0.25

    For horizontal tubes: h = 0.728 * [g*rho_l*(rho_l-rho_v)*k_l^3*h_fg /
                           (mu_l*(T_sat-T_w)*D_o)]^0.25

    Simplified (not iterative): h = C * [g*rho_l*(rho_l-rho_v)*k_l^3*h_fg / (mu_l*D_o)]^0.25
    """
    if rho_l <= 0 or k_l <= 0 or mu_l <= 0 or h_fg <= 0:
        return TwoPhaseResult(0.0, "Nusselt", "invalid", ["Invalid fluid properties"])

    delta_rho = max(rho_l - rho_v, 0.1)

    if vertical:
        C = 0.943
    else:
        C = 0.728

    group = g * rho_l * delta_rho * k_l**3 * h_fg / (mu_l * D_o)
    h = C * (group ** 0.25)

    return TwoPhaseResult(h, "Nusselt film", "laminar film", [])


def shah_condensation(
    rho_l: float,
    rho_v: float,
    k_l: float,
        mu_l: float,
    Cp_l: float,
    h_fg: float,
    G: float,          # Mass flux [kg/(m^2.s)]
    D_h: float,        # Hydraulic diameter [m]
    Pr_l: float = None,
    x_vapor: float = 0.5,  # Vapor quality
) -> TwoPhaseResult:
    """Shah (1979) correlation for condensation inside tubes.

    Nu_tp = Nu_l * [(1-x)^0.8 + 3.8*x^0.76*(1-x)^0.04 / P_r^0.38]

    where Nu_l = 0.023 * Re_l^0.8 * Pr_l^0.4
    """
    if Pr_l is None:
        Pr_l = Cp_l * mu_l / k_l

    if G <= 0 or D_h <= 0 or mu_l <= 0:
        return TwoPhaseResult(0.0, "Shah", "invalid", ["Invalid flow parameters"])

    # Single-phase liquid Reynolds number (all liquid flowing)
    Re_l = G * D_h / mu_l
    if Re_l < 2300:
        Nu_l = 3.66  # laminar
    else:
        Nu_l = 0.023 * Re_l**0.8 * Pr_l**0.4

    P_r = 1.0  # reduced pressure (simplified)

    x = max(0.0, min(1.0, x_vapor))
    term1 = (1 - x)**0.8
    term2 = 3.8 * x**0.76 * (1 - x)**0.04 / max(P_r**0.38, 0.01)

    Nu_tp = Nu_l * (term1 + term2)
    h_tp = Nu_tp * k_l / D_h

    return TwoPhaseResult(h_tp, "Shah (1979)", "condensation", [])


def kern_condensation(
    rho_l: float,
    k_l: float,
    mu_l: float,
    h_fg: float,
    D_o: float,
    g: float = 9.81,
) -> TwoPhaseResult:
    """Kern method for condensation on outside of horizontal tubes.

    h = 0.728 * [g * rho_l * (rho_l - rho_v) * k_l^3 * h_fg /
                 (mu_l * D_o)]^0.25

    Simplified using only liquid properties.
    """
    if rho_l <= 0 or k_l <= 0 or mu_l <= 0 or h_fg <= 0:
        return TwoPhaseResult(0.0, "Kern", "invalid", ["Invalid properties"])

    group = g * rho_l**2 * k_l**3 * h_fg / (mu_l * D_o)
    h = 0.728 * (group ** 0.25)

    return TwoPhaseResult(h, "Kern condensation", "laminar film", [])


# ---------------------------------------------------------------------------
# Boiling correlations
# ---------------------------------------------------------------------------

def rohsenow_pool_boiling(
    rho_l: float,
    rho_v: float,
    sigma: float,       # Surface tension [N/m]
    h_fg: float,
    Cp_l: float,
    mu_l: float,
    k_l: float,
    dT_e: float,        # Excess temperature (T_w - T_sat) [K]
    C_sf: float = 0.013, # Surface-fluid coefficient (water-steel ~ 0.013)
    n_exp: int = 1,      # Exponent for Cp*mu (1 for water, 1.7 for others)
    g: float = 9.81,
) -> TwoPhaseResult:
    """Rohsenow correlation for nucleate pool boiling.

    q/A = mu_l * h_fg * [g*(rho_l-rho_v)/sigma]^0.5 *
          [(Cp_l * dT_e) / (C_sf * h_fg * Pr_l^n)]^3

    h = q/A / dT_e
    """
    if rho_l <= 0 or rho_v <= 0 or sigma <= 0 or h_fg <= 0 or mu_l <= 0:
        return TwoPhaseResult(0.0, "Rohsenow", "invalid", ["Invalid properties"])

    Pr_l = Cp_l * mu_l / k_l if k_l > 0 else 1.0

    g_mod = g * (rho_l - rho_v)
    if g_mod < 0:
        g_mod = g * rho_l * 0.01  # fallback

    q_over_A = (
        mu_l * h_fg *
        (g_mod / sigma) ** 0.5 *
        ((Cp_l * dT_e) / (C_sf * h_fg * max(Pr_l**n_exp, 1e-10))) ** 3
    )

    h_tp = q_over_A / dT_e if dT_e > 0 else 0.0

    return TwoPhaseResult(h_tp, "Rohsenow pool boiling", "nucleate boiling", [])


def mostinski_convective_boiling(
    rho_l: float,
    rho_v: float,
    k_l: float,
    Cp_l: float,
    mu_l: float,
    h_fg: float,
    D_o: float,
    P: float,           # System pressure [Pa]
    P_crit: float = 22.06e6,  # Critical pressure of water [Pa]
    g: float = 9.81,
) -> TwoPhaseResult:
    """Mostinski correlation for convective boiling in tubes.

    h_tp = 0.00417 * (q/A)^0.7 * P_crit^0.14 * F_p
    where F_p is a pressure function.

    Simplified form for preliminary design.
    """
    if rho_l <= 0 or rho_v <= 0:
        return TwoPhaseResult(0.0, "Mostinski", "invalid", ["Invalid properties"])

    P_r = P / P_crit if P_crit > 0 else 0.5
    P_r = max(0.01, min(0.99, P_r))

    # Simplified: h = C * P_crit^0.14 * f(P_r)
    C = 0.00417
    F_p = (1.8 * P_r**0.17) + (4.51 * P_r**0.87) - (3.39 * P_r**2.27)

    # For a typical heat flux of 50 kW/m2
    q_over_A = 50000.0  # approximate
    h_tp = C * q_over_A**0.7 * P_crit**0.14 * F_p

    return TwoPhaseResult(h_tp, "Mostinski convective boiling", "convective boiling", [])


def forster_zuber_boiling(
    rho_l: float,
    rho_v: float,
    sigma: float,
    Cp_l: float,
    mu_l: float,
    k_l: float,
    h_fg: float,
    dT_e: float,
    P: float,
    P_crit: float = 22.06e6,
) -> TwoPhaseResult:
    """Forster-Zuber correlation for nucleate pool boiling.

    h = 0.00122 * [(k_l^0.79 * Cp_l^0.45 * rho_l^0.49) /
                    (sigma^0.5 * mu_l^0.29 * h_fg^0.24 * rho_v^0.24)] *
        (dT_e)^0.24 * (P_sat(T_w) - P)^0.75
    """
    if rho_l <= 0 or rho_v <= 0 or sigma <= 0:
        return TwoPhaseResult(0.0, "Forster-Zuber", "invalid", ["Invalid properties"])

    P_r = max(0.01, min(0.99, P / P_crit))

    numerator = k_l**0.79 * Cp_l**0.45 * rho_l**0.49
    denominator = sigma**0.5 * mu_l**0.29 * h_fg**0.24 * rho_v**0.24

    if denominator <= 0:
        return TwoPhaseResult(0.0, "Forster-Zuber", "invalid", ["Zero denominator"])

    # Approximate P_sat(T_w) - P using reduced pressure
    delta_P = P_r * P * 0.1  # rough approximation

    h_tp = 0.00122 * (numerator / denominator) * max(dT_e, 0.1)**0.24 * delta_P**0.75

    return TwoPhaseResult(h_tp, "Forster-Zuber nucleate boiling", "nucleate boiling", [])


# ---------------------------------------------------------------------------
# Lockhart-Martinelli two-phase multiplier
# ---------------------------------------------------------------------------

def lockhart_martinelli_multiplier(
    x: float,           # Vapor quality
    rho_l: float,
    rho_v: float,
    mu_l: float,
    mu_v: float,
) -> float:
    """Lockhart-Martinelli two-phase pressure drop multiplier (phi_l).

    Returns phi_l^2 for liquid-phase reference dP.
    """
    if x <= 0 or x >= 1:
        return 1.0
    if rho_l <= 0 or rho_v <= 0:
        return 1.0

    X_tt = ((1 - x) / x)**0.9 * (rho_v / rho_l)**0.5 * (mu_l / mu_v)**0.1

    if X_tt <= 0:
        return 1.0

    # Turbulent-turbulent correlation
    phi_l2 = 1 + 20.0 / X_tt + 1.0 / X_tt**2
    return phi_l2
