"""Cost optimization model for heat exchanger design.

Estimates CAPEX (capital expenditure) and OPEX (operating expenditure)
to find the economically optimal HX configuration.

Cost models based on:
  - Peters, M.S. & Timmerhaus, K.D., "Plant Design and Economics for
    Chemical Engineers", 4th Ed., McGraw-Hill, 1991. (Lang factor method,
    factorial cost estimation, equipment costing)
  - Turton, R. et al., "Analysis, Synthesis and Design of Chemical
    Processes", 4th Ed., Prentice Hall, 2012. (CAPEX estimation, pump
    cost models, maintenance factors)
  - Couper, J.R. et al., "Chemical Process Equipment: Selection and
    Design", 3rd Ed., Elsevier, 2012. (equipment sizing and cost curves)
  - Kern, D.Q., "Process Heat Transfer", McGraw-Hill, 1950. (Lang factor
    for shell-and-tube: 3.1-4.0 range; used 3.5 as representative value)
  - Ulrich, G.D., "A Guide to Chemical Engineering Process Design and
    Economics", Wiley, 1984. (maintenance cost: 3-5% of CAPEX/year)

Formulas used:
  CAPEX = bare_cost * Lang_factor
    where bare_cost = tube_cost + shell_cost + baffle_cost + nozzle_cost
    Lang_factor = 3.5 (Kern, 1950; typical for shell-and-tube)

  Pumping_power = m_dot * dP / (rho * eta)
    Ref: Turton et al. (2012), Ch. 6; also Incropera & DeWitt, "Fundamentals
    of Heat and Mass Transfer", 7th Ed., Ch. 8 (Darcy-Weisbach dP).

  OPEX = energy_cost + maintenance_cost
    energy_cost = total_pumping_power * operating_hours * electricity_price
    maintenance_cost = CAPEX * maintenance_pct (3% typical, Ulrich 1984)

  Lifecycle_cost = CAPEX + lifetime * OPEX
    Ref: Peters & Timmerhaus (1991), Ch. 6; Turton et al. (2012), Ch. 14.

  cost_per_m2 = CAPEX / heat_transfer_area
  cost_per_kw  = CAPEX / heat_duty_kW
    Typical shell-and-tube: $50-200/m2 (carbon steel), $150-500/m2 (stainless),
    $500-2000/m2 (exotic alloys). Ref: Couper et al. (2012), Table 12.1.

"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class CostResult:
    """Heat exchanger cost analysis result."""
    # Capital costs
    tube_cost: float           # Tube material cost [USD]
    shell_cost: float          # Shell/fabrication cost [USD]
    baffle_cost: float         # Baffle and support cost [USD]
    nozzle_cost: float         # Nozzle and flange cost [USD]
    total_capex: float         # Total capital cost [USD]
    # Operating costs
    pumping_power_tube: float  # Tube-side pumping power [W]
    pumping_power_shell: float # Shell-side pumping power [W]
    total_pumping_power: float # Total pumping power [W]
    annual_energy_cost: float  # Annual electricity cost [USD/year]
    annual_maintenance: float  # Annual maintenance cost [USD/year]
    total_annual_opex: float   # Total annual OPEX [USD/year]
    # Lifecycle
    lifetime_years: float      # Design life [years]
    total_lifecycle_cost: float  # CAPEX + lifetime * OPEX [USD]
    # Metrics
    cost_per_m2: float         # Capital cost per m2 of area [USD/m2]
    cost_per_kw: float         # Capital cost per kW of duty [USD/kW]


def estimate_capex(
    # Geometry
    D_o: float,
    D_shell: float,
    L: float,
    N_tubes: int,
    N_baffles: int,
    # Material
    material_cost_per_kg: float = 5.0,
    tube_density: float = 8000,
    shell_density: float = 7850,
    # Additional
    N_nozzles: int = 4,
    nozzle_diameter: float = 0.1,
    currency_factor: float = 1.0,  # adjustment factor
) -> CostResult:
    """Estimate capital and operating costs for a shell-and-tube HX.

    Uses weighted factorial cost method (Lang factor approach).
    """
    # Tube volume and mass
    A_tube_wall = math.pi / 4 * (D_o**2 - (D_o - 0.004)**2)  # ~4mm wall
    V_tube = A_tube_wall * L * N_tubes
    m_tube = V_tube * tube_density

    # Shell volume and mass (cylindrical shell)
    t_shell = max(0.005, D_shell * 0.02)  # ~2% of diameter
    V_shell = math.pi * D_shell * t_shell * L
    m_shell = V_shell * shell_density

    # Baffle mass
    m_baffles = N_baffles * math.pi / 4 * D_shell**2 * 0.006  # 6mm thick

    # Nozzle cost (estimate)
    m_nozzles = N_nozzles * 0.5  # ~0.5 kg each

    # Material costs
    tube_cost = m_tube * material_cost_per_kg * currency_factor
    shell_cost = m_shell * 3.0 * currency_factor  # fabrication factor ~3x
    baffle_cost = m_baffles * 2.5 * currency_factor
    nozzle_cost = m_nozzles * 4.0 * currency_factor

    # Total bare cost
    bare_cost = tube_cost + shell_cost + baffle_cost + nozzle_cost

    # Lang factor for shell-and-tube: typically 3.1–4.0
    # Includes installation, piping, instrumentation, etc.
    lang_factor = 3.5
    total_capex = bare_cost * lang_factor

    return CostResult(
        tube_cost=tube_cost,
        shell_cost=shell_cost,
        baffle_cost=baffle_cost,
        nozzle_cost=nozzle_cost,
        total_capex=total_capex,
        pumping_power_tube=0.0,
        pumping_power_shell=0.0,
        total_pumping_power=0.0,
        annual_energy_cost=0.0,
        annual_maintenance=0.0,
        total_annual_opex=0.0,
        lifetime_years=20.0,
        total_lifecycle_cost=total_capex,
        cost_per_m2=0.0,
        cost_per_kw=0.0,
    )


def full_cost_analysis(
    # Geometry
    D_o: float, D_i: float, D_shell: float,
    L: float, N_tubes: int, N_baffles: int,
    # Performance
    q_duty: float,           # Heat duty [W]
    A_surface: float,        # Heat transfer area [m^2]
    dp_tube: float,          # Tube dP [Pa]
    dp_shell: float,         # Shell dP [Pa]
    m_dot_tube: float,       # Tube mass flow [kg/s]
    m_dot_shell: float,      # Shell mass flow [kg/s]
    # Material
    material_cost_per_kg: float = 5.0,
    tube_density: float = 8000,
    shell_density: float = 7850,
    # Operating parameters
    electricity_cost: float = 0.08,  # USD/kWh
    operating_hours: float = 8000,   # hours/year
    pump_efficiency: float = 0.75,
    lifetime_years: float = 20.0,
    maintenance_pct: float = 0.03,   # % of CAPEX/year
) -> CostResult:
    """Full cost analysis including CAPEX, OPEX, and lifecycle cost."""
    # CAPEX
    capex = estimate_capex(
        D_o, D_shell, L, N_tubes, N_baffles,
        material_cost_per_kg, tube_density, shell_density,
    )

    # Pumping power: P = m_dot * dP / (rho * eta)
    rho_tube = 1000.0  # approximate
    rho_shell = 1000.0

    P_tube = m_dot_tube * dp_tube / (rho_tube * pump_efficiency) if rho_tube > 0 else 0
    P_shell = m_dot_shell * dp_shell / (rho_shell * pump_efficiency) if rho_shell > 0 else 0
    total_power = P_tube + P_shell

    # Annual energy cost
    annual_energy = total_power * operating_hours * electricity_cost / 1000  # kWh -> USD

    # Annual maintenance
    annual_maint = capex.total_capex * maintenance_pct

    total_opex = annual_energy + annual_maint

    # Lifecycle
    lifecycle = capex.total_capex + lifetime_years * total_opex

    # Per-unit metrics
    cost_per_m2 = capex.total_capex / A_surface if A_surface > 0 else 0
    cost_per_kw = capex.total_capex / (q_duty / 1000) if q_duty > 0 else 0

    return CostResult(
        tube_cost=capex.tube_cost,
        shell_cost=capex.shell_cost,
        baffle_cost=capex.baffle_cost,
        nozzle_cost=capex.nozzle_cost,
        total_capex=capex.total_capex,
        pumping_power_tube=P_tube,
        pumping_power_shell=P_shell,
        total_pumping_power=total_power,
        annual_energy_cost=annual_energy,
        annual_maintenance=annual_maint,
        total_annual_opex=total_opex,
        lifetime_years=lifetime_years,
        total_lifecycle_cost=lifecycle,
        cost_per_m2=cost_per_m2,
        cost_per_kw=cost_per_kw,
    )
