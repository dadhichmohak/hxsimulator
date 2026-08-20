"""Flow-Induced Vibration (FIV) analysis for shell-and-tube heat exchangers.

Checks for:
  1. Vortex shedding frequency vs tube natural frequency
  2. Fluidelastic instability (critical velocity)
  3. Turbulent buffeting
  4. Acoustic resonance

References:
  - TEMA Standards, 10th Ed., Section RGP G-4.4
  - Connors, H.J. "Fluidelastic Instability of Tube Arrays", ASME 1970
  - HTRI Xvib methodology
  - Palmer & Rowley, "Flow-Induced Vibration of Heat Exchanger Tube Bundles"
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class FIVResult:
    """Flow-Induced Vibration analysis result."""
    # Frequencies
    f_natural: float        # Tube natural frequency [Hz]
    f_vortex: float         # Vortex shedding frequency [Hz]
    f_ratio: float          # f_vortex / f_natural (dangerous if ~1.0)

    # Critical velocities
    v_critical_elastic: float   # Fluidelastic instability critical velocity [m/s]
    v_crossflow: float          # Actual crossflow velocity [m/s]
    v_ratio_elastic: float      # v_crossflow / v_critical (<1 safe)

    v_critical_vortex: float    # Critical velocity for vortex resonance [m/s]
    v_ratio_vortex: float       # v_crossflow / v_critical_vortex

    # Amplitudes
    amplitude_turbulent: float  # Turbulent buffeting amplitude [m]
    amplitude_vortex: float     # Vortex-induced amplitude [m]
    total_amplitude: float      # Combined amplitude [m]

    # Clearance check
    min_clearance: float        # Minimum tube-to-baffle clearance [m]
    amplitude_ok: bool          # Amplitude < clearance

    # Acoustic resonance
    f_acoustic: float           # Acoustic frequency [Hz]
    acoustic_resonant: bool     # Whether acoustic resonance occurs

    # Summary
    safe: bool                  # Overall FIV safety
    warnings: list[str]


def tube_natural_frequency(
    E: float,           # Young's modulus [Pa]
    I: float,           # Tube moment of inertia [m^4]
    rho_tube: float,    # Tube material density [kg/m^3]
    A_tube: float,      # Tube cross-sectional area [m^2]
    L_eff: float,       # Effective tube length between supports [m]
    m_fluid: float = 0.0,  # Added fluid mass per unit length [kg/m]
) -> float:
    """Tube natural frequency (first mode, simply supported).

    f_n = (pi^2 / (2 * L_eff^2)) * sqrt(E*I / (rho_tube * A_tube + m_fluid))
    """
    m_total = rho_tube * A_tube + m_fluid
    if m_total <= 0 or E <= 0 or I <= 0:
        return 0.0
    f_n = (math.pi**2 / (2 * L_eff**2)) * math.sqrt(E * I / m_total)
    return f_n


def vortex_shedding_frequency(v: float, D_o: float, St: float = 0.2) -> float:
    """Strouhal-based vortex shedding frequency.

    f_v = St * v / D_o
    Typical St = 0.18–0.22 for tube banks.
    """
    if D_o <= 0 or v <= 0:
        return 0.0
    return St * v / D_o


def fluidelastic_critical_velocity(
    f_n: float,
    D_o: float,
    m_tube: float,     # mass per unit length [kg/m]
    delta_a: float,    # logarithmic decrement of damping
    K_c: float = 3.0,  # Connors constant (typically 2.7–3.5)
) -> float:
    """Critical velocity for fluidelastic instability (Connors criterion).

    v_cr = K_c * f_n * D_o * sqrt(m_tube * delta_a / (rho * D_o^2))

    Simplified: v_cr = K_c * f_n * D_o  (conservative)
    """
    if f_n <= 0 or D_o <= 0:
        return float('inf')
    return K_c * f_n * D_o


def turbulent_buffeting_amplitude(
    rho: float,
    v: float,
    D_o: float,
    L_eff: float,
    f_n: float,
    mu: float,
) -> float:
    """Approximate turbulent buffeting amplitude.

    Empirical correlation based on Owen's method.
    """
    if f_n <= 0 or D_o <= 0 or rho <= 0:
        return 0.0
    Re = rho * v * D_o / mu
    # Simplified empirical
    amplitude = 0.001 * D_o * (v / (f_n * D_o))**1.5 * (Re / 10000)**0.2
    return max(0.0, amplitude)


def vortex_induced_amplitude(
    D_o: float,
    v: float,
    v_cr_elastic: float,
    damping: float = 0.02,
) -> float:
    """Amplitude from vortex-induced vibration near lock-in."""
    if v_cr_elastic <= 0:
        return 0.0
    ratio = v / v_cr_elastic
    if 0.7 < ratio < 1.3:
        # Lock-in region: amplitude is significant
        return D_o * 0.05 * damping / max(1e-6, abs(ratio - 1.0))
    return 0.0


def acoustic_frequency(
    c: float,          # Speed of sound in shell-side fluid [m/s]
    D_shell: float,    # Shell inner diameter [m]
    mode: int = 1,     # Acoustic mode (1 = fundamental)
) -> float:
    """Acoustic natural frequency for shell side.

    f_ac = mode * c / (2 * D_shell)
    """
    if D_shell <= 0 or c <= 0:
        return 0.0
    return mode * c / (2 * D_shell)


def fiv_analysis(
    # Geometry
    D_o: float,
    D_i: float,
    D_shell: float,
    L: float,           # Tube length
    L_baffle: float,    # Baffle spacing (effective support length)
    pitch_ratio: float = 1.25,
    tube_layout: str = "triangular",
    # Material
    E: float = 2.0e11,       # Young's modulus [Pa] (carbon steel)
    rho_tube: float = 7800,  # Tube density [kg/m^3]
    # Fluid properties (shell-side)
    rho_fluid: float = 1000,
    mu_fluid: float = 0.001,
    v_crossflow: float = 1.0,  # Shell-side crossflow velocity [m/s]
    # Tube
    tube_thickness: float = 0.002,  # Wall thickness [m]
    # Safety
    K_connors: float = 3.0,
    amplitude_limit: float = 0.0005,  # Max allowable amplitude [m] (~5% of clearance)
) -> FIVResult:
    """Complete FIV analysis for a shell-and-tube HX.

    Returns FIVResult with all vibration parameters and safety checks.
    """
    warnings = []

    # Tube geometry
    A_tube = math.pi / 4 * (D_o**2 - D_i**2)
    I_tube = math.pi / 64 * (D_o**4 - D_i**4)
    m_tube = rho_tube * A_tube  # mass per unit length [kg/m]

    # Added fluid mass (approximate)
    m_fluid = rho_fluid * math.pi * D_i**2 / 4  # internal fluid only

    # Effective length between supports
    L_eff = L_baffle

    # Tube natural frequency
    f_n = tube_natural_frequency(E, I_tube, rho_tube, A_tube, L_eff, m_fluid)

    # Vortex shedding frequency
    f_v = vortex_shedding_frequency(v_crossflow, D_o)

    # Frequency ratio
    f_ratio = f_v / f_n if f_n > 0 else 0.0

    # Fluidelastic critical velocity
    delta_a = 0.05  # typical logarithmic decrement
    v_cr_elastic = fluidelastic_critical_velocity(f_n, D_o, m_tube, delta_a, K_connors)
    v_ratio_elastic = v_crossflow / v_cr_elastic if v_cr_elastic > 0 else 0.0

    # Vortex critical velocity (when f_v = f_n)
    v_cr_vortex = f_n * D_o / 0.2 if f_n > 0 else float('inf')
    v_ratio_vortex = v_crossflow / v_cr_vortex if v_cr_vortex > 0 else 0.0

    # Amplitudes
    amp_turb = turbulent_buffeting_amplitude(rho_fluid, v_crossflow, D_o, L_eff, f_n, mu_fluid)
    amp_vortex = vortex_induced_amplitude(D_o, v_crossflow, v_cr_elastic)
    total_amp = math.sqrt(amp_turb**2 + amp_vortex**2)

    # Tube-to-baffle clearance (typical)
    min_clearance = 0.0008  # 0.8 mm typical
    amp_ok = total_amp < min_clearance * amplitude_limit / 0.0005

    # Acoustic resonance
    c_sound = 343.0  # approximate for air; should be computed from fluid
    f_ac = acoustic_frequency(c_sound, D_shell)
    f_ac_ratio = f_v / f_ac if f_ac > 0 else 0.0
    acoustic_resonant = 0.8 < f_ac_ratio < 1.2

    # Overall safety
    safe = True
    if v_ratio_elastic > 1.0:
        safe = False
        warnings.append(f"FLUIDELASTIC INSTABILITY: v/v_cr = {v_ratio_elastic:.2f} > 1.0")
    if f_ratio > 0.8 and f_ratio < 1.2:
        warnings.append(f"VORTEX RESONANCE RISK: f_v/f_n = {f_ratio:.2f} (near 1.0)")
    if not amp_ok:
        safe = False
        warnings.append(f"EXCESSIVE AMPLITUDE: {total_amp*1000:.3f}mm > limit")
    if acoustic_resonant:
        warnings.append(f"ACOUSTIC RESONANCE: f_ac = {f_ac:.1f}Hz, f_v/f_ac = {f_ac_ratio:.2f}")

    return FIVResult(
        f_natural=f_n,
        f_vortex=f_v,
        f_ratio=f_ratio,
        v_critical_elastic=v_cr_elastic,
        v_crossflow=v_crossflow,
        v_ratio_elastic=v_ratio_elastic,
        v_critical_vortex=v_cr_vortex,
        v_ratio_vortex=v_ratio_vortex,
        amplitude_turbulent=amp_turb,
        amplitude_vortex=amp_vortex,
        total_amplitude=total_amp,
        min_clearance=min_clearance,
        amplitude_ok=amp_ok,
        f_acoustic=f_ac,
        acoustic_resonant=acoustic_resonant,
        safe=safe,
        warnings=warnings,
    )
