# Module 8 — Free (Natural) Convection & Boiling
**Dates:** 30 Oct, 3 Nov, 6 Nov 2025  
**Sources:** `htoa2530oct.pdf`, `htoa2503nov.pdf`, `htoa2503nov_1.pdf`, `htoa256nov.pdf`, `htoa256nov_1.pdf`

**Textbooks:** Holman & Bhattacharya Ch. 5 & 7 · Incropera & DeWitt Ch. 9 · McCabe & Smith pp. 376–382 (Ch. 12)

---

## Overview

**Free (natural) convection** occurs when density differences caused by temperature gradients create buoyancy forces that drive fluid motion — no external pump or fan needed. **Boiling** is a phase-change process where heat transfer rates far exceed those of single-phase convection. Both phenomena are analysed in this module.

---

## Part A: Free (Natural) Convection

---

## A1. Physical Mechanism

When a vertical plate is at $T_s > T_\infty$:
- The fluid near the wall heats up → decreases in density
- Buoyancy force drives this lighter fluid upward
- A **velocity boundary layer** and **thermal boundary layer** develop simultaneously, driven by temperature gradient (not an external pressure gradient)

```
     T_s  > T_∞       T_s > T_∞
     ████             ████
     ████  ←δ→        ████  ←δt→
     ████  u(y)        ████  T(y)
     ████              ████
     ↑ x, u (upward)   quiescent fluid T∞, ρ∞
     → y, v
```

### Two Configurations on 30 Oct

**Case A ($T_1 < T_2$, bottom cold, top hot):** Unstable → fluid circulation, free convection.  
**Case B ($T_1 > T_2$, bottom hot, top cold):** Also unstable in vertical geometry (convection cells).

---

## A2. Governing Equations for Free Convection

### Momentum Equation (x-direction along plate)

$$\rho\left(u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y}\right) = -\frac{\partial p}{\partial x} - \rho g + \mu\frac{\partial^2 u}{\partial y^2}$$

Due to the thinness of the boundary layer, the pressure gradient $\partial p/\partial x \approx \partial p_\infty/\partial x = -\rho_\infty g$. Therefore:

$$u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y} = g\frac{(\rho_\infty - \rho)}{\rho} + \nu\frac{\partial^2 u}{\partial y^2}$$

### Boussinesq Approximation

For small temperature differences, the density variation is linearised:

**Volumetric thermal expansion coefficient:**

$$\beta = \frac{1}{V}\left(\frac{\partial V}{\partial T}\right)_p = -\frac{1}{\rho}\left(\frac{\partial \rho}{\partial T}\right)_p \qquad [K^{-1}]$$

**Boussinesq approximation:**

$$\beta \approx -\frac{1}{\rho}\frac{\Delta\rho}{\Delta T} = -\frac{1}{\rho}\frac{\rho_\infty - \rho}{T_\infty - T}$$

$$\boxed{(\rho_\infty - \rho) = \rho\beta(T - T_\infty)}$$

This replaces the density difference with a temperature difference, making the momentum and energy equations coupled but tractable.

**Substituted into momentum equation:**

$$u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y} = g\beta(T - T_\infty) + \nu\frac{\partial^2 u}{\partial y^2}$$

For an ideal gas: $\beta = 1/T$ [K⁻¹] where $T$ is in Kelvin.

---

## A3. Grashof Number

Dimensional analysis of the free convection momentum equation yields the **Grashof number**:

$$\boxed{Gr_L = \frac{g\beta(T_s - T_\infty)L^3}{\nu^2}}$$

Physical meaning:

$$Gr = \frac{\text{Buoyancy force}}{\text{Viscous force}^2} \sim \left(\frac{Re_L^2}{Re_L}\right) = Re^2 \text{ analog}$$

The Grashof number plays the same role in free convection as the **Reynolds number** plays in forced convection.

**The combined parameter:**

$$Ra_L = Gr_L \cdot Pr = \frac{g\beta(T_s - T_\infty)L^3}{\nu\alpha}$$

$Ra_L$ = **Rayleigh number** — the key parameter governing free convection.

**Transition to turbulence (vertical plate):**  
$Ra_L \approx 10^9$ — below this value, free convection BL is laminar.

---

## A4. Nusselt Number Correlations (Free Convection)

For a **vertical plate**:

$$\overline{Nu}_L = \left[0.825 + \frac{0.387\,Ra_L^{1/6}}{(1 + (0.492/Pr)^{9/16})^{8/27}}\right]^2$$

(Churchill & Chu correlation — valid for all $Ra_L$)

All properties evaluated at film temperature $T_f = (T_s + T_\infty)/2$.

---

## Part B: Boiling

## B0. What Makes Boiling Different from Single-Phase Convection (3 Nov tutorial)

**Sources:** Incropera & DeWitt Ch. 10 · Holman & Bhattacharya Ch. 9

Three key quantities that appear in boiling but not single-phase convection:
1. **Latent heat** $h_{fg}$ — energy absorbed per kg during phase change [J/kg]
2. **Surface tension** $\sigma$ at the liquid-vapour interface [N/m]
3. **Density difference** $(\rho_\ell - \rho_v)$ between the two phases

### Dimensionless Groups for Boiling

The Nusselt number for boiling is derived from the **Buckingham Π theorem** and depends on:

$$Nu_L = \frac{hL}{k} = f\!\left[\frac{\rho g(\rho_\ell - \rho_v)L^3}{\mu^2},\; Ja,\; Pr,\; Bo\right]$$

**Jakob Number (Ja):**

$$\boxed{Ja = \frac{C_p\,\Delta T}{h_{fg}} = \frac{\text{Max. sensible heat absorbed by liquid}}{\text{Latent energy absorbed by liquid during boiling}}}$$

where $\Delta T = |T_s - T_{sat}|$ = wall superheat.

- $Ja \ll 1$: latent heat dominates (efficient boiling)
- $Ja \sim 1$: sensible and latent comparable

**Bond Number (Bo):**

$$\boxed{Bo = \frac{g(\rho_\ell - \rho_v)L^2}{\sigma} = \frac{\text{Buoyancy force}}{\text{Surface tension force}}}$$

- Controls bubble size and detachment
- Large $Bo$: buoyancy dominates → bubbles detach easily
- Small $Bo$: surface tension dominant → bubbles cling to surface

---

## B1. What is Boiling?

Boiling is **phase change convection** — far higher heat transfer rates than single-phase convection because latent heat $h_{fg}$ is large. Applications: boilers, reactors, refrigeration evaporators.

---

## B2. Bubble Dynamics (3 Nov & 6 Nov)

### Forces on a Bubble

A spherical vapour bubble of radius $r$ inside a liquid pool:

- $p_v$: vapour pressure inside the bubble
- $p_\ell$: liquid pressure outside
- $\sigma$: surface tension of vapour-liquid interface [N/m]

**Work balance for bubble growth (3 Nov derivation):**

Initial surface area: $4\pi r^2$  
Increase surface area by $\Delta r$:

$$\Delta A = 8\pi r\,\Delta r$$

Work done against surface tension:

$$\delta W = \sigma\,\Delta A = 8\pi r\,\Delta r\,\sigma$$

Work done by net pressure:

$$\delta W = F\,\Delta r = (p_v - p_\ell)(4\pi r^2)\,\Delta r$$

Equating:

$$\boxed{p_v - p_\ell = \frac{2\sigma}{r}} \quad \text{(Young-Laplace equation)}$$

### Physical Interpretation

- For a bubble to exist in equilibrium: vapour pressure must exceed liquid pressure by $2\sigma/r$
- **Small bubbles** require a larger pressure excess (larger superheat)
- **Large bubbles** can exist at smaller pressure excess
- This means small nucleation sites require higher wall superheat to initiate boiling

### Bubble Fate (6 Nov)

Bubbles are **not always in thermal equilibrium** with the surrounding fluid. Vapour inside is not necessarily at the same temperature as the liquid outside.

Whether a bubble grows or collapses depends on the **local liquid temperature**:
- If liquid is superheated near the wall: bubble **grows and escapes to the surface**
- If liquid bulk is subcooled: bubble **collapses** back into the liquid

$$p_v - p_\ell = \frac{2\sigma}{r} \quad \text{(equilibrium condition)}$$

---

## B3. Boiling Regimes (Boiling Curve)

The **boiling curve** (Nukiyama curve) shows heat flux $q_s''$ vs wall superheat $\Delta T_e = T_s - T_{sat}$:

```
q''s (W/m²)
  |              C ●  ← Critical heat flux (CHF)
  |           ●     ●
  |        ●           ●  D (Leidenfrost point)
  |     ●                  ●
  | ●                           ●
  |                                   ●
  A                                        ●  B
  ──────────────────────────────────────────→  ΔTe
      FC   |  NB  |  TB  |  FB
```

| Region | Name | Mechanism | $q_s''$ |
|--------|------|-----------|---------|
| A–B | Free (single-phase) Convection | No phase change | Low |
| B–C | Nucleate Boiling (NB) | Bubbles nucleate, grow, detach | Rapidly increasing |
| C | **Critical Heat Flux (CHF)** | Vapour blanket begins to form | Maximum |
| C–D | Transition Boiling | Unstable film | Decreasing |
| D–E | **Film Boiling** | Stable vapour film | Increasing again |

**Critical Heat Flux** is the most important design point — exceeding CHF causes the surface to overheat dramatically (burnout).

---

## B4. Key Boiling Correlations

### Nucleate Boiling — Rohsenow Correlation

$$q_s'' = \mu_\ell h_{fg}\left[\frac{g(\rho_\ell - \rho_v)}{\sigma}\right]^{1/2}\left[\frac{C_{p,\ell}(T_s - T_{sat})}{C_{sf}h_{fg}Pr_\ell^n}\right]^3$$

where $C_{sf}$ = surface-fluid constant (tabulated), $n = 1$ for water, $n = 1.7$ for other fluids.

### Critical Heat Flux — Zuber Correlation

$$q_{max}'' = C_{cr}\,h_{fg}\,\rho_v\left[\frac{\sigma g(\rho_\ell - \rho_v)}{\rho_v^2}\right]^{1/4}$$

$C_{cr} = \pi/24 \approx 0.131$ for a large flat surface.

---

## Summary of Free Convection & Boiling Parameters

| Parameter | Symbol | Significance |
|-----------|--------|--------------|
| Thermal expansion coeff. | $\beta$ | Density variation with temperature |
| Grashof number | $Gr_L = g\beta(T_s-T_\infty)L^3/\nu^2$ | Buoyancy / viscous (analog of $Re^2$) |
| Rayleigh number | $Ra_L = Gr_L \cdot Pr$ | Key parameter for free convection |
| Saturation temperature | $T_{sat}$ | Boiling point at given pressure |
| Wall superheat | $\Delta T_e = T_s - T_{sat}$ | Driving force for boiling |
| Latent heat | $h_{fg}$ | Energy per unit mass for vaporisation |
| Surface tension | $\sigma$ | Controls bubble equilibrium radius |
| Young-Laplace | $p_v - p_\ell = 2\sigma/r$ | Bubble pressure–size relation |

---

## Textbook References

- **Incropera & DeWitt:** Chapter 9 (Free Convection), Chapter 10 (Boiling & Condensation)
- **Holman & Bhattacharya:** Chapters 5 & 7
- **McCabe & Smith:** Chapter 12, pp. 376–382

---

## Connected Modules

- [Module 4](05_convection_external.md) — Forced convection BL; free convection adds buoyancy body force
- [Module 9](10_condensation.md) — Condensation is the reverse of boiling; same fluid properties
