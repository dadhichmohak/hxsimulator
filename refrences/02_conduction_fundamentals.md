# Module 1 — Conduction: Fundamentals
**Dates:** 30 Jul, 4 Aug, 6 Aug 2025  
**Sources:** `htoa25lec130jul.pdf`, `htoa254aug.pdf`, `htoa256aug.pdf`

---

## Overview

Conduction is **heat transfer through molecular activity** — vibration, collision, and electron transport — without bulk motion of the medium. This module covers 1D steady-state conduction in planar, cylindrical, and spherical geometries, using the thermal resistance analogy.

---

## 1. Fourier's Law (1D)

$$q = -k\frac{dT}{dx} \qquad \left[\frac{W}{m^2}\right]$$

The **convection** analog for reference:
$$q = h(T_s - T_\infty)$$

Where $h \equiv f(v, \mu, k)$ — the convection coefficient depends on flow velocity $v$, viscosity $\mu$, and conductivity $k$.

**Units of $h$:** $\left[\frac{W}{m^2 K}\right]$

---

## 2. Thermal Resistance Concept

By analogy with Ohm's law ($V = IR$), heat flow through a layer can be written as:

$$Q = \frac{\Delta T}{R_{th}}$$

where $R_{th}$ is the **thermal resistance**.

### Planar (Slab) Wall

$$R_{th,\text{cond}} = \frac{L}{kA}$$

$$R_{th,\text{conv}} = \frac{1}{hA}$$

### Series Resistance (Composite Wall or with Convection)

For a wall with fluid on both sides:

$$R_{total} = \frac{1}{h_i A_i} + \frac{L}{kA} + \frac{1}{h_o A_o}$$

The heat flux through each resistance is the same at steady state.

---

## 3. Cylindrical Coordinates — Steady State

### 3.1 Single Cylinder (Hollow)

For a hollow cylinder of length $L$, inner radius $r_i$, outer radius $r_o$, at steady state with no heat generation:

$$Q = \frac{2\pi k L (T_i - T_o)}{\ln(r_o/r_i)}$$

**Thermal resistance of the cylindrical shell:**

$$\boxed{R_1 = \frac{\ln(r_o/r_i)}{2\pi k L}}$$

### 3.2 Cylinder with Inner and Outer Convection

For a cylinder with:
- Inner fluid at $T_A$, inner convection coefficient $h_i$
- Outer fluid at $T_B$, outer convection coefficient $h_o$

**Total thermal resistance:**

$$R_{th} = \frac{1}{h_i A_i} + \frac{\ln(r_o/r_i)}{2\pi k L} + \frac{1}{h_o A_o}$$

Where $A_i = 2\pi r_i L$ and $A_o = 2\pi r_o L$.

At steady state, the same heat flux passes through all resistances:

$$q = h_o A_o (T_B - T_o) = \frac{2\pi k L (T_i - T_o)}{\ln(r_o/r_i)} = h_i A_i (T_i - T_A)$$

---

## 4. Heat Source Problems — Cylindrical Coordinates

**Setup (4 Aug 2025):** A cylindrical wire/rod with internal heat generation (e.g., resistive heating), cooled by convection at its surface.

Given:
- $T_s = 215°C$ (surface temperature — known)
- $T_\infty = 110°C$ (ambient fluid temperature)
- Resistivity $S = 70\, \mu\Omega\cdot\text{cm}$
- Radius $R$, find $T(r=0)$ — **centreline temperature**

**Governing equation** (1D cylindrical, steady state, with heat generation $\dot{q}$):

$$\frac{1}{r}\frac{d}{dr}\left(r\frac{dT}{dr}\right) + \frac{\dot{q}}{k} = 0$$

**General solution:**

$$T(r) = -\frac{\dot{q}}{4k}r^2 + C_1 \ln r + C_2$$

**Boundary conditions:**
1. $\frac{dT}{dr}\Big|_{r=0} = 0$ (symmetry — finite temperature at centre) → $C_1 = 0$
2. $T(R) = T_s$ (known surface temperature)

**Solution:**

$$T(r) = T_s + \frac{\dot{q}}{4k}(R^2 - r^2)$$

**Maximum temperature** (at centreline $r = 0$):

$$T_{max} = T_s + \frac{\dot{q}R^2}{4k}$$

**Heat generation from resistivity:**

$$\dot{q} = \frac{I^2 S}{\pi^2 R^4} \quad \text{[or expressed via power dissipation per unit volume]}$$

---

## 4b. Full Worked Example — Electrical Wire (4 Aug)

**Problem:** A cylindrical wire, $D = ?$, $L = 1\,\text{m}$, resistivity $S = 70\,\mu\Omega\cdot\text{cm}$, carrying current $I$, $T_s = 215°C$, $T_\infty = 110°C$. Find centreline temperature $T(r=0)$.

**Step 1 — Electrical resistance:**

$$R_{elec} = \frac{S\,L}{A} = \frac{S\,L}{\pi D^2/4} = 0.099\,\Omega$$

**Step 2 — Power dissipated:**

$$P = I^2 R = 3960\,\text{W}$$

**Step 3 — Volumetric heat generation:**

$$\dot{H}_v = \frac{P}{V_{wire}} = \frac{P}{\pi D^2 L/4} = 560.2\times10^6\,\text{W/m}^3$$

**Step 4 — Steady-state heat equation in cylindrical coordinates** (Poisson form):

$$\nabla^2 T + \frac{\dot{H}_v}{k} = 0 \implies \frac{d}{dr}\!\left(r\frac{dT}{dr}\right) = -\frac{\dot{H}_v}{k}\,r$$

Laplacian in 1D cylindrical:

$$\frac{d^2T}{dr^2} + \frac{1}{r}\frac{dT}{dr} + \frac{\dot{H}_v}{k} = 0$$

**General solution:**

$$T(r) = -\frac{\dot{H}_v r^2}{4k} + C_1\ln r + C_2$$

**Apply BCs:**
- $T$ finite at $r=0$ → $C_1 = 0$
- $T(r=R) = T_s$ → $C_2 = T_s + \frac{\dot{H}_v R^2}{4k}$

**Final solution:**

$$\boxed{T(r) = T_s + \frac{\dot{H}_v}{4k}(R^2 - r^2)}$$

**Centreline temperature:**

$$T(r=0) = T_s + \frac{\dot{H}_v R^2}{4k} = 215 + \frac{560.2\times10^6 \times R^2}{4k} = 231.6°C$$

---

## 4c. Overall Heat Transfer Coefficient for a Cylinder (6 Aug)

For a cylindrical pipe with inner diameter $D_i$, outer diameter $D_o$, with inner fluid ($h_i$) and outer fluid ($h_o$):

**Referenced to inner area $A_i = \pi D_i L$:**

$$\frac{1}{U_i} = \frac{1}{h_i} + \frac{A_i\ln(D_o/D_i)}{2\pi k L} + \left(\frac{A_i}{A_o}\right)\frac{1}{h_o}$$

Since $A_i/A_o = D_i/D_o$:

$$\boxed{\frac{1}{U_i} = \frac{1}{h_i} + \frac{D_i\ln(D_o/D_i)}{2k} + \left(\frac{D_i}{D_o}\right)\frac{1}{h_o}}$$

This form is used directly in shell-and-tube heat exchanger calculations.

---

## 5. Critical Thickness of Insulation (8 Sep 2025)

An important and counter-intuitive result: adding insulation to a cylinder does **not** always decrease heat loss. There exists an optimal outer radius.

**Setup:** Cylindrical pipe, inner radius $r_i$, inner surface temperature $T_i$. Add insulation layer to outer radius $r_o$. Outer surface exposed to ambient at $T_\infty$ with convection coefficient $h$.

**Thermal resistance circuit:**

$$T_i \xrightarrow{R_1} T_s \xrightarrow{R_2} T_\infty$$

$$R_1 = \frac{\ln(r_o/r_i)}{2\pi k L} \qquad R_2 = \frac{1}{h \cdot 2\pi r_o L}$$

**Total resistance:**
$$R_{total}(r_o) = \frac{\ln(r_o/r_i)}{2\pi k L} + \frac{1}{2\pi r_o h L}$$

**Finding the minimum** (maximum heat loss) by $\frac{dR_{total}}{dr_o} = 0$:

$$\boxed{r_{o,crit} = \frac{k}{h}}$$

- If actual outer radius $r_o < r_{crit}$: adding insulation **increases** heat loss
- If $r_o > r_{crit}$: adding insulation **decreases** heat loss as expected
- For thin wires/pipes (small $r_i$), this is practically significant (e.g., electrical cables)

---

## 6. Composite Walls — Series and Parallel

### Series (1D, resistances in sequence)

$$Q = \frac{T_{fluid,1} - T_{fluid,2}}{R_{conv,1} + R_{wall,1} + R_{wall,2} + \cdots + R_{conv,2}}$$

### Contact Resistance

At the interface between two materials, there is an additional resistance due to surface roughness. It is typically tabulated as a contact resistance per unit area $R''_c$ [m²K/W]:

$$R_{contact} = \frac{R''_c}{A}$$

---

## 7. Summary of Thermal Resistances

| Geometry | Conduction Resistance |
|----------|----------------------|
| Plane wall | $R = \frac{L}{kA}$ |
| Cylindrical shell | $R = \frac{\ln(r_o/r_i)}{2\pi k L}$ |
| Spherical shell | $R = \frac{1/(r_i) - 1/(r_o)}{4\pi k}$ |

| Type | Convection Resistance |
|------|----------------------|
| Any surface | $R = \frac{1}{hA}$ |

---

## 8. Textbook References

- **Incropera & DeWitt:** Chapter 3 (One-Dimensional Steady-State Conduction)
- **Holman & Bhattacharya:** Chapters 2–3

---

## Connected Modules

- [Module 0](01_foundations.md) — Fourier's law derived from constitutive equations
- [Module 2](03_conduction_2D.md) — Extension to 2D steady-state
- [Module 3](04_conduction_numerical.md) — Numerical solution of conduction problems
- [Module 6](07_fins.md) — Critical thickness continues with fins analysis
