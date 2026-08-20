# Module 4 — Convection: Boundary Layers & External Flow
**Dates:** 14 Aug, 18 Aug, 20 Aug, 21 Aug 2025  
**Sources:** `htoa2514aug.pdf`, `htoa2518aug.pdf`, `htoa2520aug.pdf`, `htoa2521aug.pdf`

---

## Overview

External forced convection occurs when a fluid flows over a surface driven by an external mechanism (fan, pump, freestream). The key physics lies in the **boundary layer** — a thin region near the surface where velocity and temperature change from surface values to freestream values. This module covers boundary layer theory, key dimensionless groups, and the flat plate correlations.

---

## 1. Velocity Boundary Layer

### Physical Description

When a fluid stream ($u_\infty$, $T_\infty$) flows over a stationary plate, a **velocity boundary layer** develops from the leading edge ($x = 0$):

```
u∞ ——→  ——→  ——→  ——→  ——→
         Laminar  | Turbulent
 y ↑               |
   |    ←δ(x)→     xc              L
 0 ●───────────────────────────────→ x
   (no-slip: u = 0 at wall)
```

- **Boundary layer thickness** $\delta(x)$: the $y$-distance at which $u = 0.99\, u_\infty$
- $\delta$ grows in the $x$-direction
- Flow transitions from **laminar → turbulent** at the critical Reynolds number

### Reynolds Numbers

**Local Reynolds number:**
$$Re_x = \frac{\rho u_\infty x}{\mu} = \frac{u_\infty x}{\nu}$$

**Plate-length Reynolds number:**
$$Re_L = \frac{\rho u_\infty L}{\mu}$$

**Critical Reynolds number (transition):**
$$\boxed{Re_{x_c} = 5 \times 10^5}$$

### Boundary Layer Regime Rules (from lecture notes)

- If $0.95 < x_c/L \le 1$: assume **entire plate is laminar**
- If $x_c/L < 0.95$ (i.e., $x_c/L < 0.95$): **mixed boundary layer** (laminar then turbulent)

---

## 2. Thermal Boundary Layer

### Physical Description

If the surface temperature $T_s \neq T_\infty$, a **thermal boundary layer** of thickness $\delta_t$ develops alongside the velocity boundary layer:

- Defined as the $y$-distance at which:

$$\frac{T_s - T}{T_s - T_\infty} = 0.99$$

- The thermal BL grows similarly to the velocity BL but at a different rate

### Trend Along the Plate

As distance $x$ from the leading edge increases:
$$x \uparrow \implies \delta_t \uparrow \implies \left.\frac{\partial T}{\partial y}\right|_{y=0} \downarrow \implies q \downarrow \implies \boxed{h \downarrow}$$

The local heat transfer coefficient $h_x$ **decreases** along the plate — the boundary layer thickens and becomes a poorer conductor of heat to/from the surface.

---

## 3. Local Heat Transfer Coefficient

At any point $x$ on the plate, equate the conduction at the wall with Newton's cooling law:

$$q = -k_f \left.\frac{\partial T}{\partial y}\right|_{y=0} = h_x(T_s - T_\infty)$$

**Local heat transfer coefficient:**

$$\boxed{h_x = \frac{-k_f \left[\partial T/\partial y\right]_{y=0}}{T_s - T_\infty}}$$

where $k_f$ = thermal conductivity of the **fluid** (not the solid).

---

## 4. Key Dimensionless Groups

### Nusselt Number

$$Nu_x = \frac{h_x x}{k_f} = \frac{\text{Convective heat transfer}}{\text{Conductive heat transfer}}$$

### Prandtl Number

$$Pr = \frac{\mu C_p}{k} = \frac{\nu}{\alpha} = \frac{\text{Momentum diffusivity}}{\text{Thermal diffusivity}}$$

- $Pr > 1$: velocity BL is thicker than thermal BL (e.g., oil, $Pr \sim 100$–1000)
- $Pr < 1$: thermal BL is thicker (e.g., liquid metals, $Pr \sim 0.001$–0.1)
- $Pr \approx 1$: similar thicknesses (e.g., air, $Pr \approx 0.7$)

Relation between BL thicknesses:

$$\frac{\delta}{\delta_t} \approx Pr^{1/3}$$

---

## 5. Flat Plate Correlations

### 5.1 Laminar Flow Over Entire Plate

**Average Nusselt number** (18 Aug lecture):

$$\overline{Nu}_L = 2\,Nu_x\big|_{x=L} = 0.664\,Re_L^{1/2}\,Pr^{1/3}$$

- Valid for: $Pr > 1$ (also approximately valid for gases with $Pr \approx 0.7$)
- Strictly: **$Pr \ge 1$** (note from lectures)

**Local Nusselt number** (20 Aug lecture):

$$Nu_x = \frac{h_x x}{k} = 0.453\,Re_x^{1/2}\,Pr^{1/3}$$

Since $h_x \sim x^{-1/2}$, the **local h decreases** along the plate:

$$h_x \sim x^{-1/2} \implies \text{minimum } h_x \text{ is at the last (farthest) point}$$

**Practical consequence (chip cooling example, 20 Aug):**

> "Minimum $h_x$ is for the last chip. If we ensure that the last chip does not exceed 80°C during operation, preceding chips will be safe."

### 5.2 Film Temperature

All fluid properties ($\nu$, $k$, $\mu$, $Pr$) are evaluated at the **film temperature**:

$$T_f = \frac{T_s + T_\infty}{2}$$

**Example (21 Aug):** $T_s = 350\,\text{K}$, $T_\infty = 300\,\text{K}$, so $T_f = 325\,\text{K}$.  
From Table A-4 in Incropera & DeWitt (air at 1 atm, $T_f = 325\,\text{K}$):
- $\nu = 18.41 \times 10^{-6}\,\text{m}^2/\text{s}$
- $k = 28.2 \times 10^{-3}\,\text{W/mK}$
- $Pr = 0.704$

### 5.3 Mixed Boundary Layer (Laminar + Turbulent)

When $x_c/L < 0.95$, use the mixed correlation:

$$\overline{Nu}_L = (0.037\,Re_L^{4/5} - A)\,Pr^{1/3}$$

where $A = 0.037\,Re_{x_c}^{4/5} - 0.664\,Re_{x_c}^{1/2}$ accounts for the laminar portion.

For $Re_{x_c} = 5 \times 10^5$: $A = 871$ (tabulated result).

### 5.4 Fully Turbulent Plate ($L \gg x_c$)

When $Re_L \gg Re_{x_c}$ (plate much longer than transition point), the entire plate is effectively turbulent:

$$\boxed{\overline{Nu}_L = 0.037\,Re_L^{4/5}\,Pr^{1/3}}$$

Valid for: $5\times10^5 < Re_L < 10^8$, $0.6 \le Pr \le 60$

### 5.5 Constant Heat Flux Boundary Condition

For a plate with **uniform heat flux** $q_s'' = \text{const}$ (rather than constant $T_s$):

| Regime | Local $Nu_x$ | Validity |
|--------|-------------|---------|
| Laminar | $Nu_x = 0.453\,Re_x^{1/2}\,Pr^{1/3}$ | $Pr \ge 0.6$ |
| Turbulent | $Nu_x = 0.0308\,Re_x^{4/5}\,Pr^{1/3}$ | $0.6 \le Pr \le 60$ |

The coefficient changes from 0.453 (const. $T_s$) to 0.453 (same for laminar! — note: it is identical for laminar), but differs for turbulent: 0.0308 vs 0.0296.

### 5.6 Worked Example — Chip Cooling (20 Aug)

**Setup:** Array of chips on a flat plate, $L = $ plate length, air flow $u_\infty$. Each chip generates power $q_{chip}$. Find max chip temperature.

**Key insight:** Since $h_x \sim x^{-1/2}$ (laminar), the **last chip** (at $x = L$) has the minimum $h_x$ and therefore the highest surface temperature.

**Turbulent local $h$** (chip cooling case, turbulent BL):

$$\bar{h}_{10} = 0.0308\left(\frac{k}{x}\right)Re_x^{4/5}Pr^{1/3} = 145\,\text{W/m}^2\text{K}$$

$$q = 0.81\,\text{W per chip}$$

**Strategy:** Design so that the last chip stays below $T_{max}$; all preceding chips will automatically be safe.

---

## 6. Procedure for Solving External Convection Problems

1. Identify surface temperature $T_s$ and fluid temperature $T_\infty$
2. Calculate film temperature $T_f = (T_s + T_\infty)/2$
3. Look up fluid properties at $T_f$ (Table A-4 for air in Incropera & DeWitt)
4. Calculate $Re_L = u_\infty L / \nu$
5. Determine flow regime:
   - If $Re_L < 5 \times 10^5$: fully laminar
   - If $Re_L > 5 \times 10^5$: check $x_c/L$, use mixed correlation
6. Compute $\overline{Nu}_L$ using appropriate correlation
7. Compute $\bar{h} = \overline{Nu}_L \cdot k / L$
8. Compute $q = \bar{h} A_s (T_s - T_\infty)$

---

## 7. Summary of Flat Plate Correlations

| Flow Regime | Correlation | Validity |
|-------------|-------------|----------|
| Laminar (local) | $Nu_x = 0.453\,Re_x^{1/2}\,Pr^{1/3}$ | $Pr \ge 0.6$ |
| Laminar (average) | $\overline{Nu}_L = 0.664\,Re_L^{1/2}\,Pr^{1/3}$ | $Re_L < 5\times10^5$, $Pr \ge 0.6$ |
| Turbulent (local) | $Nu_x = 0.0296\,Re_x^{4/5}\,Pr^{1/3}$ | $5\times10^5 < Re_x < 10^7$ |
| Mixed | $\overline{Nu}_L = (0.037\,Re_L^{4/5} - 871)\,Pr^{1/3}$ | $Re_L > 5\times10^5$ |

All evaluated at film temperature $T_f$.

---

## Textbook References

- **Incropera & DeWitt:** Chapters 6 & 7 (External Forced Convection)
- **Holman & Bhattacharya:** Chapter 4
- **Table A-4** (Incropera & DeWitt): Properties of air at 1 atm

---

## Connected Modules

- [Module 0](01_foundations.md) — Navier-Stokes as the governing momentum equation for BL
- [Module 5](06_convection_internal.md) — Same dimensionless groups, applied inside pipes
- [Module 8](09_free_convection_boiling.md) — Free convection: buoyancy replaces the external forcing
