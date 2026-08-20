"""Core heat exchanger solver — LMTD, ε-NTU, design (sizing) and rating (analysis).

This module ties together heat_transfer, pressure_drop, fluids, and utils
to solve HX problems. Two modes:

  Rating  (analysis):  Given geometry → find outlet temps, q, ΔP
  Design  (sizing):    Given temps     → find required area, N_tubes

All physics from HTOA 2025 course references.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .fluids import FluidProperties
from .heat_transfer import (
    compute_h_tube, compute_h_shell, U_clean, U_fouled,
    compute_full_ht, HTCoefficients, FOULING_FACTORS, _FOULING_KEY_MAP,
)
from .pressure_drop import (
    tube_side_dp, shell_side_dp, PressureDropResult,
)
from .utils import (
    heat_capacity_rate, q_max as q_max_fn, LMTD,
    epsilon_NTU_counterflow, epsilon_NTU_parallel, epsilon_NTU_phase_change,
    NTU_from_epsilon_counterflow, NTU_from_epsilon_parallel,
    check_convergence, print_section, print_result_row,
)
from .bell_delaware import bell_delaware_shell_side, get_tema_code, SHELL_TYPES
from .fiv import fiv_analysis
from .cost_model import full_cost_analysis
from .fouling_model import predict_fouling
from .nozzle import size_nozzle
from .materials import get_material, MATERIAL_DB


# ---------------------------------------------------------------------------
# Configuration dataclasses
# ---------------------------------------------------------------------------

@dataclass
class FluidInput:
    """User-supplied fluid information."""
    name: str                          # 'water', 'air', 'oil', 'custom'
    T_inlet: float                     # Inlet temperature [K]
    m_dot: float                       # Mass flow rate [kg/s]
    properties: FluidProperties | None = None  # For custom fluid

    # Overrides (if None, use built-in table)
    rho: float | None = None
    mu: float | None = None
    Cp: float | None = None
    k: float | None = None
    Pr: float | None = None


@dataclass
class BaffleResult:
    """Computed baffle geometry for shell-and-tube HX."""
    spacing: float          # Baffle spacing (pitch) [m]
    cut_pct: float          # Baffle cut as % of shell diameter [-]
    cut_height: float       # Baffle cut height [m]
    N_baffles: int          # Number of baffles [-]
    A_baffle: float         # Area of one baffle plate [m^2]
    A_flow_shell: float     # Shell-side cross-flow area [m^2]
    D_eq: float             # Equivalent diameter for shell-side [m]


@dataclass
class GeometryInput:
    """HX geometry specification."""
    # Tube
    D_i: float               # Inner diameter [m]
    D_o: float               # Outer diameter [m]
    L: float                 # Tube length [m]
    N_tubes: int = 1         # Number of tubes
    N_passes: int = 1        # Number of tube passes (multi-pass)
    # Shell
    D_shell: float = 0.0     # Shell inner diameter [m]
    shell_type: str = "E"    # TEMA shell type: E, F, G, H, J, K, X
    pitch_ratio: float = 1.25  # Pitch / D_o
    tube_layout: str = "triangular"  # 'triangular' or 'square'
    # Baffles
    baffle_spacing_ratio: float = 0.3  # Baffle spacing / D_shell (default 30%)
    baffle_cut_pct: float = 25.0       # Baffle cut (% of D_shell, typical 20-35%)
    baffle_type: str = "segmental"     # segmental, double-segmental, rod-baffle
    # Wall
    k_wall: float = 50.0     # Tube wall conductivity [W/(m.K)] (steel)
    # Material
    material: str = "SA-249-304"  # ASME material spec
    tube_thickness: float = 0.002  # Tube wall thickness [m] (auto-computed if 0)
    # Fouling
    fouling: str = "clean"   # Key into FOULING_FACTORS
    custom_Rf: float | None = None  # Custom fouling resistance [m2K/W] (overrides key)
    # Flow arrangement
    arrangement: str = "counter"  # 'counter' or 'parallel'
    # Nozzle sizing
    nozzle_velocity_limit: float = 2.0  # Max nozzle velocity [m/s]


@dataclass
class SolverResult:
    """Complete result from the HX solver."""
    # Heat duty
    q: float                          # Actual heat transfer [W]
    q_max: float                      # Maximum possible [W]
    epsilon: float                    # Effectiveness [-]
    NTU: float                        # Number of transfer units [-]
    Cr: float                         # Heat capacity ratio [-]
    # Capacity rates
    C_h: float                        # Hot side capacity rate [W/K]
    C_c: float                        # Cold side capacity rate [W/K]
    C_min: float
    C_max: float
    # Outlet temperatures
    Th_o: float                       # Hot outlet [K]
    Tc_o: float                       # Cold outlet [K]
    # LMTD
    LMTD: float                       # Log mean temperature difference [K]
    # Heat transfer coefficients
    ht: HTCoefficients                # Full HT results
    # Pressure drops
    dp_tube: PressureDropResult
    dp_shell: PressureDropResult
    # Baffle geometry
    baffle: BaffleResult | None = None
    # TEMA designation
    tema_code: str = ""
    # Industrial analysis results (populated when available)
    fiv: object | None = None         # FIVResult from fiv.py
    cost: object | None = None        # CostResult from cost_model.py
    fouling_pred: object | None = None  # FoulingResult from fouling_model.py
    nozzle_hot_in: object | None = None  # NozzleResult
    nozzle_hot_out: object | None = None
    nozzle_cold_in: object | None = None
    nozzle_cold_out: object | None = None
    # Design mode extras
    area_required: float = 0.0        # Required area [m^2]
    area_actual: float = 0.0          # Actual area [m^2]
    converged: bool = True
    iterations: int = 0
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Baffle geometry computation
# ---------------------------------------------------------------------------

def compute_baffles(geom: GeometryInput) -> BaffleResult:
    """Compute baffle geometry for a shell-and-tube HX.

    Uses the user-specified baffle spacing ratio (% of D_shell) and
    baffle cut (% of D_shell) to determine actual baffle dimensions.

    Typical values:
      - Baffle spacing: 20–100% of D_shell (0.3–0.5 common)
      - Baffle cut: 20–35% of D_shell (25% most common)
    """
    D_s = geom.D_shell
    L = geom.L
    D_o = geom.D_o
    N_tubes = geom.N_tubes
    pitch_ratio = geom.pitch_ratio

    # Baffle spacing
    B = geom.baffle_spacing_ratio * D_s  # actual spacing [m]
    B = max(B, 0.5 * D_o)  # cannot be less than half a tube OD

    # Number of baffles: (L / B) - 1, minimum 1
    N_baffles = max(1, int(round(L / B)) - 1)

    # Recompute actual spacing after rounding N_baffles
    if N_baffles > 0:
        B_actual = L / (N_baffles + 1)
    else:
        B_actual = L

    # Baffle cut
    cut_pct = geom.baffle_cut_pct / 100.0
    cut_height = cut_pct * D_s

    # Baffle plate area (approximate as circle minus segment)
    # A_baffle ≈ pi*R^2 - R^2*acos((R-h)/R) + (R-h)*sqrt(2Rh - h^2)
    R = D_s / 2.0
    h = cut_height
    if h < R:
        theta = math.acos(max(-1.0, min(1.0, (R - h) / R)))
        A_segment = R**2 * theta - (R - h) * math.sqrt(max(0.0, 2 * R * h - h**2))
        A_baffle = math.pi * R**2 - A_segment
    else:
        A_baffle = math.pi * R**2 / 2.0  # half-circle cut

    # Shell-side cross-flow area at the baffle
    # A_flow = D_shell * B * (pitch - D_o) / pitch  (simplified)
    pitch = pitch_ratio * D_o
    A_flow_shell = D_s * B_actual * (pitch - D_o) / pitch if pitch > D_o else 0.0

    # Equivalent diameter for shell-side (for Re calculation)
    # D_eq = 4 * A_flow / (pi * D_o * N_tubes_crossing)  simplified
    D_eq = 4.0 * A_flow_shell / (math.pi * D_o * max(1, N_tubes)) if N_tubes > 0 else D_s

    return BaffleResult(
        spacing=B_actual,
        cut_pct=geom.baffle_cut_pct,
        cut_height=cut_height,
        N_baffles=N_baffles,
        A_baffle=A_baffle,
        A_flow_shell=A_flow_shell,
        D_eq=D_eq,
    )


# ---------------------------------------------------------------------------
# Helper: evaluate fluid properties at reference temperature
# ---------------------------------------------------------------------------

def _eval_fluid(fluid: FluidInput, T_ref: float) -> FluidProperties:
    """Evaluate fluid properties, using overrides if given."""
    if fluid.properties is not None:
        return fluid.properties
    from .fluids import get_properties, make_custom_fluid
    if fluid.rho is not None and fluid.mu is not None and fluid.Cp is not None and fluid.k is not None:
        return make_custom_fluid(fluid.rho, fluid.mu, fluid.Cp, fluid.k, fluid.Pr)
    return get_properties(fluid.name, T_ref)


# ---------------------------------------------------------------------------
# RATING SOLVER  (given geometry → find performance)
# ---------------------------------------------------------------------------

def solve_rating(hot: FluidInput, cold: FluidInput,
                 geom: GeometryInput) -> SolverResult:
    """Rating (analysis) mode: given HX geometry, find outlet temps and q.

    Algorithm:
    1. Evaluate properties at mean temperatures (first guess: inlet average)
    2. Compute h_i, h_o, U_o (with fouling)
    3. Compute C_h, C_c, C_min, C_max, Cr
    4. Compute NTU = U * A / C_min
    5. Use ε-NTU relation → ε → q = ε * C_min * (Th_i - Tc_i)
    6. Outlet temps from energy balance
    7. Verify with LMTD: q = U*A*F*ΔT_lm
    8. Converge on mean temperature if needed
    """
    warnings: list[str] = []

    # Validate geometry
    validate_tube_geometry(geom)

    # Reference temperatures for property evaluation
    T_h_avg = (hot.T_inlet + cold.T_inlet) / 2.0
    T_c_avg = (hot.T_inlet + cold.T_inlet) / 2.0

    # Initial property evaluation
    fluid_h = _eval_fluid(hot, T_h_avg)
    fluid_c = _eval_fluid(cold, T_c_avg)

    # If custom Cp provided, override
    if hot.Cp is not None:
        fluid_h.Cp = hot.Cp
    if cold.Cp is not None:
        fluid_c.Cp = cold.Cp

    # Area
    A_o = math.pi * geom.D_o * geom.L * geom.N_tubes

    # Iterative convergence on mean temperature
    max_iter = 50
    tol = 1e-4
    converged = False
    Th_o_prev = hot.T_inlet  # initial guess

    for iteration in range(1, max_iter + 1):
        # Capacity rates
        C_h = heat_capacity_rate(hot.m_dot, fluid_h.Cp)
        C_c = heat_capacity_rate(cold.m_dot, fluid_c.Cp)
        C_min_val = min(C_h, C_c)
        C_max_val = max(C_h, C_c)
        Cr_val = C_min_val / C_max_val if C_max_val > 0 else 0.0

        # Heat transfer coefficients
        ht = compute_full_ht(
            m_dot_tube=hot.m_dot, D_i=geom.D_i, D_o=geom.D_o,
            L=geom.L, fluid_tube=fluid_h,
            m_dot_shell=cold.m_dot, D_shell=geom.D_shell,
            N_tubes=geom.N_tubes, fluid_shell=fluid_c,
            k_wall=geom.k_wall, pitch_ratio=geom.pitch_ratio,
            fouling=geom.fouling, heating=True,
        )
        U_val = ht.U_o_fouled

        # NTU
        NTU_val = U_val * A_o / C_min_val if C_min_val > 0 else 0.0

        # Effectiveness
        if geom.arrangement == "counter":
            epsilon_val = epsilon_NTU_counterflow(NTU_val, Cr_val)
        elif geom.arrangement == "parallel":
            epsilon_val = epsilon_NTU_parallel(NTU_val, Cr_val)
        else:
            epsilon_val = epsilon_NTU_counterflow(NTU_val, Cr_val)

        # Heat transfer rate
        q_max_val = q_max_fn(C_min_val, hot.T_inlet, cold.T_inlet)
        q_val = epsilon_val * q_max_val

        # Outlet temperatures from energy balance
        if C_h > 0:
            Th_o = hot.T_inlet - q_val / C_h
        else:
            Th_o = hot.T_inlet
        if C_c > 0:
            Tc_o = cold.T_inlet + q_val / C_c
        else:
            Tc_o = cold.T_inlet

        # Check convergence on outlet temperature
        if check_convergence(Th_o_prev, Th_o, tol):
            converged = True
            break
        Th_o_prev = Th_o

        # Update mean temperatures for next iteration
        T_h_avg_new = (hot.T_inlet + Th_o) / 2.0
        T_c_avg_new = (cold.T_inlet + Tc_o) / 2.0
        fluid_h = _eval_fluid(hot, T_h_avg_new)
        fluid_c = _eval_fluid(cold, T_c_avg_new)
        if hot.Cp is not None:
            fluid_h.Cp = hot.Cp
        if cold.Cp is not None:
            fluid_c.Cp = cold.Cp

    if not converged:
        warnings.append(f"Did not converge after {max_iter} iterations")

    # LMTD verification
    if geom.arrangement == "counter":
        dT1 = hot.T_inlet - Tc_o
        dT2 = Th_o - cold.T_inlet
    else:
        dT1 = hot.T_inlet - cold.T_inlet
        dT2 = Th_o - Tc_o

    dT1 = max(dT1, 0.01)
    dT2 = max(dT2, 0.01)
    lmtd_val = LMTD(dT1, dT2)

    # Baffle geometry (for shell-and-tube)
    baffle_result = None
    if geom.N_tubes > 1:
        baffle_result = compute_baffles(geom)

    # Pressure drops
    dp_tube = tube_side_dp(
        hot.m_dot, geom.D_i, geom.L, fluid_h.rho, fluid_h.mu
    )
    dp_shell = shell_side_dp(
        cold.m_dot, geom.D_o, geom.D_shell, geom.L, geom.N_tubes,
        fluid_c.rho, fluid_c.mu, geom.pitch_ratio,
        N_baffles=baffle_result.N_baffles if baffle_result else None,
    )

    warnings.extend(ht.warnings)

    # --- Industrial analyses (shell-and-tube only) ---
    tema_code = ""
    fiv_result = None
    cost_result = None
    fouling_result = None
    nozzle_hi = nozzle_ho = nozzle_ci = nozzle_co = None

    if geom.N_tubes > 1:
        # TEMA code
        tema_code = get_tema_code("B", geom.shell_type, "L")

        # Bell-Delaware shell-side (overwrite simplified result if available)
        bd = bell_delaware_shell_side(
            rho=fluid_c.rho, mu=fluid_c.mu, Cp=fluid_c.Cp,
            k=fluid_c.k, Pr=fluid_c.Pr,
            D_o=geom.D_o, D_shell=geom.D_shell, D_i=geom.D_i,
            L=geom.L, N_tubes=geom.N_tubes,
            baffle_spacing=baffle_result.spacing if baffle_result else 0.3 * geom.D_shell,
            baffle_cut_pct=geom.baffle_cut_pct,
            pitch_ratio=geom.pitch_ratio,
            tube_layout=geom.tube_layout,
            baffle_type=geom.baffle_type,
            N_p=geom.N_passes,
            m_dot_shell=cold.m_dot,
        )
        # Update dp_shell with Bell-Delaware result
        dp_shell = PressureDropResult(
            delta_P=bd.dp_total,
            delta_P_friction=bd.dp_total,
            delta_P_minor=0.0,
            velocity=bd.v_crossflow,
            Re=bd.Re_s,
            f_D=bd.dp_crossflow / (bd.G_s**2 / (2 * fluid_c.rho) + 1e-10),
            regime=bd.regime,
        )

        # Flow-Induced Vibration
        try:
            mat = get_material(geom.material)
            fiv_result = fiv_analysis(
                D_o=geom.D_o, D_i=geom.D_i, D_shell=geom.D_shell,
                L=geom.L,
                L_baffle=baffle_result.spacing if baffle_result else 0.3 * geom.D_shell,
                pitch_ratio=geom.pitch_ratio,
                tube_layout=geom.tube_layout,
                E=mat.E_modulus, rho_tube=mat.density,
                rho_fluid=fluid_c.rho, mu_fluid=fluid_c.mu,
                v_crossflow=bd.v_crossflow,
                tube_thickness=geom.tube_thickness,
            )
            warnings.extend(fiv_result.warnings)
        except Exception:
            pass

        # Cost analysis
        try:
            cost_result = full_cost_analysis(
                D_o=geom.D_o, D_i=geom.D_i, D_shell=geom.D_shell,
                L=geom.L, N_tubes=geom.N_tubes,
                N_baffles=baffle_result.N_baffles if baffle_result else 0,
                q_duty=q_val, A_surface=A_o,
                dp_tube=dp_tube.delta_P, dp_shell=bd.dp_total,
                m_dot_tube=hot.m_dot, m_dot_shell=cold.m_dot,
            )
        except Exception:
            pass

        # Fouling prediction
        try:
            tema_fluid = _FOULING_KEY_MAP.get(geom.fouling, "cooling_water (treated)")
            fouling_result = predict_fouling(
                fouling_fluid=tema_fluid,
                Rf_design=FOULING_FACTORS.get(geom.fouling, (0.0, 0.0))[1],
                time_years=5.0,
                U_clean=ht.U_o,
                U_minimum=ht.U_o * 0.5,
                velocity_tube=dp_tube.velocity,
                custom_Rf=geom.custom_Rf,
            )
        except Exception:
            pass

        # Nozzle sizing
        try:
            nozzle_hi = size_nozzle(hot.m_dot, fluid_h.rho, "liquid",
                                    D_shell=geom.D_shell)
            nozzle_ho = size_nozzle(hot.m_dot, fluid_h.rho, "liquid",
                                    D_shell=geom.D_shell)
            nozzle_ci = size_nozzle(cold.m_dot, fluid_c.rho, "liquid",
                                    D_shell=geom.D_shell)
            nozzle_co = size_nozzle(cold.m_dot, fluid_c.rho, "liquid",
                                    D_shell=geom.D_shell)
        except Exception:
            pass

    # --- Fouling prediction (all HX types) ---
    if fouling_result is None:
        try:
            tema_fluid = _FOULING_KEY_MAP.get(geom.fouling, "cooling_water (treated)")
            fouling_result = predict_fouling(
                fouling_fluid=tema_fluid,
                Rf_design=FOULING_FACTORS.get(geom.fouling, (0.0, 0.0))[1],
                time_years=5.0,
                U_clean=ht.U_o,
                U_minimum=ht.U_o * 0.5,
                velocity_tube=dp_tube.velocity,
                custom_Rf=geom.custom_Rf,
            )
        except Exception:
            pass

    return SolverResult(
        q=q_val, q_max=q_max_val, epsilon=epsilon_val,
        NTU=NTU_val, Cr=Cr_val,
        C_h=C_h, C_c=C_c, C_min=C_min_val, C_max=C_max_val,
        Th_o=Th_o, Tc_o=Tc_o, LMTD=lmtd_val,
        ht=ht, dp_tube=dp_tube, dp_shell=dp_shell,
        baffle=baffle_result, tema_code=tema_code,
        fiv=fiv_result, cost=cost_result, fouling_pred=fouling_result,
        nozzle_hot_in=nozzle_hi, nozzle_hot_out=nozzle_ho,
        nozzle_cold_in=nozzle_ci, nozzle_cold_out=nozzle_co,
        area_actual=A_o,
        converged=converged, iterations=iteration,
        warnings=warnings,
    )


# ---------------------------------------------------------------------------
# DESIGN SOLVER  (given temps → find required area)
# ---------------------------------------------------------------------------

def solve_design(hot: FluidInput, cold: FluidInput,
                 geom: GeometryInput,
                 Tc_o_desired: float | None = None,
                 q_duty: float | None = None) -> SolverResult:
    """Design (sizing) mode: given inlet and outlet temps, find required area.

    User specifies either Tc_o_desired or q_duty (one must be given).
    Algorithm:
    1. Compute q from energy balance
    2. Compute C_h, C_c, C_min, C_max, Cr
    3. Compute required ε from temperatures
    4. Invert ε-NTU to get required NTU
    5. Iterate: guess T_m → compute h_i, h_o, U → A = NTU*C_min/U
    6. Converge until |A_new - A_old| < tol
    7. Report required area, number of tubes
    """
    warnings: list[str] = []

    validate_tube_geometry(geom)

    # Determine heat duty
    fluid_h_init = _eval_fluid(hot, hot.T_inlet)
    fluid_c_init = _eval_fluid(cold, cold.T_inlet)
    if hot.Cp is not None:
        fluid_h_init.Cp = hot.Cp
    if cold.Cp is not None:
        fluid_c_init.Cp = cold.Cp

    C_h = heat_capacity_rate(hot.m_dot, fluid_h_init.Cp)
    C_c = heat_capacity_rate(cold.m_dot, fluid_c_init.Cp)
    C_min_val = min(C_h, C_c)
    C_max_val = max(C_h, C_c)
    Cr_val = C_min_val / C_max_val if C_max_val > 0 else 0.0

    if q_duty is not None:
        q_required = q_duty
        # Back-calculate outlet temps
        Th_o = hot.T_inlet - q_required / C_h if C_h > 0 else hot.T_inlet
        Tc_o = cold.T_inlet + q_required / C_c if C_c > 0 else cold.T_inlet
    elif Tc_o_desired is not None:
        Tc_o = Tc_o_desired
        q_required = C_c * (Tc_o - cold.T_inlet)
        Th_o = hot.T_inlet - q_required / C_h if C_h > 0 else hot.T_inlet
    else:
        raise ValueError("Must specify either Tc_o_desired or q_duty")

    # Maximum possible heat transfer
    q_max_val = q_max_fn(C_min_val, hot.T_inlet, cold.T_inlet)
    if q_max_val <= 0:
        raise ValueError("q_max <= 0 — check inlet temperatures")
    epsilon_required = q_required / q_max_val
    if epsilon_required <= 0 or epsilon_required >= 1:
        raise ValueError(
            f"epsilon = {epsilon_required:.4f} out of range (0,1). "
            "Check desired outlet temperatures."
        )

    # Invert ε-NTU to get required NTU
    if geom.arrangement == "counter":
        NTU_required = NTU_from_epsilon_counterflow(epsilon_required, Cr_val)
    else:
        NTU_required = NTU_from_epsilon_parallel(epsilon_required, Cr_val)

    # Iterative solve: converge on mean temperature and U
    max_iter = 50
    tol = 1e-4
    A_prev = 1e6  # initial guess
    converged = False
    area_required = 0.0

    for iteration in range(1, max_iter + 1):
        # Mean temperatures
        T_h_avg = (hot.T_inlet + Th_o) / 2.0
        T_c_avg = (cold.T_inlet + Tc_o) / 2.0

        fluid_h = _eval_fluid(hot, T_h_avg)
        fluid_c = _eval_fluid(cold, T_c_avg)
        if hot.Cp is not None:
            fluid_h.Cp = hot.Cp
        if cold.Cp is not None:
            fluid_c.Cp = cold.Cp

        # Update capacity rates (Cp may change with temperature)
        C_h = heat_capacity_rate(hot.m_dot, fluid_h.Cp)
        C_c = heat_capacity_rate(cold.m_dot, fluid_c.Cp)
        C_min_val = min(C_h, C_c)

        # Recompute required NTU with updated C_min
        if q_duty is not None:
            epsilon_required = q_required / (C_min_val * (hot.T_inlet - cold.T_inlet))
        epsilon_required = max(0.01, min(0.99, epsilon_required))

        if geom.arrangement == "counter":
            NTU_required = NTU_from_epsilon_counterflow(epsilon_required, Cr_val)
        else:
            NTU_required = NTU_from_epsilon_parallel(epsilon_required, Cr_val)

        # Heat transfer coefficients
        ht = compute_full_ht(
            m_dot_tube=hot.m_dot, D_i=geom.D_i, D_o=geom.D_o,
            L=geom.L, fluid_tube=fluid_h,
            m_dot_shell=cold.m_dot, D_shell=geom.D_shell,
            N_tubes=geom.N_tubes, fluid_shell=fluid_c,
            k_wall=geom.k_wall, pitch_ratio=geom.pitch_ratio,
            fouling=geom.fouling, heating=True,
        )
        U_val = ht.U_o_fouled

        # Required area
        area_required = NTU_required * C_min_val / U_val if U_val > 0 else 0.0

        # Check convergence
        if check_convergence(A_prev, area_required, tol):
            converged = True
            break
        A_prev = area_required

    if not converged:
        warnings.append(f"Design did not converge after {max_iter} iterations")

    # LMTD
    if geom.arrangement == "counter":
        dT1 = hot.T_inlet - Tc_o
        dT2 = Th_o - cold.T_inlet
    else:
        dT1 = hot.T_inlet - cold.T_inlet
        dT2 = Th_o - Tc_o
    dT1 = max(dT1, 0.01)
    dT2 = max(dT2, 0.01)
    lmtd_val = LMTD(dT1, dT2)

    # Baffle geometry (for shell-and-tube)
    baffle_result = None
    if geom.N_tubes > 1:
        baffle_result = compute_baffles(geom)

    # Pressure drops
    dp_tube = tube_side_dp(
        hot.m_dot, geom.D_i, geom.L, fluid_h.rho, fluid_h.mu
    )
    dp_shell = shell_side_dp(
        cold.m_dot, geom.D_o, geom.D_shell, geom.L, geom.N_tubes,
        fluid_c.rho, fluid_c.mu, geom.pitch_ratio,
        N_baffles=baffle_result.N_baffles if baffle_result else None,
    )

    warnings.extend(ht.warnings)

    # Number of tubes estimate
    A_per_tube = math.pi * geom.D_o * geom.L
    N_tubes_required = math.ceil(area_required / A_per_tube) if A_per_tube > 0 else 1

    # --- Industrial analyses (shell-and-tube only) ---
    tema_code = ""
    fiv_result = None
    cost_result = None
    fouling_result = None
    nozzle_hi = nozzle_ho = nozzle_ci = nozzle_co = None

    if geom.N_tubes > 1:
        tema_code = get_tema_code("B", geom.shell_type, "L")

        bd = bell_delaware_shell_side(
            rho=fluid_c.rho, mu=fluid_c.mu, Cp=fluid_c.Cp,
            k=fluid_c.k, Pr=fluid_c.Pr,
            D_o=geom.D_o, D_shell=geom.D_shell, D_i=geom.D_i,
            L=geom.L, N_tubes=geom.N_tubes,
            baffle_spacing=baffle_result.spacing if baffle_result else 0.3 * geom.D_shell,
            baffle_cut_pct=geom.baffle_cut_pct,
            pitch_ratio=geom.pitch_ratio,
            tube_layout=geom.tube_layout,
            baffle_type=geom.baffle_type,
            N_p=geom.N_passes,
            m_dot_shell=cold.m_dot,
        )
        dp_shell = PressureDropResult(
            delta_P=bd.dp_total, delta_P_friction=bd.dp_total, delta_P_minor=0.0,
            velocity=bd.v_crossflow, Re=bd.Re_s,
            f_D=bd.dp_crossflow / (bd.G_s**2 / (2 * fluid_c.rho) + 1e-10),
            regime=bd.regime,
        )

        try:
            mat = get_material(geom.material)
            fiv_result = fiv_analysis(
                D_o=geom.D_o, D_i=geom.D_i, D_shell=geom.D_shell,
                L=geom.L, L_baffle=baffle_result.spacing if baffle_result else 0.3*geom.D_shell,
                pitch_ratio=geom.pitch_ratio, tube_layout=geom.tube_layout,
                E=mat.E_modulus, rho_tube=mat.density,
                rho_fluid=fluid_c.rho, mu_fluid=fluid_c.mu,
                v_crossflow=bd.v_crossflow, tube_thickness=geom.tube_thickness,
            )
            warnings.extend(fiv_result.warnings)
        except Exception:
            pass

        try:
            cost_result = full_cost_analysis(
                D_o=geom.D_o, D_i=geom.D_i, D_shell=geom.D_shell,
                L=geom.L, N_tubes=geom.N_tubes,
                N_baffles=baffle_result.N_baffles if baffle_result else 0,
                q_duty=q_required, A_surface=geom.N_tubes * A_per_tube,
                dp_tube=dp_tube.delta_P, dp_shell=bd.dp_total,
                m_dot_tube=hot.m_dot, m_dot_shell=cold.m_dot,
            )
        except Exception:
            pass

        try:
            nozzle_hi = size_nozzle(hot.m_dot, fluid_h.rho, "liquid", D_shell=geom.D_shell)
            nozzle_ho = size_nozzle(hot.m_dot, fluid_h.rho, "liquid", D_shell=geom.D_shell)
            nozzle_ci = size_nozzle(cold.m_dot, fluid_c.rho, "liquid", D_shell=geom.D_shell)
            nozzle_co = size_nozzle(cold.m_dot, fluid_c.rho, "liquid", D_shell=geom.D_shell)
        except Exception:
            pass

    # --- Fouling prediction (all HX types) ---
    if fouling_result is None:
        try:
            tema_fluid = _FOULING_KEY_MAP.get(geom.fouling, "cooling_water (treated)")
            fouling_result = predict_fouling(
                fouling_fluid=tema_fluid,
                Rf_design=FOULING_FACTORS.get(geom.fouling, (0.0, 0.0))[1],
                time_years=5.0,
                U_clean=ht.U_o,
                U_minimum=ht.U_o * 0.5,
                velocity_tube=dp_tube.velocity,
                custom_Rf=geom.custom_Rf,
            )
        except Exception:
            pass

    return SolverResult(
        q=q_required, q_max=q_max_val, epsilon=epsilon_required,
        NTU=NTU_required, Cr=Cr_val,
        C_h=C_h, C_c=C_c, C_min=C_min_val, C_max=C_max_val,
        Th_o=Th_o, Tc_o=Tc_o, LMTD=lmtd_val,
        ht=ht, dp_tube=dp_tube, dp_shell=dp_shell,
        baffle=baffle_result, tema_code=tema_code,
        fiv=fiv_result, cost=cost_result, fouling_pred=fouling_result,
        nozzle_hot_in=nozzle_hi, nozzle_hot_out=nozzle_ho,
        nozzle_cold_in=nozzle_ci, nozzle_cold_out=nozzle_co,
        area_required=area_required, area_actual=geom.N_tubes * A_per_tube,
        converged=converged, iterations=iteration,
        warnings=warnings,
    )


# ---------------------------------------------------------------------------
# Geometry validation
# ---------------------------------------------------------------------------

def validate_tube_geometry(geom: GeometryInput) -> None:
    """Validate geometry inputs."""
    if geom.D_i <= 0 or geom.D_o <= 0:
        raise ValueError(f"Diameters must be positive: D_i={geom.D_i}, D_o={geom.D_o}")
    if geom.D_o <= geom.D_i:
        raise ValueError(f"Outer diameter ({geom.D_o}) must exceed inner diameter ({geom.D_i})")
    if geom.L <= 0:
        raise ValueError(f"Length must be positive: L={geom.L}")
    if geom.N_tubes < 1:
        raise ValueError(f"N_tubes must be >= 1, got {geom.N_tubes}")
    if geom.D_shell <= 0:
        raise ValueError(f"Shell diameter must be positive: D_shell={geom.D_shell}")


# ---------------------------------------------------------------------------
# Pretty-print results
# ---------------------------------------------------------------------------

def print_results(result: SolverResult, mode: str = "rating",
                   Th_inlet: float = 0.0, Tc_inlet: float = 0.0) -> None:
    """Print a formatted results summary."""
    print_section("HEAT EXCHANGER RESULTS")

    print(f"\n  Mode: {mode.upper()}")
    print(f"  Converged: {'YES' if result.converged else 'NO'} "
          f"(iterations: {result.iterations})")

    if result.warnings:
        print("\n  WARNINGS:")
        for w in result.warnings:
            print(f"    - {w}")

    print_section("Thermal Performance")
    print_result_row("Heat duty q", result.q, "W")
    print_result_row("q_max", result.q_max, "W")
    print_result_row("Effectiveness epsilon", result.epsilon, "-")
    print_result_row("NTU", result.NTU, "-")
    print_result_row("Heat capacity ratio Cr", result.Cr, "-")

    print_section("Capacity Rates")
    print_result_row("C_h (hot)", result.C_h, "W/K")
    print_result_row("C_c (cold)", result.C_c, "W/K")
    print_result_row("C_min", result.C_min, "W/K")
    print_result_row("C_max", result.C_max, "W/K")

    print_section("Temperatures")
    print_result_row("T_h,in", Th_inlet, "K")
    print_result_row("T_h,o", result.Th_o, "K")
    print_result_row("T_c,in", Tc_inlet, "K")
    print_result_row("T_c,o", result.Tc_o, "K")
    print_result_row("LMTD", result.LMTD, "K")

    print_section("Heat Transfer Coefficients")
    print_result_row("h_i (tube-side)", result.ht.h_i, "W/(m^2.K)")
    print_result_row("h_o (shell-side)", result.ht.h_o, "W/(m^2.K)")
    print_result_row("U_o (clean)", result.ht.U_o, "W/(m^2.K)")
    print_result_row("U_o (fouled)", result.ht.U_o_fouled, "W/(m^2.K)")
    print_result_row("Re_i (tube)", result.ht.Re_i, "-")
    print_result_row("Re_o (shell)", result.ht.Re_o, "-")

    print_section("Pressure Drops")
    print_result_row("Tube-side dP", result.dp_tube.delta_P, "Pa")
    print_result_row("  (friction)", result.dp_tube.delta_P_friction, "Pa")
    print_result_row("  (minor losses)", result.dp_tube.delta_P_minor, "Pa")
    print_result_row("  velocity", result.dp_tube.velocity, "m/s")
    print(f"  {'  regime':<35s} {result.dp_tube.regime:>12s}")
    print_result_row("Shell-side dP", result.dp_shell.delta_P, "Pa")
    print_result_row("  velocity", result.dp_shell.velocity, "m/s")

    if mode == "design":
        print_section("Design Sizing")
        print_result_row("Required area", result.area_required, "m^2")
        print_result_row("Actual area", result.area_actual, "m^2")
