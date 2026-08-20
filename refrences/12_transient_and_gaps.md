# Module 11 — Transient Conduction & Remaining Gaps
**Status:** Supplementary module — topics absent or only partially covered in lecture notes  
**Textbooks:** Incropera & DeWitt Ch. 5 (Transient), Ch. 7 (External flow — cylinders, spheres), Ch. 6 (Dimensional analysis)

---

## Overview

Three classical Heat Transfer topics were missing from the HTOA 2025 notes:

1. **Transient (unsteady) conduction beyond lumped capacitance** — Heisler chart solutions for plane walls, long cylinders, and spheres when $Bi > 0.1$; semi-infinite solid; product solution for multi-dimensional transient.
2. **External forced convection over non-flat geometries** — cylinders in cross-flow, spheres, and tube banks (the flat plate was covered; cylinders and spheres were not).
3. **Dimensional analysis and the Buckingham Π theorem** — how the dimensionless groups ($Re$, $Nu$, $Pr$, etc.) arise systematically from the governing equations.

---

## Part A — Transient Conduction

---

## A1. The Two Regimes

The **Biot number** $Bi = hL_c/k$ (where $L_c = V/A_s$) partitions transient problems into two regimes:

| $Bi$ | Physical meaning | Method |
|------|-----------------|--------|
| $Bi < 0.1$ | Solid nearly isothermal; surface resistance dominates | **Lumped capacitance** (covered in Module 3) |
| $Bi \ge 0.1$ | Significant temperature gradients inside solid | **Exact series / Heisler charts** |

The lumped capacitance result (covered in Module 3):

$$\frac{T - T_\infty}{T_i - T_\infty} = \exp\!\left(-\frac{t}{\tau}\right), \quad \tau = \frac{\rho C_p V}{hA_s}$$

Everything below applies when $Bi \ge 0.1$.

---

## A2. Exact Series Solution — Plane Wall

**Setup:** Plane wall of half-thickness $L$ (total thickness $2L$), initially uniform at $T_i$, suddenly exposed on both faces to fluid at $T_\infty$ with convection coefficient $h$.

**Governing PDE:**

$$\frac{\partial T}{\partial t} = \alpha \frac{\partial^2 T}{\partial x^2}, \qquad 0 \le x \le L$$

**Boundary conditions:**
- Symmetry: $\partial T/\partial x = 0$ at $x = 0$
- Convection: $-k\,\partial T/\partial x = h(T - T_\infty)$ at $x = L$

**Dimensionless variables:**

$$\Theta^* = \frac{T - T_\infty}{T_i - T_\infty}, \quad x^* = \frac{x}{L}, \quad Fo = \frac{\alpha t}{L^2}, \quad Bi = \frac{hL}{k}$$

$Fo$ is the **Fourier number** — dimensionless time representing how far heat has diffused relative to the body size.

**Exact solution (series):**

$$\boxed{\Theta^*(x^*, Fo, Bi) = \sum_{n=1}^{\infty} C_n \exp(-\zeta_n^2 Fo)\cos(\zeta_n x^*)}$$

where:
- $\zeta_n$ are the **eigenvalues** (roots of the transcendental equation): $\zeta_n \tan(\zeta_n) = Bi$
- Coefficients: $C_n = \dfrac{4\sin(\zeta_n)}{2\zeta_n + \sin(2\zeta_n)}$

**For $Fo > 0.2$ (one-term approximation is excellent):**

$$\Theta^* \approx C_1 \exp(-\zeta_1^2 Fo)\cos(\zeta_1 x^*)$$

- **Centreline** ($x^* = 0$): $\Theta^*_0 = C_1\exp(-\zeta_1^2 Fo)$
- **Surface** ($x^* = 1$): $\Theta^*_s = \Theta^*_0 \cos(\zeta_1)$

The first eigenvalue $\zeta_1$ and coefficient $C_1$ are tabulated as functions of $Bi$ (Table 5.1 in Incropera & DeWitt):

| $Bi$ | $\zeta_1$ (rad) | $C_1$ |
|------|----------------|-------|
| 0.1 | 0.3111 | 1.0160 |
| 0.5 | 0.6533 | 1.0701 |
| 1.0 | 0.8603 | 1.1191 |
| 5.0 | 1.3138 | 1.2479 |
| 10.0 | 1.4289 | 1.2620 |
| $\infty$ (const. $T_s$) | $\pi/2$ | 1.2733 |

### Total Energy Stored/Released

The total heat transferred from the wall up to time $t$:

$$\frac{Q}{Q_0} = 1 - \Theta^*_0 \frac{\sin(\zeta_1)}{\zeta_1}$$

where $Q_0 = \rho C_p V (T_i - T_\infty)$ = initial stored energy relative to fluid.

---

## A3. Exact Series Solution — Long Cylinder and Sphere

The same approach applies to a **long cylinder** (radius $r_o$) and **sphere** (radius $r_o$), initially at $T_i$, exposed to fluid at $T_\infty$:

**Dimensionless time:** $Fo = \alpha t / r_o^2$ (note: $r_o$ replaces $L$)

**Biot number:** $Bi = h r_o / k$

### Long Cylinder — One-Term Approximation ($Fo > 0.2$):

$$\Theta^* \approx C_1 \exp(-\zeta_1^2 Fo) J_0(\zeta_1 r^*)$$

where $J_0$ = Bessel function of the first kind, order zero; $r^* = r/r_o$.

Eigenvalues from: $\zeta_1 J_1(\zeta_1) = Bi \cdot J_0(\zeta_1)$

**Centreline ($r^* = 0$):** $\Theta^*_0 = C_1\exp(-\zeta_1^2 Fo)$ (since $J_0(0) = 1$)

### Sphere — One-Term Approximation ($Fo > 0.2$):

$$\Theta^* \approx C_1 \exp(-\zeta_1^2 Fo) \frac{\sin(\zeta_1 r^*)}{\zeta_1 r^*}$$

Eigenvalues from: $1 - \zeta_1\cot(\zeta_1) = Bi$

**Centre ($r^* = 0$):** $\Theta^*_0 = C_1\exp(-\zeta_1^2 Fo)$ (L'Hôpital gives $\sin(\zeta_1 r^*)/(\zeta_1 r^*) \to 1$ as $r^* \to 0$)

---

## A4. Heisler Charts

Before computing was ubiquitous, these solutions were read off **Heisler charts** — log-scale plots of $\Theta^*_0$ vs $Fo$ with $1/Bi$ as a parameter. They exist for:
- Plane wall (centreline and surface)
- Long cylinder (centreline and surface)  
- Sphere (centre and surface)

**Reading procedure:**
1. Compute $Fo = \alpha t / L_c^2$ and $1/Bi = k/(hL_c)$
2. Read $\Theta^*_0$ from chart
3. If surface temperature needed, read a second chart for $\Theta^*/\Theta^*_0$ at $x^* = 1$

Modern practice: use the one-term approximation analytically (valid for $Fo > 0.2$) or software. Charts are useful for quick estimates.

---

## A5. Semi-Infinite Solid

**Setup:** A solid occupying $x \ge 0$, initially uniform at $T_i$. At $t = 0$, either:
- **(a)** Surface suddenly set to constant $T_s$
- **(b)** Surface subjected to constant heat flux $q_s''$
- **(c)** Surface subjected to convection from fluid at $T_\infty$ with coefficient $h$

The solid extends to $x \to \infty$ — no far-field temperature change during the time of interest.

**Governing equation:**

$$\frac{\partial T}{\partial t} = \alpha\frac{\partial^2 T}{\partial x^2}, \quad 0 \le x < \infty$$

**Key similarity variable:** $\eta = \frac{x}{2\sqrt{\alpha t}}$

### Case (a): Sudden change in surface temperature ($T_s = $ const)

$$\boxed{\frac{T(x,t) - T_s}{T_i - T_s} = \text{erf}\!\left(\frac{x}{2\sqrt{\alpha t}}\right)}$$

- $\text{erf}(\eta) = \frac{2}{\sqrt{\pi}}\int_0^\eta e^{-u^2}du$ = **Gauss error function** (tabulated)
- Surface heat flux: $q_s'' = \frac{k(T_s - T_i)}{\sqrt{\pi\alpha t}}$ (decays as $t^{-1/2}$)

### Case (b): Constant surface heat flux $q_s''$

$$T(x,t) - T_i = \frac{2q_s''\sqrt{\alpha t/\pi}}{k}\exp\!\left(-\frac{x^2}{4\alpha t}\right) - \frac{q_s'' x}{k}\,\text{erfc}\!\left(\frac{x}{2\sqrt{\alpha t}}\right)$$

where $\text{erfc}(\eta) = 1 - \text{erf}(\eta)$.

### Case (c): Convection at the surface

$$\frac{T(x,t) - T_i}{T_\infty - T_i} = \text{erfc}\!\left(\frac{x}{2\sqrt{\alpha t}}\right) - \exp\!\left(hx/k + h^2\alpha t/k^2\right)\text{erfc}\!\left(\frac{x}{2\sqrt{\alpha t}} + \frac{h\sqrt{\alpha t}}{k}\right)$$

The combination $h\sqrt{\alpha t}/k$ appears naturally — it is the ratio of heat penetration depth to $k/h$ (convective length scale).

**When is a body semi-infinite?** When the thermal penetration depth $\delta_t \approx 4\sqrt{\alpha t}$ is much less than the body thickness $L$:

$$4\sqrt{\alpha t} \ll L \quad \Longleftrightarrow \quad Fo = \frac{\alpha t}{L^2} \ll \frac{1}{16}$$

---

## A6. Multi-Dimensional Transient — Product Solution

For a **finite body** (e.g., a rectangular block, short cylinder), the transient solution is the **product** of the 1D solutions for each direction.

**Short cylinder** (radius $r_o$, half-length $L$):

$$\Theta^*(r, x, t) = \Theta^*_\text{plane wall}(x, t) \times \Theta^*_\text{long cylinder}(r, t)$$

**Rectangular block** (half-dimensions $L_1$, $L_2$, $L_3$):

$$\Theta^* = \Theta^*_{PW}(x_1, t) \times \Theta^*_{PW}(x_2, t) \times \Theta^*_{PW}(x_3, t)$$

**Total heat transfer** (product method for $Q/Q_0$):

$$\left(\frac{Q}{Q_0}\right)_{SC} = \left(\frac{Q}{Q_0}\right)_{PW} + \left(\frac{Q}{Q_0}\right)_{LC}\left[1 - \left(\frac{Q}{Q_0}\right)_{PW}\right]$$

This is valid because the PDE is linear and the geometry is separable — each 1D solution is independent.

---

## A7. Fourier Number — Physical Meaning

$$\boxed{Fo = \frac{\alpha t}{L_c^2} = \frac{\text{Rate of heat conduction across }L_c}{\text{Rate of energy storage}} = \frac{t}{\tau_{diff}}}$$

where $\tau_{diff} = L_c^2/\alpha$ is the diffusion time scale.

- $Fo \ll 1$: heat has barely penetrated — semi-infinite approximation good
- $Fo > 0.2$: one-term series approximation sufficient (error < 2%)
- $Fo \gg 1$: nearly equilibrated with surroundings

---

## A8. Summary — Transient Problem Decision Tree

```
Given: solid body, initial T_i, suddenly exposed to T∞ with h
         |
         ↓
    Compute Bi = h·Lc/k  (Lc = V/As)
         |
    Bi < 0.1?
    YES → Lumped capacitance:  T(t) = T∞ + (Ti-T∞)exp(-t/τ)
    NO  → Significant internal gradients
         |
         ↓
    Is Fo > 0.2?
    YES → One-term approximation (use Table 5.1)
    NO  → Full series or Heisler chart
         |
         ↓
    Geometry:
    Plane wall  → Θ* = C1 exp(-ζ1²Fo)cos(ζ1 x*)
    Long cyl.   → Θ* = C1 exp(-ζ1²Fo)J0(ζ1 r*)
    Sphere      → Θ* = C1 exp(-ζ1²Fo)sin(ζ1r*)/(ζ1r*)
    Semi-inf.   → use erf solution (only if Fo ≪ 1/16)
    2D/3D body  → product solution
```

---

## Part B — External Convection: Cylinders, Spheres, Tube Banks

---

## B1. Cylinder in Cross-Flow

**Setup:** Long circular cylinder (diameter $D$) with fluid approaching at free-stream velocity $u_\infty$, $T_\infty$; surface temperature $T_s$.

Unlike the flat plate, the **boundary layer separates** from the cylinder surface (typically at ~$80°$ from the stagnation point in laminar flow, earlier in turbulent), creating a wake. This makes the local $h$ highly non-uniform around the circumference — but we use the **average** correlation.

### Churchill-Bernstein Correlation (all $Re$, all $Pr$):

$$\boxed{\overline{Nu}_D = 0.3 + \frac{0.62\,Re_D^{1/2}\,Pr^{1/3}}{\left[1+(0.4/Pr)^{2/3}\right]^{1/4}}\left[1+\left(\frac{Re_D}{282000}\right)^{5/8}\right]^{4/5}}$$

Valid for: $Re_D\,Pr \ge 0.2$ (essentially all engineering conditions).  
Properties at film temperature $T_f = (T_s + T_\infty)/2$.

### Hilpert Correlation (simpler, for specific $Re$ ranges):

$$\overline{Nu}_D = C\,Re_D^m\,Pr^{1/3}$$

| $Re_D$ | $C$ | $m$ |
|--------|-----|-----|
| 0.4–4 | 0.989 | 0.330 |
| 4–40 | 0.911 | 0.385 |
| 40–4000 | 0.683 | 0.466 |
| 4000–40,000 | 0.193 | 0.618 |
| 40,000–400,000 | 0.027 | 0.805 |

Properties at film temperature $T_f$.

---

## B2. Sphere in External Flow

**Setup:** Sphere of diameter $D$ in uniform flow $u_\infty$, $T_\infty$; surface at $T_s$.

### Whitaker Correlation:

$$\boxed{\overline{Nu}_D = 2 + (0.4\,Re_D^{1/2} + 0.06\,Re_D^{2/3})\,Pr^{0.4}\left(\frac{\mu}{\mu_s}\right)^{1/4}}$$

Valid for: $3.5 \le Re_D \le 7.6\times10^4$, $0.71 \le Pr \le 380$, $1.0 \le (\mu/\mu_s) \le 3.2$

- All properties at $T_\infty$ except $\mu_s$ at $T_s$
- Limiting value: $\overline{Nu}_D \to 2$ as $Re_D \to 0$ (pure conduction from a sphere in a stagnant medium)

**Why $Nu \to 2$ for conduction limit?** From the exact conduction solution for a sphere of radius $r_o$ in an infinite medium: $h = k/r_o$, so $Nu = hD/k = 2$. This is the theoretical minimum.

---

## B3. Tube Banks in Cross-Flow

**Setup:** An array of $N$ rows of tubes (diameter $D$, staggered or in-line arrangement) with fluid flowing across them. Used in heat exchangers, boiler/condenser tube banks.

### Geometry Parameters

```
In-line arrangement:        Staggered arrangement:
  o   o   o                   o   o   o
  o   o   o                     o   o   o
  o   o   o                   o   o   o
←─ST─→                      ←─ST─→
  ↕ SL                         ↕ SL
```

- $S_T$ = transverse pitch (perpendicular to flow)
- $S_L$ = longitudinal pitch (parallel to flow)
- $A_{1,max}$: maximum flow area (minimum cross-section)

**Maximum velocity** (used in $Re$):

$$u_{max} = u_\infty \frac{S_T}{S_T - D} \quad \text{(in-line)}$$

For staggered, check if diagonal or transverse passage is narrower.

### Zukauskas Correlation:

$$\overline{Nu}_D = C_1 C_2\,Re_{D,max}^m\,Pr^{0.36}\left(\frac{Pr}{Pr_s}\right)^{0.25}$$

where $Re_{D,max} = \rho u_{max} D/\mu$ uses the **maximum velocity**.

Constants $C_1$, $m$ from Table 7.2 in Incropera & DeWitt (depend on arrangement and $Re$ range):

| Arrangement | $Re_{D,max}$ | $C_1$ | $m$ |
|-------------|-------------|-------|-----|
| In-line | 100–10⁵ | 0.27 | 0.63 |
| Staggered ($S_T/S_L < 2$) | 10³–2×10⁵ | 0.35$(S_T/S_L)^{1/5}$ | 0.60 |
| Staggered ($S_T/S_L \ge 2$) | 10³–2×10⁵ | 0.40 | 0.60 |

$C_2$ = row correction factor for $N < 20$ rows:

| $N$ rows | 1 | 2 | 3 | 4 | 7 | 10 | 13 | $\ge$20 |
|----------|---|---|---|---|---|----|----|---------|
| $C_2$ (in-line) | 0.70 | 0.80 | 0.86 | 0.90 | 0.96 | 0.98 | 0.99 | 1.00 |
| $C_2$ (staggered) | 0.64 | 0.76 | 0.84 | 0.89 | 0.96 | 0.98 | 0.99 | 1.00 |

Properties at arithmetic mean of inlet/outlet fluid temperatures; $Pr_s$ at tube surface temperature.

### Tube Bank Energy Balance

Fluid temperature rise across the bank:

$$T_{o} - T_{i} = (T_s - T_i)\left[1 - \exp\!\left(-\frac{\pi D N \bar{h}}{\rho u_\infty S_T C_p}\right)\right]$$

Or using LMTD approach:

$$q = \bar{h} A_{total} \Delta T_{lm}, \quad A_{total} = N_{total}\pi D L$$

$$\Delta T_{lm} = \frac{(T_s - T_i) - (T_s - T_o)}{\ln[(T_s - T_i)/(T_s - T_o)]}$$

---

## Part C — Dimensional Analysis and the Buckingham Π Theorem

---

## C1. Why Dimensional Analysis?

The dimensionless groups ($Re$, $Nu$, $Pr$, $Bi$, $Gr$, etc.) are not arbitrary — they arise naturally from the governing equations and from dimensional analysis. The **Buckingham Π theorem** provides a systematic method to find these groups.

---

## C2. Buckingham Π Theorem

**Statement:** If a physical phenomenon involves $n$ variables with $r$ independent fundamental dimensions (usually M, L, T, θ — mass, length, time, temperature), then the phenomenon can be described by:

$$\Pi = n - r \quad \text{independent dimensionless groups (Π-groups)}$$

**Procedure:**
1. List all $n$ relevant variables with their dimensions
2. Identify $r$ independent dimensions
3. Choose $r$ **repeating variables** (must span all dimensions)
4. Form each Π-group by multiplying one non-repeating variable with the repeating variables raised to unknown powers
5. Solve for powers by requiring each Π-group to be dimensionless
6. Express the physical relation as $\Pi_1 = f(\Pi_2, \Pi_3, \ldots)$

---

## C3. Derivation of $Nu = f(Re, Pr)$ for Forced Convection

**Step 1 — Relevant variables:** $h$, $L$, $k$, $\rho$, $\mu$, $C_p$, $u_\infty$

$n = 7$ variables

**Step 2 — Dimensions** (using M, L, t, θ):

| Variable | Dimensions |
|----------|-----------|
| $h$ | M t⁻³ θ⁻¹ |
| $L$ | L |
| $k$ | M L t⁻³ θ⁻¹ |
| $\rho$ | M L⁻³ |
| $\mu$ | M L⁻¹ t⁻¹ |
| $C_p$ | L² t⁻² θ⁻¹ |
| $u_\infty$ | L t⁻¹ |

$r = 4$ dimensions (M, L, t, θ) → $\Pi = 7 - 4 = 3$ groups

**Step 3 — Repeating variables:** Choose $\rho$, $u_\infty$, $L$, $k$ (span all 4 dimensions)

**Step 4 — Form the Π-groups:**

$\Pi_1 = h \cdot \rho^a u_\infty^b L^c k^d$ → solving: $\Pi_1 = \dfrac{hL}{k} = Nu$

$\Pi_2 = \mu \cdot \rho^a u_\infty^b L^c k^d$ → solving: $\Pi_2 = \dfrac{\rho u_\infty L}{\mu} = Re$

$\Pi_3 = C_p \cdot \rho^a u_\infty^b L^c k^d$ → solving: $\Pi_3 = \dfrac{\mu C_p}{k} = Pr$

**Result:**

$$Nu = f(Re, Pr) \quad \text{— all forced convection correlations have this form}$$

---

## C4. Derivation of $Nu = f(Gr, Pr)$ for Free Convection

For free convection, $u_\infty$ is replaced by buoyancy. The relevant variables are $h$, $L$, $k$, $\rho$, $\mu$, $C_p$, $g\beta\Delta T$ (the buoyancy group — has dimensions L t⁻²).

Applying the Π theorem:

$$Nu = f(Gr, Pr), \quad Gr = \frac{g\beta\Delta T L^3}{\nu^2}$$

$Ra = Gr\cdot Pr$ emerges as the natural combination because $Nu$ is often correlated as $Nu \sim Ra^n$.

---

## C5. Why These Groups Have Physical Meaning

| Group | Derived ratio | Physical interpretation |
|-------|--------------|------------------------|
| $Re = \rho u L/\mu$ | Inertia / Viscous | Controls flow regime (laminar vs turbulent) |
| $Nu = hL/k$ | Convective HT / Conductive HT | Non-dim. heat transfer coefficient |
| $Pr = \nu/\alpha$ | Momentum diffusivity / Thermal diffusivity | Relative BL thicknesses |
| $Gr = g\beta\Delta T L^3/\nu^2$ | Buoyancy / Viscous² | Natural convection driving force |
| $Bi = hL/k_{solid}$ | Surface convection / Internal conduction | Temperature uniformity in solid |
| $Fo = \alpha t/L^2$ | Thermal diffusion rate / Stored energy | Dimensionless time in transient |
| $St = h/(\rho u C_p)$ | HT / Enthalpy flux | $= Nu/(Re\cdot Pr)$ |
| $Ja = C_p\Delta T/h_{fg}$ | Sensible / Latent heat | Phase-change intensity |
| $Bo = g\Delta\rho L^2/\sigma$ | Buoyancy / Surface tension | Bubble/droplet size |

---

## Part D — Mass Transfer Analogy (Brief)

---

## D1. Heat-Mass Transfer Analogy

The governing equations for heat transfer and mass transfer are mathematically identical in form. This means every heat transfer correlation has a **direct mass transfer analog** obtained by substituting:

| Heat Transfer | Mass Transfer |
|--------------|--------------|
| $Nu = hL/k$ | $Sh = h_m L/D_{AB}$ (Sherwood number) |
| $Pr = \nu/\alpha$ | $Sc = \nu/D_{AB}$ (Schmidt number) |
| $St = h/(\rho u C_p)$ | $St_m = h_m/u$ (mass transfer Stanton) |
| $j_H = St\,Pr^{2/3}$ | $j_m = St_m\,Sc^{2/3}$ |

**Lewis number:** $Le = Sc/Pr = \alpha/D_{AB}$ — ratio of thermal to mass diffusivity.

**Example:** The flat plate laminar correlation $\overline{Nu}_L = 0.664\,Re_L^{1/2}\,Pr^{1/3}$ becomes $\overline{Sh}_L = 0.664\,Re_L^{1/2}\,Sc^{1/3}$ for mass transfer.

The **Colburn analogy** (already in Module 5) is the practical bridge:

$$j_H = j_m \implies \frac{h}{\rho u C_p}Pr^{2/3} = \frac{h_m}{u}Sc^{2/3}$$

This allows estimation of mass transfer coefficients from heat transfer data, and vice versa.

---

## Summary — All Gaps Now Covered

### Transient Conduction

| Topic | Formula/Method |
|-------|---------------|
| Lumped capacitance ($Bi < 0.1$) | $\Theta^* = e^{-t/\tau}$ — Module 3 |
| Plane wall ($Bi \ge 0.1$, $Fo > 0.2$) | $\Theta^* = C_1 e^{-\zeta_1^2 Fo}\cos(\zeta_1 x^*)$ |
| Long cylinder ($Fo > 0.2$) | $\Theta^* = C_1 e^{-\zeta_1^2 Fo}J_0(\zeta_1 r^*)$ |
| Sphere ($Fo > 0.2$) | $\Theta^* = C_1 e^{-\zeta_1^2 Fo}\sin(\zeta_1 r^*)/(\zeta_1 r^*)$ |
| Semi-infinite solid | $\Theta^* = \text{erf}(x/2\sqrt{\alpha t})$ |
| Multi-dimensional | Product solution |
| Fourier number | $Fo = \alpha t/L_c^2$ |

### External Convection — Non-Flat Geometries

| Geometry | Correlation |
|----------|------------|
| Cylinder in cross-flow | Churchill-Bernstein or Hilpert |
| Sphere | Whitaker ($Nu \to 2$ for $Re \to 0$) |
| Tube banks | Zukauskas with $u_{max}$, row correction $C_2$ |

### Dimensional Analysis

| Topic | Key result |
|-------|-----------|
| Buckingham Π theorem | $\Pi = n - r$ groups |
| Forced convection | $Nu = f(Re, Pr)$ — derived from Π theorem |
| Free convection | $Nu = f(Gr, Pr)$ — buoyancy replaces $u_\infty$ |
| Mass transfer analogy | $Nu \leftrightarrow Sh$, $Pr \leftrightarrow Sc$ |

---

## Complete Course Gap Audit

With Modules 10 (Radiation) and 11 (this file), the notes now cover all standard classical Heat Transfer topics:

| Classical Topic | Status |
|----------------|--------|
| Conduction — 1D steady | ✅ Module 1 |
| Conduction — 2D steady (separation of variables) | ✅ Module 2 |
| Conduction — FDM numerical | ✅ Module 3 |
| Transient — lumped capacitance | ✅ Module 3 |
| Transient — Heisler / one-term series | ✅ **This module §A** |
| Transient — semi-infinite solid (erf) | ✅ **This module §A5** |
| Transient — product solution | ✅ **This module §A6** |
| Convection — external, flat plate | ✅ Module 4 |
| Convection — external, cylinder in cross-flow | ✅ **This module §B1** |
| Convection — external, sphere | ✅ **This module §B2** |
| Convection — external, tube banks | ✅ **This module §B3** |
| Convection — internal, laminar | ✅ Module 5 |
| Convection — internal, turbulent (Dittus-Boelter) | ✅ Module 5 |
| Natural / free convection | ✅ Module 8 |
| Fins / extended surfaces | ✅ Module 6 |
| Heat exchangers (LMTD, ε-NTU) | ✅ Module 7 |
| Boiling | ✅ Module 8 |
| Condensation | ✅ Module 9 |
| Evaporation | ✅ Module 9 |
| Radiation — blackbody laws, Wien, Stefan-Boltzmann | ✅ Module 10 |
| Radiation — surface properties, Kirchhoff | ✅ Module 10 |
| Radiation — view factors, network method | ✅ Module 10 |
| Radiation — shields, combined modes | ✅ Module 10 |
| Dimensional analysis (Buckingham Π) | ✅ **This module §C** |
| Mass transfer analogy | ✅ **This module §D** |

---

## Textbook References

- **Incropera & DeWitt:** Ch. 5 (Transient Conduction), Ch. 7 (External Flow — cylinders & spheres), Ch. 6 §6.2 (Dimensional analysis)
- **Holman & Bhattacharya:** Ch. 4 (Unsteady heat conduction), Ch. 6 (Flow over bodies)
- **Cengel & Ghajar:** Ch. 4 (Transient), Ch. 7 (External flow)

---

## Connected Modules

- [Module 3](04_conduction_numerical.md) — Lumped capacitance; Biot number; basis for §A here
- [Module 4](05_convection_external.md) — Flat plate; same dimensionless groups extended to cylinders/spheres here
- [Module 5](06_convection_internal.md) — Colburn analogy extended to mass transfer in §D
- [Module 10](11_radiation.md) — Radiation; completes the three-mode picture
