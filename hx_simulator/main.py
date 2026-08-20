"""CLI entry point for the Heat Exchanger Simulator.

Run:  python -m hx_simulator.main
  or: python hx_simulator/main.py

Interactive prompts guide the user through selecting mode, fluids,
geometry, and operating conditions. Results are printed as formatted tables.
"""

from __future__ import annotations

import sys
import os

# Ensure parent directory is on path for relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hx_simulator.fluids import FluidProperties, get_properties, make_custom_fluid
from hx_simulator.hx_solver import (
    FluidInput, GeometryInput, SolverResult,
    solve_rating, solve_design, print_results,
)
from hx_simulator.utils import print_section


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------

def prompt_float(msg: str, default: float | None = None) -> float:
    """Prompt user for a float value, with optional default."""
    while True:
        suffix = f" [{default}]" if default is not None else ""
        raw = input(f"  {msg}{suffix}: ").strip()
        if raw == "" and default is not None:
            return default
        try:
            return float(raw)
        except ValueError:
            print(f"    Invalid number: '{raw}'. Try again.")


def prompt_int(msg: str, default: int | None = None) -> int:
    """Prompt user for an integer value."""
    while True:
        suffix = f" [{default}]" if default is not None else ""
        raw = input(f"  {msg}{suffix}: ").strip()
        if raw == "" and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print(f"    Invalid integer: '{raw}'. Try again.")


def prompt_choice(msg: str, options: list[str], default: int = 0) -> str:
    """Prompt user to choose from numbered options. Returns selected option string."""
    print(f"\n  {msg}")
    for i, opt in enumerate(options):
        marker = " (default)" if i == default else ""
        print(f"    [{i+1}] {opt}{marker}")
    while True:
        raw = input("  Enter choice: ").strip()
        if raw == "":
            return options[default]
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        print(f"    Invalid choice. Enter 1-{len(options)}.")


def prompt_fluid(label: str) -> FluidInput:
    """Interactively prompt for fluid information."""
    print_section(f"Fluid: {label}")

    fluid_name = prompt_choice(
        f"Select {label} fluid:",
        ["water", "air", "oil", "custom"],
        default=0,
    )

    T_inlet = prompt_float(f"{label} inlet temperature [K]")

    m_dot = prompt_float(f"{label} mass flow rate [kg/s]")

    if fluid_name == "custom":
        print("  Enter custom fluid properties:")
        rho = prompt_float("  density rho [kg/m^3]")
        mu  = prompt_float("  dynamic viscosity mu [Pa.s]")
        Cp  = prompt_float("  specific heat Cp [J/(kg.K)]")
        k   = prompt_float("  thermal conductivity k [W/(m.K)]")
        props = make_custom_fluid(rho, mu, Cp, k)
        return FluidInput(
            name="custom", T_inlet=T_inlet, m_dot=m_dot,
            properties=props, rho=rho, mu=mu, Cp=Cp, k=k,
        )
    else:
        return FluidInput(name=fluid_name, T_inlet=T_inlet, m_dot=m_dot)


def prompt_geometry() -> GeometryInput:
    """Interactively prompt for HX geometry."""
    print_section("Heat Exchanger Geometry")

    hx_type = prompt_choice("HX type:", ["double_pipe", "shell_and_tube"], default=0)

    D_i = prompt_float("Tube inner diameter D_i [m]", default=0.0254)
    D_o = prompt_float("Tube outer diameter D_o [m]", default=0.0318)
    L   = prompt_float("Tube length L [m]", default=3.0)

    N_tubes = 1
    D_shell = 0.0
    if hx_type == "shell_and_tube":
        N_tubes = prompt_int("Number of tubes", default=10)
        D_shell = prompt_float("Shell inner diameter D_shell [m]", default=0.1)

    k_wall = prompt_float("Tube wall conductivity k_wall [W/(m.K)]", default=50.0)

    fouling = prompt_choice(
        "Fouling condition:",
        list(__import__("hx_simulator.heat_transfer", fromlist=["FOULING_FACTORS"])
             .FOULING_FACTORS.keys()),
        default=0,  # 'clean' is typically first
    )

    arrangement = prompt_choice(
        "Flow arrangement:",
        ["counter", "parallel"],
        default=0,
    )

    pitch_ratio = 1.25
    if hx_type == "shell_and_tube":
        pitch_ratio = prompt_float("Pitch ratio (pitch/D_o)", default=1.25)

    return GeometryInput(
        D_i=D_i, D_o=D_o, L=L, N_tubes=N_tubes,
        D_shell=D_shell, pitch_ratio=pitch_ratio,
        k_wall=k_wall, fouling=fouling, arrangement=arrangement,
    )


# ---------------------------------------------------------------------------
# Main CLI
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the interactive HX simulator."""
    print("\n" + "=" * 60)
    print("  HEAT EXCHANGER SIMULATOR")
    print("  Double-Pipe & Shell-and-Tube HX Design Tool")
    print("  Based on HTOA 2025 course formulas")
    print("=" * 60)

    # --- Mode ---
    mode = prompt_choice(
        "Select operating mode:",
        ["rating", "design"],
        default=0,
    )

    # --- Fluids ---
    hot = prompt_fluid("Hot")
    cold = prompt_fluid("Cold")

    # --- Geometry ---
    geom = prompt_geometry()

    # --- Design-specific inputs ---
    Tc_o_desired = None
    q_duty = None
    if mode == "design":
        print_section("Design Requirements")
        design_target = prompt_choice(
            "Specify design target:",
            ["cold_outlet_temperature", "heat_duty"],
            default=0,
        )
        if design_target == "cold_outlet_temperature":
            Tc_o_desired = prompt_float("Desired T_c,out [K]")
        else:
            q_duty = prompt_float("Required heat duty q [W]")

    # --- Solve ---
    print_section("Solving...")
    try:
        if mode == "rating":
            result = solve_rating(hot, cold, geom)
        else:
            result = solve_design(hot, cold, geom,
                                  Tc_o_desired=Tc_o_desired,
                                  q_duty=q_duty)
    except Exception as e:
        print(f"\n  ERROR: {e}")
        sys.exit(1)

    # --- Output ---
    print_results(result, mode, Th_inlet=hot.T_inlet, Tc_inlet=cold.T_inlet)

    # --- Summary ---
    print_section("PHYSICS SUMMARY")
    print(f"  Heat transferred:     {result.q:.2f} W")
    print(f"  Hot fluid:  {hot.T_inlet:.2f} K -> {result.Th_o:.2f} K  "
          f"(dCp = {hot.m_dot:.4f} kg/s)")
    print(f"  Cold fluid: {cold.T_inlet:.2f} K -> {result.Tc_o:.2f} K  "
          f"(mCp = {cold.m_dot:.4f} kg/s)")
    print(f"  LMTD:       {result.LMTD:.2f} K")
    print(f"  Effectiveness: {result.epsilon:.4f} ({result.epsilon*100:.1f}%)")
    if mode == "design":
        print(f"  Required area: {result.area_required:.4f} m^2")
    print()


if __name__ == "__main__":
    main()
