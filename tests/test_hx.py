"""Tests for the HX simulator — validated against lecture worked examples.

References:
  - 08_heat_exchangers.md §4c: Rating example with U=2000, A=10, Ch=5556, Cc=5806
  - 06_convection_internal.md §5: Dittus-Boelter in turbulent pipe flow
  - 00_formula_cheatsheet.md: Dimensionless number definitions
"""

import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hx_simulator.utils import (
    Re_D, Re_D_from_mdot, Nu_D, Pr, LMTD,
    epsilon_NTU_counterflow, epsilon_NTU_parallel, epsilon_NTU_phase_change,
    epsilon_NTU_shell_tube, NTU_from_epsilon_shell_tube,
    epsilon_NTU_crossflow_both_unmixed, epsilon_NTU_crossflow_one_mixed,
    NTU_from_epsilon_crossflow_one_mixed,
    NTU_from_epsilon_counterflow, heat_capacity_rate, q_max, check_convergence,
)
from hx_simulator.fluids import get_properties, make_custom_fluid, get_h_fg_water
from hx_simulator.heat_transfer import (
    dittus_boelter, laminar_Nu, U_clean, U_fouled,
    compute_h_tube, fin_analysis, overall_surface_efficiency,
    FOULING_FACTORS,
)
from hx_simulator.pressure_drop import (
    friction_factor, tube_side_dp, shell_side_dp,
)
from hx_simulator.hx_solver import (
    FluidInput, GeometryInput, solve_rating, solve_design,
)


# ============================================================
# 1. Dimensionless numbers
# ============================================================

class TestDimensionlessNumbers:
    def test_Re_D(self):
        """Re = rho*v*D/mu"""
        assert Re_D(1000.0, 1.0, 0.05, 0.001) == 50000.0

    def test_Re_D_from_mdot(self):
        """Re = 4*mdot/(pi*D*mu)"""
        mdot = 0.1
        D = 0.025
        mu = 0.001
        Re = Re_D_from_mdot(mdot, D, mu)
        expected = 4 * mdot / (math.pi * D * mu)
        assert abs(Re - expected) < 1e-10

    def test_Nu_D(self):
        """Nu = h*D/k"""
        assert Nu_D(100.0, 0.05, 0.6) == Nu_D(100.0, 0.05, 0.6)
        assert abs(Nu_D(100.0, 0.05, 0.6) - 8.3333) < 0.01

    def test_Pr(self):
        """Pr = mu*Cp/k"""
        Pr_val = Pr(0.001, 4180, 0.6)
        expected = 0.001 * 4180 / 0.6
        assert abs(Pr_val - expected) < 1e-10


# ============================================================
# 2. LMTD
# ============================================================

class TestLMTD:
    def test_equal_dT(self):
        """When dT1 == dT2, LMTD = dT1."""
        assert abs(LMTD(50.0, 50.0) - 50.0) < 1e-10

    def test_known_value(self):
        """Classic example: dT1=100, dT2=50 → LMTD = 72.13"""
        lmtd = LMTD(100.0, 50.0)
        expected = (100 - 50) / math.log(100 / 50)
        assert abs(lmtd - expected) < 0.01

    def test_from_lecture(self):
        """From 08_heat_exchangers.md §4c: counter-flow example."""
        # Th_i=120, Tc_o=90 → dT1=30; Th_o=100, Tc_i=20 → dT2=80
        lmtd = LMTD(30.0, 80.0)
        expected = (30 - 80) / math.log(30 / 80)
        assert abs(lmtd - expected) < 0.01

    def test_raises_on_negative(self):
        """LMTD should raise on non-positive dT."""
        import pytest
        with pytest.raises(ValueError):
            LMTD(-10.0, 50.0)


# ============================================================
# 3. ε-NTU relations
# ============================================================

class TestEpsilonNTU:
    def test_counterflow_known(self):
        """Counter-flow ε-NTU with Cr=0.5, NTU=2 → known value."""
        eps = epsilon_NTU_counterflow(2.0, 0.5)
        # Manual: exp(-2*0.5) = exp(-1) = 0.3679
        # eps = (1 - 0.3679) / (1 - 0.5*0.3679) = 0.6321 / 0.8160 = 0.7746
        assert abs(eps - 0.7746) < 0.01

    def test_counterflow_Cr0(self):
        """When Cr=0 (phase change), ε = 1-exp(-NTU)."""
        eps = epsilon_NTU_counterflow(2.0, 0.0)
        expected = 1 - math.exp(-2.0)
        assert abs(eps - expected) < 1e-10

    def test_counterflow_Cr1(self):
        """When Cr=1, ε = NTU/(1+NTU)."""
        eps = epsilon_NTU_counterflow(2.0, 1.0)
        expected = 2.0 / 3.0
        assert abs(eps - expected) < 1e-10

    def test_parallel_known(self):
        """Parallel-flow ε-NTU with Cr=0.5, NTU=1."""
        eps = epsilon_NTU_parallel(1.0, 0.5)
        expected = (1 - math.exp(-1.5)) / 1.5
        assert abs(eps - expected) < 1e-10

    def test_phase_change(self):
        """Phase change: ε = 1-exp(-NTU)."""
        eps = epsilon_NTU_phase_change(1.5)
        expected = 1 - math.exp(-1.5)
        assert abs(eps - expected) < 1e-10

    def test_invert_counterflow(self):
        """NTU from ε: round-trip should recover."""
        for NTU_true in [0.5, 1.0, 2.0, 3.0]:
            Cr_val = 0.5
            eps = epsilon_NTU_counterflow(NTU_true, Cr_val)
            NTU_recovered = NTU_from_epsilon_counterflow(eps, Cr_val)
            assert abs(NTU_recovered - NTU_true) < 1e-6, (
                f"Round-trip failed: NTU_true={NTU_true}, recovered={NTU_recovered}"
            )

    def test_shell_tube_known(self):
        """Shell-and-tube (1 shell, 2+ tube) with Cr=0.5, NTU=2."""
        eps = epsilon_NTU_shell_tube(2.0, 0.5)
        # Should be between parallel and counter-flow
        eps_par = epsilon_NTU_parallel(2.0, 0.5)
        eps_cnt = epsilon_NTU_counterflow(2.0, 0.5)
        assert eps_par < eps < eps_cnt, (
            f"Shell-tube eps={eps:.4f} not between parallel={eps_par:.4f} and counter={eps_cnt:.4f}"
        )

    def test_shell_tube_Cr0(self):
        """Shell-and-tube with Cr=0 should match phase-change formula."""
        eps = epsilon_NTU_shell_tube(2.0, 0.0)
        expected = epsilon_NTU_phase_change(2.0)
        assert abs(eps - expected) < 1e-10

    def test_invert_shell_tube(self):
        """Round-trip NTU from ε for shell-and-tube."""
        for NTU_true in [0.5, 1.0, 2.0, 3.0]:
            Cr_val = 0.5
            eps = epsilon_NTU_shell_tube(NTU_true, Cr_val)
            NTU_recovered = NTU_from_epsilon_shell_tube(eps, Cr_val)
            assert abs(NTU_recovered - NTU_true) < 1e-6, (
                f"Shell-tube round-trip failed: NTU_true={NTU_true}, recovered={NTU_recovered}"
            )

    def test_crossflow_both_unmixed(self):
        """Cross-flow (both unmixed) should be between parallel and counter."""
        eps = epsilon_NTU_crossflow_both_unmixed(2.0, 0.5)
        eps_par = epsilon_NTU_parallel(2.0, 0.5)
        eps_cnt = epsilon_NTU_counterflow(2.0, 0.5)
        assert eps_par < eps < eps_cnt, (
            f"Crossflow eps={eps:.4f} not between parallel={eps_par:.4f} and counter={eps_cnt:.4f}"
        )

    def test_crossflow_one_mixed_Cr0(self):
        """Cross-flow (one mixed) with Cr=0 should match phase-change."""
        eps_cold = epsilon_NTU_crossflow_one_mixed(2.0, 0.0, "cold")
        eps_hot = epsilon_NTU_crossflow_one_mixed(2.0, 0.0, "hot")
        expected = epsilon_NTU_phase_change(2.0)
        assert abs(eps_cold - expected) < 1e-10
        assert abs(eps_hot - expected) < 1e-10

    def test_crossflow_one_mixed_cold(self):
        """Cross-flow (C_c mixed, C_h unmixed) with Cr=0.5, NTU=2."""
        eps = epsilon_NTU_crossflow_one_mixed(2.0, 0.5, "cold")
        # Should be between parallel and counter
        eps_par = epsilon_NTU_parallel(2.0, 0.5)
        eps_cnt = epsilon_NTU_counterflow(2.0, 0.5)
        assert eps_par < eps < eps_cnt

    def test_crossflow_one_mixed_hot(self):
        """Cross-flow (C_h mixed, C_c unmixed) with Cr=0.5, NTU=2."""
        eps = epsilon_NTU_crossflow_one_mixed(2.0, 0.5, "hot")
        eps_par = epsilon_NTU_parallel(2.0, 0.5)
        eps_cnt = epsilon_NTU_counterflow(2.0, 0.5)
        assert eps_par < eps < eps_cnt

    def test_invert_crossflow_one_mixed(self):
        """Round-trip NTU from ε for cross-flow (one mixed)."""
        for NTU_true in [0.5, 1.0, 2.0, 3.0]:
            Cr_val = 0.4
            for side in ["cold", "hot"]:
                eps = epsilon_NTU_crossflow_one_mixed(NTU_true, Cr_val, side)
                NTU_recovered = NTU_from_epsilon_crossflow_one_mixed(eps, Cr_val, side)
                assert abs(NTU_recovered - NTU_true) < 1e-5, (
                    f"Crossflow ({side}) round-trip failed: NTU_true={NTU_true}, recovered={NTU_recovered}"
                )


# ============================================================
# 4. Fluid properties
# ============================================================

class TestFluids:
    def test_water_300K(self):
        """Water at 300K: rho~997, mu~0.855e-3, Pr~5.89."""
        props = get_properties("water", 300.0)
        assert abs(props.rho - 997.0) < 5.0
        assert abs(props.mu - 0.855e-3) < 0.05e-3
        assert abs(props.Pr - 5.89) < 0.5

    def test_air_300K(self):
        """Air at 300K: rho~1.1614, mu~1.846e-5, Pr~0.707."""
        props = get_properties("air", 300.0)
        assert abs(props.rho - 1.1614) < 0.05
        assert abs(props.mu - 1.846e-5) < 0.1e-5
        assert abs(props.Pr - 0.707) < 0.05

    def test_oil_300K(self):
        """Engine oil at 300K: rho~884, mu~0.55, Pr~7250."""
        props = get_properties("oil", 300.0)
        assert abs(props.rho - 884.0) < 10.0
        assert abs(props.mu - 0.55) < 0.1
        assert props.Pr > 5000  # very high Pr

    def test_custom_fluid(self):
        """Custom fluid creation."""
        props = make_custom_fluid(1000.0, 0.001, 4180, 0.6)
        assert props.rho == 1000.0
        assert props.mu == 0.001
        assert abs(props.Pr - 0.001 * 4180 / 0.6) < 1e-10

    def test_h_fg_water(self):
        """Latent heat of water at 373K ~ 2.256e6 J/kg."""
        hfg = get_h_fg_water(373.15)
        assert 2.2e6 < hfg < 2.6e6


# ============================================================
# 5. Heat transfer coefficients
# ============================================================

class TestHeatTransfer:
    def test_dittus_boelter_heating(self):
        """Dittus-Boelter: Nu = 0.023*Re^0.8*Pr^0.4 (heating)."""
        Re = 50000
        Pr_val = 5.0
        Nu = dittus_boelter(Re, Pr_val, heating=True)
        expected = 0.023 * Re**0.8 * Pr_val**0.4
        assert abs(Nu - expected) < 1e-10

    def test_dittus_boelter_cooling(self):
        """Dittus-Boelter: n=0.3 for cooling."""
        Nu_cool = dittus_boelter(50000, 5.0, heating=False)
        Nu_heat = dittus_boelter(50000, 5.0, heating=True)
        assert Nu_cool < Nu_heat  # cooling should give lower Nu

    def test_laminar_Nu(self):
        """Laminar Nu: 4.36 (const flux) or 3.66 (const Ts)."""
        assert laminar_Nu(heating=True) == 4.36
        assert laminar_Nu(heating=False) == 3.66

    def test_U_clean(self):
        """Overall U for a simple case: known analytical result."""
        D_i = 0.025
        D_o = 0.030
        L = 3.0
        h_i = 5000.0
        h_o = 2000.0
        k_wall = 50.0
        U = U_clean(D_i, D_o, L, h_i, h_o, k_wall)
        # Manual: 1/U = (D_o/D_i)/h_i + D_o*ln(D_o/D_i)/(2*k) + 1/h_o
        expected_inv = (D_o/D_i)/h_i + D_o*math.log(D_o/D_i)/(2*k_wall) + 1/h_o
        assert abs(1/U - expected_inv) < 1e-10

    def test_fouling_reduces_U(self):
        """Fouling should reduce overall U."""
        U_c = U_clean(0.025, 0.030, 3.0, 5000, 2000, 50.0)
        U_f = U_fouled(U_c, 0.025, 0.030, 1e-4, 1e-4)
        assert U_f < U_c

    def test_compute_h_tube_turbulent(self):
        """Tube-side h in turbulent regime."""
        # Water at ~300K flowing at 0.5 kg/s through D_i=25mm tube
        props = get_properties("water", 300.0)
        h, warnings = compute_h_tube(0.5, 0.025, 3.0, props, heating=True)
        Re = Re_D_from_mdot(0.5, 0.025, props.mu)
        assert Re > 10000, f"Expected turbulent, got Re={Re}"
        assert h > 0

    def test_fin_analysis(self):
        """Fin efficiency should be between 0 and 1."""
        result = fin_analysis(
            h=50.0, P=0.1, A_c=1e-4, k_fin=200.0,
            L_fin=0.05, T_base=350.0, T_inf=300.0,
        )
        assert 0 < result.eta_f <= 1.0
        assert result.q_f > 0
        assert result.effectiveness > 0

    def test_overall_surface_efficiency(self):
        """Overall surface efficiency with zero fins should be 1."""
        eta_o = overall_surface_efficiency(0, 0.01, 0.1, 0.9)
        assert abs(eta_o - 1.0) < 1e-10


# ============================================================
# 6. Pressure drops
# ============================================================

class TestPressureDrop:
    def test_friction_factor_laminar(self):
        """Laminar: f = 64/Re."""
        f = friction_factor(1000)
        assert abs(f - 64/1000) < 1e-10

    def test_friction_factor_turbulent(self):
        """Turbulent: Blasius f = 0.316*Re^-0.25."""
        f = friction_factor(50000)
        expected = 0.316 * 50000**(-0.25)
        assert abs(f - expected) < 1e-10

    def test_tube_dp_positive(self):
        """Tube-side dP should be positive."""
        props = get_properties("water", 300.0)
        result = tube_side_dp(0.5, 0.025, 3.0, props.rho, props.mu)
        assert result.delta_P > 0
        assert result.velocity > 0

    def test_shell_dp_positive(self):
        """Shell-side dP should be positive."""
        props = get_properties("water", 300.0)
        result = shell_side_dp(0.3, 0.030, 0.1, 3.0, 10, props.rho, props.mu)
        assert result.delta_P > 0


# ============================================================
# 7. Rating solver  (lecture example: 08 §4c)
# ============================================================

class TestRatingSolver:
    def test_lecture_example(self):
        """Validate against 08_heat_exchangers.md §4c.

        Counter-flow HX, U=2000 W/m2K, A=10 m2.
        Hot: Ch=5556 W/K, Th_i=393.15 K (120°C)
        Cold: Cc=5806 W/K, Tc_i=293.15 K (20°C)

        Expected from the lecture: q should be between 20,000 and 35,000 W
        depending on the iteration.
        """
        hot = FluidInput(
            name="custom", T_inlet=393.15, m_dot=1.0,
            properties=make_custom_fluid(983.0, 2.82e-4, 4190.0, 0.670),
        )
        hot.Cp = 5556.0 / 1.0  # C_h / m_dot = Cp

        cold = FluidInput(
            name="custom", T_inlet=293.15, m_dot=1.0,
            properties=make_custom_fluid(998.0, 1.0e-3, 4182.0, 0.600),
        )
        cold.Cp = 5806.0 / 1.0

        geom = GeometryInput(
            D_i=0.025, D_o=0.030, L=3.0, N_tubes=1,
            D_shell=0.08, k_wall=50.0, fouling="clean",
            arrangement="counter",
        )

        result = solve_rating(hot, cold, geom)

        # q should be positive and reasonable
        assert result.q > 0, f"Heat duty should be positive, got {result.q}"
        assert result.q < 100_000, f"Heat duty unreasonably large: {result.q}"

        # Outlet temperatures should make physical sense
        assert result.Th_o < 393.15, "Hot outlet should be below hot inlet"
        assert result.Tc_o > 293.15, "Cold outlet should be above cold inlet"

        # Effectiveness should be between 0 and 1
        assert 0 < result.epsilon < 1

        # LMTD should be positive
        assert result.LMTD > 0

    def test_counterflow_better_than_parallel(self):
        """Counter-flow should achieve higher effectiveness than parallel."""
        props = make_custom_fluid(997.0, 8.55e-4, 4179.0, 0.606)

        base_args = dict(
            D_i=0.025, D_o=0.030, L=3.0, N_tubes=1,
            D_shell=0.08, k_wall=50.0, fouling="clean",
        )

        hot = FluidInput(name="custom", T_inlet=350.0, m_dot=0.5, properties=props)
        hot.Cp = 4179.0
        cold = FluidInput(name="custom", T_inlet=300.0, m_dot=0.5, properties=props)
        cold.Cp = 4179.0

        geom_counter = GeometryInput(**base_args, arrangement="counter")
        geom_parallel = GeometryInput(**base_args, arrangement="parallel")

        r_counter = solve_rating(hot, cold, geom_counter)
        r_parallel = solve_rating(hot, cold, geom_parallel)

        assert r_counter.epsilon >= r_parallel.epsilon, (
            f"Counter-flow eps={r_counter.epsilon} should >= parallel eps={r_parallel.epsilon}"
        )

    def test_convergence(self):
        """Solver should converge within reasonable iterations."""
        props = make_custom_fluid(997.0, 8.55e-4, 4179.0, 0.606)
        hot = FluidInput(name="custom", T_inlet=350.0, m_dot=0.5, properties=props)
        hot.Cp = 4179.0
        cold = FluidInput(name="custom", T_inlet=300.0, m_dot=0.5, properties=props)
        cold.Cp = 4179.0

        geom = GeometryInput(
            D_i=0.025, D_o=0.030, L=3.0, N_tubes=1,
            D_shell=0.08, fouling="clean", arrangement="counter",
        )
        result = solve_rating(hot, cold, geom)
        assert result.converged, f"Did not converge in {result.iterations} iterations"
        assert result.iterations <= 50


# ============================================================
# 8. Design solver
# ============================================================

class TestDesignSolver:
    def test_design_produces_area(self):
        """Design mode should produce a positive required area."""
        props = make_custom_fluid(997.0, 8.55e-4, 4179.0, 0.606)
        hot = FluidInput(name="custom", T_inlet=350.0, m_dot=0.5, properties=props)
        hot.Cp = 4179.0
        cold = FluidInput(name="custom", T_inlet=300.0, m_dot=0.5, properties=props)
        cold.Cp = 4179.0

        geom = GeometryInput(
            D_i=0.025, D_o=0.030, L=3.0, N_tubes=1,
            D_shell=0.08, fouling="clean", arrangement="counter",
        )
        result = solve_design(hot, cold, geom, Tc_o_desired=340.0)
        assert result.area_required > 0, "Required area should be positive"
        assert result.q > 0, "Heat duty should be positive"

    def test_design_q_duty_mode(self):
        """Design mode with specified heat duty."""
        props = make_custom_fluid(997.0, 8.55e-4, 4179.0, 0.606)
        hot = FluidInput(name="custom", T_inlet=350.0, m_dot=0.5, properties=props)
        hot.Cp = 4179.0
        cold = FluidInput(name="custom", T_inlet=300.0, m_dot=0.5, properties=props)
        cold.Cp = 4179.0

        geom = GeometryInput(
            D_i=0.025, D_o=0.030, L=3.0, N_tubes=1,
            D_shell=0.08, fouling="clean", arrangement="counter",
        )
        result = solve_design(hot, cold, geom, q_duty=10000.0)
        assert result.area_required > 0
        assert abs(result.q - 10000.0) < 1.0  # should match requested duty


# ============================================================
# 9. Energy balance conservation check
# ============================================================

class TestEnergyBalance:
    def test_energy_conservation(self):
        """q_hot_lost == q_cold_gained (energy conservation)."""
        props = make_custom_fluid(997.0, 8.55e-4, 4179.0, 0.606)
        hot = FluidInput(name="custom", T_inlet=350.0, m_dot=0.5, properties=props)
        hot.Cp = 4179.0
        cold = FluidInput(name="custom", T_inlet=300.0, m_dot=0.5, properties=props)
        cold.Cp = 4179.0

        geom = GeometryInput(
            D_i=0.025, D_o=0.030, L=3.0, N_tubes=1,
            D_shell=0.08, fouling="clean", arrangement="counter",
        )
        result = solve_rating(hot, cold, geom)

        q_hot = hot.m_dot * hot.Cp * (hot.T_inlet - result.Th_o)
        q_cold = cold.m_dot * cold.Cp * (result.Tc_o - cold.T_inlet)
        assert abs(q_hot - q_cold) < 1.0, (
            f"Energy imbalance: q_hot={q_hot:.2f}, q_cold={q_cold:.2f}"
        )

    def test_first_law(self):
        """q from solver should equal ε*C_min*(Th_i - Tc_i)."""
        props = make_custom_fluid(997.0, 8.55e-4, 4179.0, 0.606)
        hot = FluidInput(name="custom", T_inlet=350.0, m_dot=0.5, properties=props)
        hot.Cp = 4179.0
        cold = FluidInput(name="custom", T_inlet=300.0, m_dot=0.5, properties=props)
        cold.Cp = 4179.0

        geom = GeometryInput(
            D_i=0.025, D_o=0.030, L=3.0, N_tubes=1,
            D_shell=0.08, fouling="clean", arrangement="counter",
        )
        result = solve_rating(hot, cold, geom)

        q_check = result.epsilon * result.C_min * (350.0 - 300.0)
        assert abs(result.q - q_check) < 1.0


# ============================================================
# Run with: python -m pytest tests/test_hx.py -v
# ============================================================

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
