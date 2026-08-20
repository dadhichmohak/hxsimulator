# Module 0 — Foundations & Governing Equations
**Date:** 31 July 2025 | **Source:** `htoa2531jul.pdf` (13 pages)

---

## Overview

This lecture establishes the continuum mechanics foundation for the entire course. Starting from molecular-level physics, it derives the three governing equations of fluid mechanics and heat transfer, and introduces constitutive relations that close the system.

---

## 1. The Three Governing Equations

The complete description of a Newtonian fluid requires 6 equations (3 components of momentum + 1 continuity + 1 energy + 1 constitutive). The lectures introduce them in order:

### 1.1 Continuity (Mass Conservation)

$$\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \underline{v}) = 0$$

- $\rho$ = density [kg/m³]
- $\underline{v}$ = velocity vector field [m/s]
- States: *mass neither created nor destroyed*
- For **incompressible flow** (constant $\rho$): $\nabla \cdot \underline{v} = 0$

### 1.2 Momentum (Newton's Second Law for a Fluid Parcel)

$$\rho \frac{D\underline{v}}{Dt} = \rho\underline{g} + \nabla \cdot \underline{\underline{\sigma}}$$

- $\frac{D}{Dt}$ = **material derivative** (following the fluid parcel)
- $\underline{g}$ = gravitational acceleration [m/s²]
- $\underline{\underline{\sigma}}$ = **stress tensor** [Pa] — this is circled in the notes as a key quantity needing a constitutive equation

The material derivative is:
$$\frac{D}{Dt} = \frac{\partial}{\partial t} + \underline{v} \cdot \nabla$$

### 1.3 Energy Equation

$$\rho C_p \frac{DT}{Dt} = -\nabla \cdot \underline{q} + \Phi_v$$

- $C_p$ = specific heat at constant pressure [J/kg·K]
- $\underline{q}$ = heat flux vector [W/m²] — also circled, also needs constitutive relation
- $\Phi_v$ = viscous dissipation term [W/m³]

> **Note from lectures:** Both $\underline{v}$ (in momentum) and $\underline{q}$ (in energy) are circled with arrows pointing to the constitutive equations — they are the *unknowns* that need additional relations to close the system.

---

## 2. Constitutive Equations

Constitutive equations **connect molecular-level quantities to continuum ones**. They are material-specific laws, not universal conservation laws.

### 2.1 For the Stress Tensor — Newtonian Fluid

For a **Newtonian, incompressible fluid**:

$$\underline{\underline{\sigma}} = -p\underline{\underline{\delta}} + \mu\left[(\nabla\underline{v}) + (\nabla\underline{v})^T\right]$$

Where:
- $p$ = pressure [Pa]
- $\underline{\underline{\delta}}$ = identity tensor (Kronecker delta)
- $\mu$ = dynamic viscosity [Pa·s]
- $(\nabla\underline{v})^T$ = transpose of the velocity gradient tensor

This gives the **Navier-Stokes equations** when substituted into the momentum equation.

### 2.2 For the Heat Flux Vector — Fourier's Law

$$\underline{q} = -\underline{\underline{k}} \cdot \nabla T$$

For an **isotropic material** (no intrinsic orientation, i.e., $\underline{\underline{k}} = k\underline{\underline{\delta}}$):

$$\boxed{\underline{q} = -k\nabla T}$$

- $k$ = thermal conductivity [W/mK]
- The negative sign: heat flows **down** temperature gradients (from hot to cold)
- Valid in 1D as: $q = -k\frac{dT}{dx}$

> **Fourier's Statement:** *"Heat flows down temperature gradients"*

For anisotropic materials, $k$ becomes a 3×3 tensor (e.g., crystal structures, composites with preferred directions).

---

## 3. Fourier's Law in 1D (Slab Geometry)

For a planar slab of material, thickness $L$, with temperatures $T_H$ (hot face) and $T_C$ (cold face):

$$q = \frac{Q}{A} = -k\left(\frac{T_C - T_H}{L}\right) = k\frac{T_H - T_C}{L}$$

The minus sign ensures positive heat flux in the direction of decreasing temperature.

**Units of $k$:** $\left[\frac{W}{m \cdot K}\right]$

---

## 4. Course Roadmap (from Lecture 1, 30 Jul)

The overview lecture maps out the entire course structure:

```
Heat Transfer
├── Conduction  [q = -k∇T]
│   ├── Steady-State
│   │   ├── 1D
│   │   └── 2D
│   └── Transient → Lumped Capacitance
├── Convection  [q = h(Ts - T∞)]
│   ├── Forced
│   ├── Natural / Free
│   ├── Boiling & Condensation
│   └── Boundary Layers & Correlations
└── Radiation  [q = εσ(Ts⁴ - Tsur⁴)]

→ Heat Exchangers
    ├── Performance Analysis
    └── Design Problem
```

---

## 5. Key Definitions

| Symbol | Meaning | Units |
|--------|---------|-------|
| $\rho$ | Density | kg/m³ |
| $\underline{v}$ | Velocity vector | m/s |
| $T$ | Temperature | K or °C |
| $p$ | Pressure | Pa |
| $\mu$ | Dynamic viscosity | Pa·s |
| $\nu = \mu/\rho$ | Kinematic viscosity | m²/s |
| $k$ | Thermal conductivity | W/m·K |
| $\alpha = k/(\rho C_p)$ | Thermal diffusivity | m²/s |
| $C_p$ | Specific heat (const. pressure) | J/kg·K |
| $q$ | Heat flux (per unit area) | W/m² |
| $Q$ | Heat transfer rate | W |

---

## 5b. Full Heat Equation for a Stationary Solid

Plugging Fourier's law into the energy conservation equation (and setting $\underline{v} = 0$ for a solid):

$$\rho C_p\left[\frac{\partial T}{\partial t} + \underline{v}\cdot\nabla T\right] = k\nabla^2 T + \dot{H}_v$$

For a **stationary solid**:

$$\boxed{\frac{\partial T}{\partial t} = \alpha\nabla^2 T + \frac{\dot{H}_v}{\rho C_p}}$$

where $\alpha = k/(\rho C_p)$ is the **thermal diffusivity** [m²/s], and $\nabla\cdot(\nabla T) = \nabla^2 T$.

**Special cases:**

| Condition | Equation | Name |
|-----------|----------|------|
| Steady state, no generation | $\nabla^2 T = 0$ | Laplace equation |
| Steady state, with generation | $\nabla^2 T + \dot{H}_v/k = 0$ | Poisson equation |
| Transient, no generation | $\partial T/\partial t = \alpha\nabla^2 T$ | Heat (diffusion) equation |

---

## 5c. Macroscopic Energy Balance

For a control volume, the macroscopic (global) energy balance is:

$$\dot{E}_{in} - \dot{E}_{out} + \dot{E}_{gen} = \frac{dE_{acc}}{dt}$$

**Steady state** means the three left-hand terms balance perfectly → no accumulation ($dE_{acc}/dt = 0$).

---

## 5d. Worked Example — 1D Slab (Fourier's Law)

A slab of material with $T_1 - T_2 = 12°C$ temperature difference, thickness $L$, thermal conductivity $k$:

$$q = -k\frac{dT}{dx} = -k\left(\frac{T_2 - T_1}{L}\right) = k\frac{T_1-T_2}{L}$$

$$q = 13.92\,\text{W/m}^2 \qquad Q = qA = 125.28\,\text{W}$$

(Assumption: steady-state, 1D conduction.)

---

## 5e. Composite Slab — Series Resistance

Three slabs A, B, C (same thickness $L$ each, conductivities $k_A$, $k_B$, $k_C$) in series. At steady state, **same flux passes through each slab**:

$$q = -k_A\!\left(\frac{T_2-T_1}{L}\right) = -k_B\!\left(\frac{T_3-T_2}{L}\right) = -k_C\!\left(\frac{T_4-T_3}{L}\right)$$

The slab with the **steepest temperature gradient** has the **lowest conductivity** (greatest resistance).

**Total thermal resistance** (series circuit):

$$R_{tot,th} = \frac{L}{k_A A} + \frac{L}{k_B A} + \frac{L}{k_C A}$$

The **electrical analogy** (p.7–8 of notes):

| Thermal | Electrical |
|---------|------------|
| Heat flow $Q$ | Current $I$ |
| Temperature difference $\Delta T$ | Potential difference $V$ |
| Thermal resistance $R_{th}$ | Resistance $R$ |

So: $Q = \Delta T / R_{th}$, exactly like $I = V/R$.

---

## 5f. Wall with Convection on Both Sides

A wall (thickness $L$, conductivity $k$) separating two fluids:

```
T∞,1  h1  [  wall  ]  h2  T∞,2
      Ts,1             Ts,2
```

At steady state, the same flux passes through all three resistances:

$$q = h_1(T_{\infty,1} - T_{s,1}) = -k\!\left(\frac{T_{s,2}-T_{s,1}}{L}\right) = h_2(T_{s,2} - T_{\infty,2})$$

Circuit: $\frac{1}{h_1 A} \rightarrow \frac{L}{kA} \rightarrow \frac{1}{h_2 A}$

---

## 5g. Complex Composite — Parallel and Series Blocks

For a 2D composite with blocks in series AND parallel (e.g., A→[B,C,D]→E→[F,G]):

The electrical circuit has parallel resistances for blocks at the same cross-section, connected in series with blocks spanning the full width. Draw the circuit, calculate equivalent parallel resistances first, then combine in series.

---

## 6. The "6 Equations" Count

The lecture notes specifically mention **6 equations** are needed:

1. Continuity (scalar) — 1 equation
2. Momentum (vector, 3 components) — 3 equations
3. Energy (scalar) — 1 equation
4. Constitutive for $\sigma$ (Newtonian fluid) — closes momentum
5. Constitutive for $q$ (Fourier's law) — closes energy

The system is then closed and solvable given appropriate boundary and initial conditions.

---

## Connected Modules

- **Module 1** applies Fourier's law to 1D conduction problems
- **Module 2** extends to 2D steady-state conduction
- **Module 5** uses the momentum equation in boundary layer analysis
- The energy equation in simplified form appears in every subsequent module
