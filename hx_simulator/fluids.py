"""Built-in fluid property tables and interpolation.

Properties sourced from Incropera & DeWitt, Tables A-4 (air at 1 atm),
A-5 (saturated liquid water), A-6 (engine oil).
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class FluidProperties:
    """Container for thermophysical properties at a given temperature."""
    T: float          # Temperature [K]
    rho: float        # Density [kg/m^3]
    mu: float         # Dynamic viscosity [Pa.s]
    Cp: float         # Specific heat [J/(kg.K)]
    k: float          # Thermal conductivity [W/(m.K)]
    Pr: float         # Prandtl number [-]
    nu: float = 0.0   # Kinematic viscosity [m^2/s]

    def __post_init__(self):
        if self.nu == 0.0 and self.rho > 0:
            self.nu = self.mu / self.rho


# ---------------------------------------------------------------------------
# Property tables  —  [T_K, rho, mu, Cp, k, Pr]
# ---------------------------------------------------------------------------

# Water (saturated liquid) — Incropera & DeWitt Table A-5
WATER_TABLE: list[list[float]] = [
    # T[K]    rho     mu         Cp       k         Pr
    [273.15, 1000.0, 1.787e-3, 4217.0, 0.569, 13.25],
    [280.0,   1000.0, 1.422e-3, 4198.0, 0.578, 10.26],
    [285.0,   1000.0, 1.225e-3, 4189.0, 0.583,  8.81],
    [290.0,    999.0, 1.080e-3, 4184.0, 0.590,  7.67],
    [295.0,    998.0, 0.959e-3, 4181.0, 0.598,  6.72],
    [300.0,    997.0, 0.855e-3, 4179.0, 0.606,  5.89],
    [305.0,    995.0, 0.769e-3, 4178.0, 0.613,  5.21],
    [310.0,    993.0, 0.695e-3, 4178.0, 0.620,  4.62],
    [315.0,    991.0, 0.631e-3, 4178.0, 0.628,  4.16],
    [320.0,    989.0, 0.577e-3, 4179.0, 0.634,  3.77],
    [325.0,    987.0, 0.528e-3, 4180.0, 0.640,  3.42],
    [330.0,    984.0, 0.489e-3, 4182.0, 0.645,  3.15],
    [335.0,    982.0, 0.453e-3, 4184.0, 0.650,  2.88],
    [340.0,    979.0, 0.420e-3, 4186.0, 0.656,  2.66],
    [345.0,    977.0, 0.391e-3, 4188.0, 0.660,  2.46],
    [350.0,    974.0, 0.364e-3, 4191.0, 0.664,  2.29],
    [355.0,    971.0, 0.340e-3, 4195.0, 0.668,  2.14],
    [360.0,    968.0, 0.317e-3, 4199.0, 0.671,  1.99],
    [365.0,    965.0, 0.297e-3, 4203.0, 0.674,  1.86],
    [370.0,    962.0, 0.279e-3, 4209.0, 0.677,  1.76],
    [373.15,   958.0, 0.265e-3, 4217.0, 0.679,  1.66],
]

# Air at 1 atm — Incropera & DeWitt Table A-4
AIR_TABLE: list[list[float]] = [
    # T[K]    rho      mu          Cp       k          Pr
    [250.0,  1.4128,  1.5960e-5,  1006.0,  0.02211,  0.7296],
    [260.0,  1.3609,  1.6480e-5,  1006.0,  0.02288,  0.7262],
    [270.0,  1.3125,  1.6980e-5,  1006.0,  0.02362,  0.7228],
    [280.0,  1.2683,  1.7460e-5,  1007.0,  0.02434,  0.7202],
    [290.0,  1.2277,  1.7920e-5,  1007.0,  0.02504,  0.7176],
    [300.0,  1.1614,  1.8460e-5,  1007.0,  0.02624,  0.7070],
    [310.0,  1.1281,  1.8920e-5,  1007.0,  0.02693,  0.7046],
    [320.0,  1.0969,  1.9370e-5,  1008.0,  0.02761,  0.7024],
    [325.0,  1.0821,  1.9580e-5,  1008.0,  0.02794,  0.7013],
    [330.0,  1.0667,  1.9820e-5,  1008.0,  0.02827,  0.7004],
    [340.0,  1.0375,  2.0250e-5,  1009.0,  0.02892,  0.6986],
    [350.0,  1.0087,  2.0820e-5,  1009.0,  0.02973,  0.6980],
    [360.0,  0.9834,  2.1180e-5,  1010.0,  0.03039,  0.6968],
    [370.0,  0.9563,  2.1620e-5,  1010.0,  0.03104,  0.6959],
    [380.0,  0.9316,  2.2040e-5,  1011.0,  0.03169,  0.6949],
    [390.0,  0.9084,  2.2470e-5,  1011.0,  0.03233,  0.6942],
    [400.0,  0.8711,  2.2860e-5,  1012.0,  0.03365,  0.6896],
    [450.0,  0.7739,  2.4840e-5,  1020.0,  0.03707,  0.6841],
    [500.0,  0.6964,  2.6710e-5,  1029.0,  0.04028,  0.6834],
    [550.0,  0.6331,  2.8480e-5,  1038.0,  0.04334,  0.6824],
    [600.0,  0.5804,  3.0180e-5,  1047.0,  0.04628,  0.6814],
]

# Engine Oil (unused liquid) — Incropera & DeWitt Table A-6
OIL_TABLE: list[list[float]] = [
    # T[K]    rho      mu          Cp       k          Pr
    [293.0,  888.0,   0.800,      1880.0,  0.1450,   10400.0],
    [300.0,  884.0,   0.550,      1900.0,  0.1440,    7250.0],
    [305.0,  881.0,   0.440,      1910.0,  0.1435,    5880.0],
    [310.0,  878.0,   0.365,      1920.0,  0.1430,    4930.0],
    [315.0,  875.0,   0.310,      1930.0,  0.1425,    4210.0],
    [320.0,  872.0,   0.266,      1940.0,  0.1420,    3640.0],
    [325.0,  869.0,   0.230,      1950.0,  0.1415,    3180.0],
    [330.0,  866.0,   0.201,      1960.0,  0.1410,    2790.0],
    [340.0,  860.0,   0.156,      1990.0,  0.1400,    2220.0],
    [350.0,  854.0,   0.124,      2010.0,  0.1390,    1800.0],
    [360.0,  848.0,   0.101,      2040.0,  0.1380,    1490.0],
    [370.0,  842.0,   0.0836,     2070.0,  0.1370,    1250.0],
    [380.0,  836.0,   0.0702,     2100.0,  0.1360,    1080.0],
    [390.0,  830.0,   0.0596,     2130.0,  0.1350,     940.0],
    [400.0,  824.0,   0.0511,     2160.0,  0.1340,     825.0],
    [410.0,  818.0,   0.0441,     2190.0,  0.1330,     725.0],
    [420.0,  812.0,   0.0384,     2220.0,  0.1320,     641.0],
    [430.0,  806.0,   0.0337,     2250.0,  0.1310,     571.0],
    [440.0,  800.0,   0.0298,     2280.0,  0.1300,     514.0],
    [450.0,  794.0,   0.0266,     2310.0,  0.1290,     466.0],
]

# Mapping from user-friendly names to tables
FLUID_TABLES: dict[str, list[list[float]]] = {
    "water": WATER_TABLE,
    "air": AIR_TABLE,
    "oil": OIL_TABLE,
    "engine_oil": OIL_TABLE,
}


def _interp_property(T: float, table: list[list[float]], col: int) -> float:
    """Linear interpolation of a single property column from a table.

    table rows: [T, rho, mu, Cp, k, Pr]
    col: column index (1=rho, 2=mu, 3=Cp, 4=k, 5=Pr)
    """
    n = len(table)
    if T <= table[0][0]:
        return table[0][col]
    if T >= table[-1][0]:
        return table[-1][col]
    for i in range(n - 1):
        T0, T1 = table[i][0], table[i + 1][0]
        if T0 <= T <= T1:
            frac = (T - T0) / (T1 - T0)
            return table[i][col] + frac * (table[i + 1][col] - table[i][col])
    return table[-1][col]


def get_properties(fluid: str, T: float) -> FluidProperties:
    """Get interpolated thermophysical properties for a fluid at temperature T [K].

    Parameters
    ----------
    fluid : str   Name: 'water', 'air', 'oil'/'engine_oil'
    T     : float Temperature in Kelvin

    Returns
    -------
    FluidProperties dataclass with rho, mu, Cp, k, Pr, nu
    """
    key = fluid.lower().strip()
    if key not in FLUID_TABLES:
        raise ValueError(
            f"Unknown fluid '{fluid}'. Available: {list(FLUID_TABLES.keys())}"
        )
    table = FLUID_TABLES[key]
    T_clamped = max(table[0][0], min(T, table[-1][0]))

    rho = _interp_property(T_clamped, table, 1)
    mu  = _interp_property(T_clamped, table, 2)
    Cp  = _interp_property(T_clamped, table, 3)
    k   = _interp_property(T_clamped, table, 4)
    Pr_val = _interp_property(T_clamped, table, 5)
    nu  = mu / rho if rho > 0 else 0.0

    return FluidProperties(T=T_clamped, rho=rho, mu=mu, Cp=Cp, k=k, Pr=Pr_val, nu=nu)


def get_beta_air(T: float) -> float:
    """Volumetric thermal expansion coefficient for air (ideal gas: beta = 1/T)."""
    return 1.0 / T


def get_beta_water(T: float) -> float:
    """Approximate beta for liquid water [K^-1] near room temperature."""
    # From data: beta ~ 2.07e-4 at 300K, increases with T
    # Polynomial fit: beta ≈ -0.000001*(T-273) + 0.000005*(T-273) + 0.000207 (rough)
    # Simplified linear fit from standard tables
    return 2.07e-4 * (T / 300.0) ** 1.5


def get_h_fg_water(T: float) -> float:
    """Latent heat of vaporisation for water [J/kg] at temperature T [K].

    Empirical: h_fg ≈ 2.501e6 - 2366*(T - 273.15)  [J/kg]
    """
    T_C = T - 273.15
    return 2_501_000.0 - 2366.0 * T_C


def get_sigma_water(T: float) -> float:
    """Surface tension of water [N/m] at temperature T [K].

    Empirical: sigma ≈ 0.0727 - 0.000155*(T - 293)  [N/m]
    """
    T_K_ref = 293.15
    return max(0.0, 0.0727 - 0.000155 * (T - T_K_ref))


# ---------------------------------------------------------------------------
# Custom fluid builder
# ---------------------------------------------------------------------------

def make_custom_fluid(rho: float, mu: float, Cp: float, k: float,
                      Pr_val: float | None = None) -> FluidProperties:
    """Create a FluidProperties object from user-supplied values.

    If Pr is not given, it is computed from mu*Cp/k.
    T is set to 0 (unknown reference).
    """
    if Pr_val is None:
        Pr_val = mu * Cp / k
    nu = mu / rho if rho > 0 else 0.0
    return FluidProperties(T=0.0, rho=rho, mu=mu, Cp=Cp, k=k, Pr=Pr_val, nu=nu)
