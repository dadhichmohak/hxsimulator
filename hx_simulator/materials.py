"""ASME material database for heat exchanger design.

Provides material properties for common alloys used in shell-and-tube
heat exchangers per ASME Section II Part D.

Properties: density, thermal conductivity, Young's modulus, allowable stress,
            Poisson ratio, thermal expansion coefficient.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MaterialProps:
    """Material properties for mechanical and thermal analysis."""
    name: str
    density: float          # [kg/m^3]
    k_thermal: float        # [W/mK] at ~100C
    E_modulus: float        # [Pa] at ~100C
    allowable_stress: float # [Pa] at ~100C
    Poisson: float          # [-]
    alpha: float            # [1/K] thermal expansion coefficient
    max_temp: float         # [K] maximum service temperature
    corrosion_allowance: float  # [m] typical
    cost_per_kg: float      # [USD/kg] approximate


# ASME approved materials for heat exchanger service
MATERIAL_DB: dict[str, MaterialProps] = {
    # Carbon steel
    "SA-179": MaterialProps(
        name="SA-179 Carbon Steel (Seamless Cold-Drawn)",
        density=7850, k_thermal=52.0, E_modulus=2.0e11,
        allowable_stress=138e6, Poisson=0.3, alpha=12e-6,
        max_temp=723, corrosion_allowance=0.003, cost_per_kg=1.5,
    ),
    "SA-192": MaterialProps(
        name="SA-192 Carbon Steel (Seamless, Boiler)",
        density=7850, k_thermal=52.0, E_modulus=2.0e11,
        allowable_stress=138e6, Poisson=0.3, alpha=12e-6,
        max_temp=723, corrosion_allowance=0.003, cost_per_kg=1.6,
    ),
    "SA-210": MaterialProps(
        name="SA-210 Carbon Steel (Seamless, Medium Carbon)",
        density=7850, k_thermal=48.0, E_modulus=2.0e11,
        allowable_stress=158e6, Poisson=0.3, alpha=12e-6,
        max_temp=773, corrosion_allowance=0.003, cost_per_kg=2.0,
    ),

    # Low alloy steel
    "SA-213-T11": MaterialProps(
        name="SA-213-T11 (1.25Cr-0.5Mo)",
        density=7850, k_thermal=40.0, E_modulus=2.0e11,
        allowable_stress=103e6, Poisson=0.3, alpha=13e-6,
        max_temp=866, corrosion_allowance=0.001, cost_per_kg=3.5,
    ),
    "SA-213-T22": MaterialProps(
        name="SA-213-T22 (2.25Cr-1Mo)",
        density=7850, k_thermal=35.0, E_modulus=2.0e11,
        allowable_stress=103e6, Poisson=0.3, alpha=13.5e-6,
        max_temp=923, corrosion_allowance=0.001, cost_per_kg=5.0,
    ),

    # Stainless steel
    "SA-249-304": MaterialProps(
        name="SA-249 304 Stainless Steel",
        density=8000, k_thermal=16.0, E_modulus=1.93e11,
        allowable_stress=138e6, Poisson=0.3, alpha=17.3e-6,
        max_temp=1143, corrosion_allowance=0.0, cost_per_kg=5.5,
    ),
    "SA-249-316": MaterialProps(
        name="SA-249 316 Stainless Steel",
        density=8000, k_thermal=16.0, E_modulus=1.93e11,
        allowable_stress=138e6, Poisson=0.3, alpha=16.0e-6,
        max_temp=1143, corrosion_allowance=0.0, cost_per_kg=6.5,
    ),
    "SA-249-321": MaterialProps(
        name="SA-249 321 Stainless Steel (Ti-stabilized)",
        density=8000, k_thermal=16.0, E_modulus=1.93e11,
        allowable_stress=138e6, Poisson=0.3, alpha=16.6e-6,
        max_temp=1173, corrosion_allowance=0.0, cost_per_kg=7.0,
    ),

    # Nickel alloys
    "SB-163-Inconel-600": MaterialProps(
        name="Inconel 600 (Ni-Cr-Fe)",
        density=8470, k_thermal=15.0, E_modulus=2.14e11,
        allowable_stress=158e6, Poisson=0.3, alpha=13.0e-6,
        max_temp=1366, corrosion_allowance=0.0, cost_per_kg=25.0,
    ),
    "SB-163-Monel-400": MaterialProps(
        name="Monel 400 (Ni-Cu)",
        density=8800, k_thermal=25.0, E_modulus=1.79e11,
        allowable_stress=129e6, Poisson=0.32, alpha=13.9e-6,
        max_temp=923, corrosion_allowance=0.0, cost_per_kg=18.0,
    ),

    # Titanium
    "SB-338-Gr2": MaterialProps(
        name="Titanium Grade 2 (CP Ti)",
        density=4510, k_thermal=16.4, E_modulus=1.05e11,
        allowable_stress=172e6, Poisson=0.34, alpha=8.4e-6,
        max_temp=573, corrosion_allowance=0.0, cost_per_kg=35.0,
    ),

    # Copper alloys
    "SB-111-CuNi-70/30": MaterialProps(
        name="Copper-Nickel 70/30",
        density=8900, k_thermal=30.0, E_modulus=1.52e11,
        allowable_stress=117e6, Poisson=0.34, alpha=16.0e-6,
        max_temp=773, corrosion_allowance=0.0, cost_per_kg=8.0,
    ),
    "SB-111-Brass": MaterialProps(
        name="Admiralty Brass (70Cu-29Zn-1Sn)",
        density=8530, k_thermal=110.0, E_modulus=1.1e11,
        allowable_stress=83e6, Poisson=0.34, alpha=21.2e-6,
        max_temp=573, corrosion_allowance=0.0, cost_per_kg=5.0,
    ),
}


def get_material(spec: str) -> MaterialProps:
    """Look up material by ASME spec number."""
    if spec in MATERIAL_DB:
        return MATERIAL_DB[spec]
    # Try case-insensitive match
    for key in MATERIAL_DB:
        if key.upper() == spec.upper():
            return MATERIAL_DB[key]
    raise ValueError(
        f"Material '{spec}' not found. Available: {list(MATERIAL_DB.keys())}"
    )


def list_materials() -> list[str]:
    """Return list of available material spec numbers."""
    return sorted(MATERIAL_DB.keys())


def tube_wall_thickness(
    D_o: float,
    P_design: float,      # Design pressure [Pa]
    S: float,              # Allowable stress [Pa]
    C_a: float = 0.0,      # Corrosion allowance [m]
    E_j: float = 1.0,      # Joint efficiency (1.0 for seamless)
) -> float:
    """Minimum tube wall thickness per ASME TEMA rules.

    t = (P * D_o) / (2 * S * E_j + P) + C_a
    """
    denominator = 2 * S * E_j + P_design
    if denominator <= 0:
        return 0.005  # default 5mm
    t_min = (P_design * D_o) / denominator + C_a
    return max(t_min, 0.001)  # minimum 1mm
