"""Fouling trend predictor for heat exchangers.

Estimates fouling resistance over time based on:
  - Fluid type (crude oil, cooling water, process streams)
  - Temperature and velocity conditions
  - Time-based fouling growth model

References:
  - TEMA Standards, 10th Ed. (2019), Table RGP-T-2.4-2: Typical fouling
    resistances for various fluid services (seawater, river water, crude oil,
    steam, etc.)
  - Kern, D.Q. & Seaton, R.E., "A Theoretical Analysis of Thermal Surface
    Fouling", British Chemical Engineering, Vol. 4, No. 5, 1959, pp. 258-262.
    Asymptotic fouling model: Rf(t) = Rf* * (1 - exp(-t/tau))
  - Epstein, N., "Fouling in Heat Exchangers", Heat Transfer 1978, Vol. 1,
    Hemisphere Publishing, 1978. (fouling mechanism classification)
  - Somerscales, E.F.C., "Fouling of Heat Exchangers", in Handbook of Heat
    Exchanger Design, Hewitt et al. (Eds.), Hemisphere, 1990. (velocity and
    temperature correction factors)

Fouling model details:
  1. Kern-Seaton asymptotic model: Rf(t) = Rf_star * (1 - exp(-t/tau))
     - tau = time constant [years], typically 1-3 years
     - Rf_star = asymptotic fouling resistance [m2K/W]
  2. Velocity correction: v_correction = max(0.3, min(2.0, 1/v^0.5))
     Higher velocity reduces fouling deposition (Kern & Seaton, 1959)
  3. Temperature correction (hydrocarbons only):
     T_correction = 1 + 0.002*(T - T_ref), T_ref = 350 K
     Higher temperature increases coking/polymerization (Epstein, 1978)
"""

from __future__ import annotations

import math
from dataclasses import dataclass


# TEMA recommended fouling resistances [m2K/W]
TEMA_FOULING: dict[str, dict] = {
    "cooling_water (treated)": {
        "Rf": 1.76e-4,
        "description": "Treated cooling water (river, lake)",
        "fouling_rate_per_year": 0.00005,  # m2K/W per year of growth
    },
    "cooling_water (untreated)": {
        "Rf": 3.52e-4,
        "description": "Untreated cooling water (river, lake)",
        "fouling_rate_per_year": 0.0001,
    },
    "cooling_water (sea)": {
        "Rf": 1.76e-4,
        "description": "Seawater",
        "fouling_rate_per_year": 0.00008,
    },
    "steam": {
        "Rf": 8.8e-5,
        "description": "Clean steam",
        "fouling_rate_per_year": 0.00002,
    },
    "crude oil": {
        "Rf": 3.52e-4,
        "description": "Crude oil (whole crude)",
        "fouling_rate_per_year": 0.00015,
    },
    "heavy fuel oil": {
        "Rf": 8.8e-4,
        "description": "Heavy fuel oil, residuum",
        "fouling_rate_per_year": 0.0004,
    },
    "light hydrocarbons": {
        "Rf": 1.76e-4,
        "description": "Light hydrocarbons, gasoline, naphtha",
        "fouling_rate_per_year": 0.00005,
    },
    "gas natural": {
        "Rf": 1.76e-4,
        "description": "Natural gas, refinery gas",
        "fouling_rate_per_year": 0.00003,
    },
    "amine solutions": {
        "Rf": 1.76e-4,
        "description": "MEA, DEA amine solutions",
        "fouling_rate_per_year": 0.00006,
    },
    "glycol solutions": {
        "Rf": 1.76e-4,
        "description": "Ethylene glycol, propylene glycol",
        "fouling_rate_per_year": 0.00004,
    },
}


@dataclass
class FoulingResult:
    """Fouling prediction result."""
    Rf_design: float          # Design fouling resistance [m2K/W]
    Rf_predicted: float       # Predicted Rf at time t [m2K/W]
    time_years: float         # Time elapsed [years]
    U_clean: float            # U without fouling [W/m2K]
    U_fouled: float           # U with fouling [W/m2K]
    U_minimum: float          # Minimum acceptable U [W/m2K]
    fouling_margin: float     # Remaining margin before cleaning needed [W/m2K]
    cleaning_interval: float  # Estimated cleaning interval [years]
    description: str          # Fouling fluid description


def kern_seaton_fouling_model(
    Rf_star: float,           # Asymptotic (maximum) fouling resistance [m2K/W]
    time_years: float,        # Operating time [years]
    time_constant: float = 1.0,  # Fouling time constant [years]
) -> float:
    """Kern-Seaton asymptotic fouling model.

    Rf(t) = Rf_star * (1 - exp(-t / tau))

    As Rf approaches Rf_star, fouling slows and eventually stops.
    """
    if time_years <= 0:
        return 0.0
    return Rf_star * (1 - math.exp(-time_years / time_constant))


def predict_fouling(
    fouling_fluid: str = "cooling_water (treated)",
    Rf_design: float = 1.76e-4,
    time_years: float = 5.0,
    U_clean: float = 2000.0,
    U_minimum: float = 500.0,
    velocity_tube: float = 1.0,
    temperature: float = 350.0,
    custom_Rf: float | None = None,
) -> FoulingResult:
    """Predict fouling resistance and remaining life.

    Parameters
    ----------
    fouling_fluid : Key from TEMA_FOULING
    Rf_design     : Design fouling resistance [m2K/W]
    time_years    : Time to evaluate
    U_clean       : U without any fouling [W/m2K]
    U_minimum     : Minimum acceptable U before cleaning [W/m2K]
    velocity_tube : Tube-side velocity [m/s]
    temperature   : Fluid temperature [K]
    custom_Rf     : If given, override TEMA Rf with this value [m2K/W]
    """
    info = TEMA_FOULING.get(fouling_fluid, {
        "Rf": 1.76e-4,
        "description": "Unknown fluid",
        "fouling_rate_per_year": 0.0001,
    })

    Rf_star = custom_Rf if custom_Rf is not None else info["Rf"]
    fouling_rate = info["fouling_rate_per_year"]

    # Velocity correction: higher velocity reduces fouling
    v_correction = max(0.3, min(2.0, 1.0 / (velocity_tube**0.5)))

    # Temperature correction: higher T increases fouling for hydrocarbons
    T_ref = 350.0  # reference temperature
    T_correction = 1.0 + 0.002 * (temperature - T_ref) if "crude" in fouling_fluid or "oil" in fouling_fluid else 1.0

    # Adjusted Rf_star
    Rf_star_adj = Rf_star * v_correction * T_correction

    # Predict Rf at time t
    tau = 2.0  # time constant (years)
    Rf_predicted = kern_seaton_fouling_model(Rf_star_adj, time_years, tau)

    # U with fouling
    # 1/U_fouled = 1/U_clean + Rf
    U_fouled = 1.0 / (1.0 / U_clean + Rf_predicted) if U_clean > 0 else 0.0

    # Fouling margin
    fouling_margin = U_fouled - U_minimum

    # Cleaning interval: when U drops to U_minimum
    Rf_limit = 1.0 / U_minimum - 1.0 / U_clean if U_clean > U_minimum else 0.0
    if Rf_limit > 0:
        # Invert Kern-Seaton: t = -tau * ln(1 - Rf_limit / Rf_star_adj)
        ratio = Rf_limit / Rf_star_adj if Rf_star_adj > 0 else 0
        if 0 < ratio < 1:
            cleaning_interval = -tau * math.log(1 - ratio)
        else:
            cleaning_interval = 20.0  # no fouling limit reached
    else:
        cleaning_interval = 20.0

    return FoulingResult(
        Rf_design=Rf_design,
        Rf_predicted=Rf_predicted,
        time_years=time_years,
        U_clean=U_clean,
        U_fouled=U_fouled,
        U_minimum=U_minimum,
        fouling_margin=fouling_margin,
        cleaning_interval=cleaning_interval,
        description=info["description"],
    )
