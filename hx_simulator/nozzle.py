"""Nozzle sizing for shell-and-tube heat exchangers.

Sizes inlet and outlet nozzles based on:
  - Allowable velocity limits (TEMA/API guidelines)
  - Pressure drop constraints
  - Erosion velocity checks

Typical limits:
  - Liquid: 1.5–3.0 m/s
  - Gas: 15–30 m/s
  - Steam: 30–60 m/s
  - Two-phase: 5–15 m/s
"""

from __future__ import annotations

import math
from dataclasses import dataclass


# Standard nozzle sizes (NPS in inches)
STANDARD_NPS = [
    0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0,
    6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 24.0,
]

# Allowable velocities by fluid type [m/s]
ALLOWABLE_VELOCITY = {
    "liquid": {"min": 0.5, "max": 3.0, "typical": 1.5},
    "gas": {"min": 5.0, "max": 30.0, "typical": 15.0},
    "steam": {"min": 15.0, "max": 60.0, "typical": 30.0},
    "two_phase": {"min": 2.0, "max": 15.0, "typical": 8.0},
    "viscous_liquid": {"min": 0.3, "max": 1.5, "typical": 0.8},
}

# Standard flange ratings (pressure classes)
FLANGE_CLASSES = [150, 300, 400, 600, 900, 1500, 2500]


@dataclass
class NozzleResult:
    """Nozzle sizing result."""
    NPS: float              # Nominal pipe size [inches]
    D_nozzle: float         # Inner diameter [m]
    velocity: float         # Actual velocity [m/s]
    dP_nozzle: float        # Pressure drop across nozzle [Pa]
    flange_class: int       # ASME B16.5 flange class
    erosion_velocity: float # Erosion velocity limit [m/s]
    erosion_ok: bool        # Velocity below erosion limit
    area: float             # Nozzle flow area [m^2]
    warnings: list[str]


def erosion_velocity_liquid(
    rho: float,
    D_nozzle: float,
    viscosity: float = 0.001,
) -> float:
    """Erosion velocity limit for liquid service.

    Based on API 14E: v_erosion = C / sqrt(rho)
    where C ~ 122 for continuous service, 152 for intermittent.
    """
    if rho <= 0:
        return 100.0
    C = 122.0  # continuous service
    return C / math.sqrt(rho)


def erosion_velocity_gas(
    rho: float,
    D_nozzle: float,
    solid_content: float = 0.0,
) -> float:
    """Erosion velocity for gas service (with possible solids)."""
    if rho <= 0:
        return 100.0
    C = 150.0  # clean gas
    if solid_content > 0:
        C = C / (1 + solid_content * 10)
    return C / math.sqrt(rho)


def size_nozzle(
    m_dot: float,
    rho: float,
    fluid_type: str = "liquid",
    D_max: float = 0.3,
    D_shell: float = 0.1,
    pressure: float = 1e6,
    temperature: float = 350.0,
    viscosity: float = 0.001,
) -> NozzleResult:
    """Size a nozzle for given flow conditions.

    Parameters
    ----------
    m_dot      : Mass flow rate [kg/s]
    rho        : Fluid density [kg/m^3]
    fluid_type : 'liquid', 'gas', 'steam', 'two_phase', 'viscous_liquid'
    D_max      : Maximum nozzle diameter [m] (typically <= D_shell)
    D_shell    : Shell inner diameter [m]
    pressure   : Operating pressure [Pa]
    temperature: Temperature [K]
    viscosity  : Dynamic viscosity [Pa.s]
    """
    warnings = []

    vel_limits = ALLOWABLE_VELOCITY.get(fluid_type, ALLOWABLE_VELOCITY["liquid"])
    v_typical = vel_limits["typical"]
    v_max = vel_limits["max"]

    # Required flow area for typical velocity
    A_required = m_dot / (rho * v_typical) if rho > 0 and v_typical > 0 else 0.001

    # Required diameter
    D_required = math.sqrt(4 * A_required / math.pi)

    # Find closest standard NPS
    D_required_inch = D_required * 39.3701  # m to inches
    best_nps = STANDARD_NPS[0]
    for nps in STANDARD_NPS:
        if nps >= D_required_inch:
            best_nps = nps
            break
        best_nps = nps

    # Actual nozzle diameter (assume schedule 40)
    D_nozzle = best_nps * 0.0254  # inches to meters (ID approx)
    # Schedule 40 wall thickness correction (approximate)
    wall = max(0.002, best_nps * 0.0003)
    D_nozzle_id = D_nozzle - 2 * wall

    # Actual velocity
    A_actual = math.pi / 4 * D_nozzle_id**2
    velocity = m_dot / (rho * A_actual) if rho > 0 and A_actual > 0 else 0.0

    # Pressure drop (simplified: dP = 0.5 * rho * v^2)
    dP_nozzle = 0.5 * rho * velocity**2

    # Erosion check
    if fluid_type in ("liquid", "viscous_liquid"):
        v_erosion = erosion_velocity_liquid(rho, D_nozzle_id, viscosity)
    else:
        v_erosion = erosion_velocity_gas(rho, D_nozzle_id)

    erosion_ok = velocity < v_erosion

    # Flange class selection based on pressure and temperature
    flange_class = 150
    for cls in FLANGE_CLASSES:
        if pressure <= cls * 6894.76:  # psi to Pa
            flange_class = cls
            break
        flange_class = cls

    # Warnings
    if velocity > v_max:
        warnings.append(
            f"Velocity {velocity:.1f} m/s exceeds max {v_max:.1f} m/s for {fluid_type}"
        )
    if velocity < vel_limits["min"]:
        warnings.append(
            f"Velocity {velocity:.1f} m/s below min {vel_limits['min']:.1f} m/s — oversized nozzle"
        )
    if D_nozzle_id > D_shell * 0.6:
        warnings.append(
            f"Nozzle {D_nozzle_id*1000:.0f}mm > 60% of shell {D_shell*1000:.0f}mm"
        )

    return NozzleResult(
        NPS=best_nps,
        D_nozzle=D_nozzle_id,
        velocity=velocity,
        dP_nozzle=dP_nozzle,
        flange_class=flange_class,
        erosion_velocity=v_erosion,
        erosion_ok=erosion_ok,
        area=A_actual,
        warnings=warnings,
    )
