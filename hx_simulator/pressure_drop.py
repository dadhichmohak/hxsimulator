"""Pressure drop calculations for tube and shell sides.

Tube-side:  Darcy-Weisbach with Blasius (smooth pipe, turbulent) or
            laminar f = 64/Re correlations.
Shell-side: Simplified cross-flow across tube bundle.

All physics follow standard mechanical engineering correlations.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .fluids import FluidProperties
from .utils import Re_D_from_mdot


# ---------------------------------------------------------------------------
# Friction factor correlations
# ---------------------------------------------------------------------------

def blazius_f(Re: float) -> float:
    """Blasius correlation for smooth pipe turbulent flow (Re < 1e5).

    f_D = 0.316 * Re^(-0.25)   (Darcy friction factor)
    """
    return 0.316 * Re ** (-0.25)


def laminar_f(Re: float) -> float:
    """Darcy friction factor for laminar flow in a circular pipe.

    f_D = 64 / Re
    """
    return 64.0 / Re


def transition_f(Re: float) -> float:
    """Approximate friction factor in transition zone (2300 < Re < 10000).

    Linear interpolation between laminar (64/Re at Re=2300) and
    Blasius (0.316*Re^-0.25 at Re=10000).
    """
    f_lam = laminar_f(2300)
    f_turb = blazius_f(10_000)
    frac = (Re - 2300) / (10_000 - 2300)
    return f_lam + frac * (f_turb - f_lam)


def friction_factor(Re: float) -> float:
    """Darcy friction factor with regime selection."""
    if Re <= 0:
        return 0.0
    if Re <= 2300:
        return laminar_f(Re)
    if Re >= 10_000:
        return blazius_f(Re)
    return transition_f(Re)


# ---------------------------------------------------------------------------
# Tube-side pressure drop  (Darcy-Weisbach)
# ---------------------------------------------------------------------------

@dataclass
class PressureDropResult:
    """Pressure drop result for one side of the HX."""
    delta_P: float       # Total pressure drop [Pa]
    delta_P_friction: float  # Friction component [Pa]
    delta_P_minor: float     # Minor losses (entrance/exit) [Pa]
    velocity: float      # Mean velocity [m/s]
    Re: float            # Reynolds number
    f_D: float           # Darcy friction factor
    regime: str          # Flow regime label


def tube_side_dp(m_dot: float, D_i: float, L: float,
                 rho: float, mu: float,
                 include_minor: bool = True,
                 K_ent: float = 0.5, K_exit: float = 1.0) -> PressureDropResult:
    """Tube-side pressure drop using Darcy-Weisbach equation.

    ΔP = f * (L/D) * (rho*v^2/2) + ΣK * (rho*v^2/2)

    Parameters
    ----------
    m_dot       : Mass flow rate [kg/s]
    D_i         : Inner tube diameter [m]
    L           : Tube length [m]
    rho         : Fluid density [kg/m^3]
    mu          : Dynamic viscosity [Pa.s]
    include_minor : Whether to include entrance/exit losses
    K_ent       : Entrance loss coefficient (default 0.5 for sharp-edged)
    K_exit      : Exit loss coefficient (default 1.0)
    """
    if rho <= 0 or D_i <= 0:
        return PressureDropResult(0, 0, 0, 0, 0, 0, "invalid")

    A = math.pi * D_i**2 / 4.0
    v = m_dot / (rho * A)   # mean velocity [m/s]
    Re = Re_D_from_mdot(m_dot, D_i, mu)
    f = friction_factor(Re)

    # Friction pressure drop
    dp_fric = f * (L / D_i) * (rho * v**2 / 2.0)

    # Minor losses
    if include_minor:
        dp_minor = (K_ent + K_exit) * (rho * v**2 / 2.0)
    else:
        dp_minor = 0.0

    dp_total = dp_fric + dp_minor

    # Regime label
    if Re <= 2300:
        regime = "laminar"
    elif Re < 10_000:
        regime = "transition"
    else:
        regime = "turbulent"

    return PressureDropResult(
        delta_P=dp_total,
        delta_P_friction=dp_fric,
        delta_P_minor=dp_minor,
        velocity=v,
        Re=Re,
        f_D=f,
        regime=regime,
    )


# ---------------------------------------------------------------------------
# Shell-side pressure drop  (simplified cross-flow)
# ---------------------------------------------------------------------------

def shell_side_dp(m_dot: float, D_o: float, D_shell: float,
                  L: float, N_tubes: float, rho: float, mu: float,
                  pitch_ratio: float = 1.25,
                  N_baffles: int | None = None,
                  f_shell: float = 0.2) -> PressureDropResult:
    """Shell-side pressure drop across tube bundle.

    Simplified model: ΔP = f_shell * N_baffles * (rho * v_shell^2 / 2)

    The shell-side friction factor f_shell is an empirical constant
    for flow across tube bundles (typically 0.1–0.5 depending on
    pitch ratio and arrangement).

    Parameters
    ----------
    m_dot        : Shell-side mass flow rate [kg/s]
    D_o          : Tube outer diameter [m]
    D_shell      : Shell inner diameter [m]
    L            : Tube length [m]
    N_tubes      : Number of tubes
    rho          : Shell-side fluid density [kg/m^3]
    mu           : Shell-side dynamic viscosity [Pa.s]
    pitch_ratio  : Pitch / D_o (default 1.25)
    N_baffles    : Number of baffles (default: estimate from L)
    f_shell      : Shell-side friction factor (empirical, default 0.2)
    """
    if rho <= 0 or D_o <= 0:
        return PressureDropResult(0, 0, 0, 0, 0, 0, "invalid")

    # Cross-flow area (same as heat_transfer.py)
    pitch = pitch_ratio * D_o
    A_cross = D_shell * (pitch - D_o) * 0.5
    if A_cross <= 0:
        return PressureDropResult(0, 0, 0, 0, 0, 0, "invalid geometry")

    G_shell = m_dot / A_cross  # mass velocity [kg/(m^2.s)]
    v_shell = G_shell / rho
    Re_shell = rho * v_shell * D_o / mu

    # Number of baffles: estimate if not given
    if N_baffles is None:
        baffle_spacing = 0.3 * D_shell  # typical: 30% of shell diameter
        N_baffles = max(1, int(L / baffle_spacing) - 1)

    # Pressure drop
    dp_fric = f_shell * (N_baffles + 1) * (rho * v_shell**2 / 2.0)

    # Regime label
    if Re_shell <= 2300:
        regime = "laminar"
    elif Re_shell < 10_000:
        regime = "transition"
    else:
        regime = "turbulent"

    return PressureDropResult(
        delta_P=dp_fric,
        delta_P_friction=dp_fric,
        delta_P_minor=0.0,
        velocity=v_shell,
        Re=Re_shell,
        f_D=f_shell,
        regime=regime,
    )


# ---------------------------------------------------------------------------
# Convenience
# ---------------------------------------------------------------------------

def compute_both_dp(
    m_dot_tube: float, D_i: float, L: float, fluid_tube: FluidProperties,
    m_dot_shell: float, D_o: float, D_shell: float, N_tubes: int,
    fluid_shell: FluidProperties, pitch_ratio: float = 1.25,
) -> tuple[PressureDropResult, PressureDropResult]:
    """Compute pressure drops on both tube and shell sides."""
    tube_dp = tube_side_dp(m_dot_tube, D_i, L,
                           fluid_tube.rho, fluid_tube.mu)
    shell_dp = shell_side_dp(m_dot_shell, D_o, D_shell, L, N_tubes,
                             fluid_shell.rho, fluid_shell.mu, pitch_ratio)
    return tube_dp, shell_dp
