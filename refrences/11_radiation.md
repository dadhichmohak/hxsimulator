# Module 10 — Radiation Heat Transfer
**Status:** Supplementary module — topic largely absent from lecture notes  
**Textbooks:** Incropera & DeWitt Ch. 12–13 · Holman & Bhattacharya Ch. 8

---

## Overview

**Radiation** is energy emitted by matter in the form of **electromagnetic waves** (photons), requiring **no medium** — it is the only heat transfer mode that operates in a vacuum. Unlike conduction and convection, radiation depends on the **fourth power of absolute temperature**, making it dominant at high temperatures (furnaces, space applications, combustion) and non-negligible even at moderate temperatures.

---

## 1. Fundamental Concepts

### 1.1 The Electromagnetic Spectrum

Thermal radiation occupies the wavelength range $0.1\,\mu\text{m} \le \lambda \le 100\,\mu\text{m}$, spanning the ultraviolet, visible, and infrared bands:

```
γ-rays  X-rays  UV  │ Visible │  Near-IR  │  Thermal IR  │  Microwave
                 0.1μm  0.4  0.7μm           10μm         100μm
                        ←────────── Thermal radiation ──────────→
```

- Solids and liquids emit radiation **continuously** across a spectrum
- Gases and flames emit at **discrete wavelengths** (band radiation)

### 1.2 Key Definitions

| Term | Symbol | Definition |
|------|--------|-----------|
| Irradiation | $G$ [W/m²] | Total radiation incident on a surface |
| Radiosity | $J$ [W/m²] | Total radiation leaving a surface (emitted + reflected) |
| Emissive Power | $E$ [W/m²] | Energy emitted per unit area by a surface |
| Spectral quantity | subscript $\lambda$ | Quantity per unit wavelength interval |
| Hemispherical | — | Integrated over all directions in a hemisphere |

### 1.3 Blackbody — The Perfect Emitter/Absorber

A **blackbody** is an idealised surface that:
1. Absorbs **all** incident radiation (absorptivity $\alpha = 1$)
2. Emits the **maximum possible** radiation at a given temperature
3. Emits radiation **isotropically** (equally in all directions — Lambertian)

All real surfaces emit less than a blackbody at the same temperature.

---

## 2. Blackbody Radiation Laws

### 2.1 Planck's Law (Spectral Distribution)

The spectral emissive power of a blackbody at temperature $T$ and wavelength $\lambda$:

$$\boxed{E_{b,\lambda}(\lambda, T) = \frac{C_1}{\lambda^5\left[\exp\!\left(\dfrac{C_2}{\lambda T}\right) - 1\right]}}$$

where:
- $C_1 = 2\pi h c^2 = 3.742 \times 10^8\,\text{W}\cdot\mu\text{m}^4/\text{m}^2$
- $C_2 = hc/k_B = 1.439 \times 10^4\,\mu\text{m}\cdot\text{K}$
- $h$ = Planck's constant, $c$ = speed of light, $k_B$ = Boltzmann constant

**Shape of the curve:**
- Peaks at a wavelength that shifts left (shorter $\lambda$) as $T$ increases
- Area under curve increases dramatically with $T$ (fourth-power law)
- At low $T$: peak in infrared; at very high $T$: peak shifts toward visible

### 2.2 Wien's Displacement Law

The wavelength at which $E_{b,\lambda}$ is maximum shifts with temperature:

$$\boxed{\lambda_{max} T = C_3 = 2897.8\,\mu\text{m}\cdot\text{K}}$$

**Practical applications:**

| Body | $T$ (K) | $\lambda_{max}$ ($\mu$m) | Comment |
|------|---------|--------------------------|---------|
| Human skin | 310 | 9.35 | Far infrared — thermal cameras |
| Light bulb filament | 2900 | 1.0 | Near infrared (inefficient for visible light) |
| Sun's surface | 5800 | 0.50 | Yellow-green — peak of human vision |
| Furnace wall | 1500 | 1.93 | Near-IR, glowing orange-red |

**Derivation sketch:** Differentiate $E_{b,\lambda}$ w.r.t. $\lambda$, set to zero → transcendental equation solved numerically to give $\lambda_{max} T = 2897.8\,\mu\text{m}\cdot\text{K}$.

### 2.3 Stefan-Boltzmann Law (Total Emissive Power)

Integrating Planck's law over all wavelengths ($0$ to $\infty$):

$$\boxed{E_b = \int_0^\infty E_{b,\lambda}\,d\lambda = \sigma T^4}$$

where $\sigma = 5.67 \times 10^{-8}\,\text{W/m}^2\text{K}^4$ is the **Stefan-Boltzmann constant**.

**Derivation:** Substituting $u = C_2/(\lambda T)$, the integral reduces to a standard result:

$$\int_0^\infty \frac{u^3}{e^u - 1}du = \frac{\pi^4}{15}$$

giving $\sigma = 2\pi^5 k_B^4 / (15 h^3 c^2)$.

### 2.4 Blackbody Radiation Function $F_{(0-\lambda T)}$

Often needed: fraction of blackbody emission in the range $0$ to $\lambda$:

$$F_{(0-\lambda T)} = \frac{\displaystyle\int_0^\lambda E_{b,\lambda}\,d\lambda}{\sigma T^4}$$

This is tabulated as a function of the product $\lambda T$ (Table 12.2 in Incropera & DeWitt).

**Fraction between $\lambda_1$ and $\lambda_2$:**

$$F_{(\lambda_1 T - \lambda_2 T)} = F_{(0-\lambda_2 T)} - F_{(0-\lambda_1 T)}$$

**Example:** Sun emits at $T = 5800\,\text{K}$. Fraction in visible range ($0.4$–$0.7\,\mu\text{m}$):
- $\lambda_1 T = 0.4 \times 5800 = 2320\,\mu\text{m}\cdot\text{K}$ → $F = 0.12$
- $\lambda_2 T = 0.7 \times 5800 = 4060\,\mu\text{m}\cdot\text{K}$ → $F = 0.49$
- Fraction in visible: $0.49 - 0.12 = 0.37$ (37% of solar emission is visible)

---

## 3. Surface Radiation Properties

### 3.1 Emissivity

$$\boxed{\varepsilon = \frac{E}{E_b} = \frac{\text{Actual emissive power}}{\text{Blackbody emissive power at same }T}}$$

Range: $0 \le \varepsilon \le 1$. A blackbody has $\varepsilon = 1$.

**Typical values:**

| Surface | $\varepsilon$ |
|---------|--------------|
| Polished silver | 0.02 |
| Polished copper | 0.03 |
| Polished aluminium | 0.04–0.06 |
| White paint | 0.90–0.95 |
| Black paint | 0.95–0.98 |
| Human skin | 0.95 |
| Brick | 0.90–0.95 |
| Glass (opaque to IR) | 0.84–0.90 |

### 3.2 Absorptivity, Reflectivity, Transmissivity

For any surface, the incident radiation $G$ is split into:

$$\boxed{\alpha + \rho + \tau = 1}$$

where:
- $\alpha$ = **absorptivity** (fraction absorbed)
- $\rho$ = **reflectivity** (fraction reflected)
- $\tau$ = **transmissivity** (fraction transmitted through the body)

For an **opaque** body ($\tau = 0$): $\alpha + \rho = 1$

**Kirchhoff's Law:** For a surface in **thermal equilibrium** with its surroundings:

$$\boxed{\varepsilon_\lambda = \alpha_\lambda}$$

Spectral emissivity equals spectral absorptivity. For a **gray surface** (properties independent of wavelength): $\varepsilon = \alpha$ at all conditions.

### 3.3 Gray Body Approximation

A **gray body** has:
- $\varepsilon$ = constant (independent of $\lambda$ and direction)
- $\alpha = \varepsilon$ (Kirchhoff's law applies globally, not just spectrally)

This is the standard engineering approximation that allows closed-form solutions. Most surfaces can be treated as gray in the infrared range.

---

## 4. Radiation Exchange Between Surfaces — View Factors

### 4.1 Definition

The **view factor** $F_{ij}$ (also called shape factor, configuration factor, or angle factor) is the **fraction of radiation leaving surface $i$ that is intercepted by surface $j$**:

$$\boxed{F_{ij} = \frac{\text{Radiation from surface }i\text{ intercepted by surface }j}{\text{Total radiation leaving surface }i}}$$

View factors are purely **geometric** — they depend only on surface geometry, size, and orientation, not on temperature or surface properties.

### 4.2 Mathematical Definition

For two differential area elements $dA_i$ and $dA_j$ separated by distance $r$, with surface normals making angles $\theta_i$ and $\theta_j$ with the line connecting them:

$$F_{ij} = \frac{1}{A_i}\int_{A_i}\int_{A_j} \frac{\cos\theta_i\cos\theta_j}{\pi r^2}\,dA_j\,dA_i$$

This double area integral is evaluated analytically for standard geometries (tabulated in textbooks).

### 4.3 View Factor Rules

**Rule 1 — Summation Rule:** All radiation leaving surface $i$ must hit some surface in the enclosure:

$$\boxed{\sum_{j=1}^{N} F_{ij} = 1}$$

**Rule 2 — Reciprocity Relation:**

$$\boxed{A_i F_{ij} = A_j F_{ji}}$$

This allows calculation of $F_{ji}$ from $F_{ij}$ when areas differ.

**Rule 3 — Self-View Factor:**
- Flat or convex surface: $F_{ii} = 0$ (cannot "see" itself)
- Concave surface: $F_{ii} > 0$ (can see itself)

### 4.4 View Factor Algebra

Complex geometries can be built from simpler ones using:

**Superposition:** If surface $j$ is subdivided into $j_1$ and $j_2$:

$$F_{i(j_1+j_2)} = F_{ij_1} + F_{ij_2}$$

**Enclosure method:** For an $N$-surface enclosure, there are $N^2$ view factors, but:
- Summation rule gives $N$ equations
- Reciprocity gives $N(N-1)/2$ equations
- Total independent values needed: $N(N-1)/2$

### 4.5 Key View Factor Results

**Two infinite parallel plates (equal area $A$):**

$$F_{12} = F_{21} = 1$$

**Concentric cylinders (inner = 1, outer = 2):**

$$F_{11} = 0, \quad F_{12} = 1, \quad F_{21} = \frac{r_1}{r_2}, \quad F_{22} = 1 - \frac{r_1}{r_2}$$

**Small convex surface (1) in a large enclosure (2):**

$$F_{12} = 1, \quad F_{21} \approx 0$$

**Two coaxial disks of equal radius $r$, separated by $h$:** (from tables)

$$F_{12} = \frac{1}{2}\left[S - \sqrt{S^2 - 4(r_2/r_1)^2}\right], \quad S = 1 + \frac{1+R_2^2}{R_1^2}, \quad R_i = r_i/h$$

**Two long parallel plates of equal width $w$, separated by $h$:**

$$F_{12} = \sqrt{1 + \left(\frac{h}{w}\right)^2} - \frac{h}{w}$$

---

## 5. Radiation Exchange in Enclosures — Network Method

### 5.1 Radiosity

For an opaque, gray, diffuse surface, the **radiosity** $J$ (total radiation leaving the surface) is:

$$J = \varepsilon E_b + (1-\varepsilon)G = \varepsilon\sigma T^4 + (1-\varepsilon)G$$

- First term: emitted radiation
- Second term: reflected portion of incident radiation $G$

### 5.2 Net Radiation from a Surface

The net radiation leaving surface $i$:

$$q_i = A_i(J_i - G_i)$$

Combining with the radiosity definition and eliminating $G$:

$$\boxed{q_i = \frac{E_{b,i} - J_i}{(1-\varepsilon_i)/(\varepsilon_i A_i)}}$$

**Surface resistance:**

$$R_{surface,i} = \frac{1 - \varepsilon_i}{\varepsilon_i A_i}$$

This is analogous to a thermal resistance — potential difference $(E_b - J)$ divided by resistance gives the net heat flow.

**For a blackbody:** $\varepsilon = 1$ → $R_{surface} = 0$ → $J = E_b = \sigma T^4$ (radiosity equals emissive power).

### 5.3 Net Radiation Exchange Between Two Surfaces

The net heat flow from surface $i$ to surface $j$ (via the view factor):

$$q_{ij} = A_i F_{ij}(J_i - J_j) = \frac{J_i - J_j}{1/(A_i F_{ij})}$$

**Space resistance:**

$$R_{space,ij} = \frac{1}{A_i F_{ij}}$$

### 5.4 The Radiation Network (Resistance Analogy)

For a two-surface gray enclosure, the circuit is:

$$E_{b,1} \xrightarrow{R_1} J_1 \xrightarrow{R_{12}} J_2 \xrightarrow{R_2} E_{b,2}$$

$$R_1 = \frac{1-\varepsilon_1}{\varepsilon_1 A_1}, \quad R_{12} = \frac{1}{A_1 F_{12}}, \quad R_2 = \frac{1-\varepsilon_2}{\varepsilon_2 A_2}$$

Total net heat transfer from surface 1 to surface 2:

$$\boxed{q_{12} = \frac{E_{b,1} - E_{b,2}}{R_1 + R_{12} + R_2} = \frac{\sigma(T_1^4 - T_2^4)}{\dfrac{1-\varepsilon_1}{\varepsilon_1 A_1} + \dfrac{1}{A_1 F_{12}} + \dfrac{1-\varepsilon_2}{\varepsilon_2 A_2}}}$$

---

## 6. Special Two-Surface Cases

### 6.1 Two Large Parallel Plates

$A_1 = A_2 = A$, $F_{12} = 1$:

$$\boxed{q_{12} = \frac{\sigma A(T_1^4 - T_2^4)}{\dfrac{1}{\varepsilon_1} + \dfrac{1}{\varepsilon_2} - 1}}$$

### 6.2 Concentric Cylinders or Spheres

Inner surface 1 (area $A_1$), outer surface 2 (area $A_2$), $F_{12} = 1$:

$$\boxed{q_{12} = \frac{\sigma A_1(T_1^4 - T_2^4)}{\dfrac{1}{\varepsilon_1} + \dfrac{A_1}{A_2}\left(\dfrac{1}{\varepsilon_2} - 1\right)}}$$

When $A_1 \ll A_2$ (small body in large enclosure, $A_1/A_2 \to 0$):

$$q_{12} = \varepsilon_1 \sigma A_1 (T_1^4 - T_2^4)$$

This is the standard **small body in large enclosure** formula — the standard engineering expression for radiation from a surface to surroundings.

### 6.3 Two Blackbodies

$\varepsilon_1 = \varepsilon_2 = 1$, so $R_1 = R_2 = 0$:

$$q_{12} = A_1 F_{12} \sigma (T_1^4 - T_2^4)$$

---

## 7. Three-Surface Enclosures

For three gray surfaces, there are three surface resistances $R_1$, $R_2$, $R_3$ and three space resistances $R_{12}$, $R_{13}$, $R_{23}$. The network is solved using Kirchhoff's current law at each radiosity node (junction):

At node $J_1$: $\frac{E_{b,1}-J_1}{R_1} = \frac{J_1-J_2}{R_{12}} + \frac{J_1-J_3}{R_{13}}$

At node $J_2$: $\frac{E_{b,2}-J_2}{R_2} = \frac{J_2-J_1}{R_{12}} + \frac{J_2-J_3}{R_{23}}$

Similarly for $J_3$. This gives 3 equations for 3 unknowns ($J_1$, $J_2$, $J_3$), then net heat flows are computed.

**Reradiating (insulated) surface:** If one surface (say $R$) is perfectly insulated ($q_R = 0$), it acts as a **reradiating surface** with $J_R = E_{b,R}$ and unknown $T_R$. It simply redirects radiation between the other surfaces. The network simplifies: $R_{surface,R} = 0$, and the $J_R$ node floats.

---

## 8. Radiation from a Surface to Surroundings — Linearisation

For a surface at $T_s$ in large surroundings at $T_{sur}$:

$$q = \varepsilon\sigma A(T_s^4 - T_{sur}^4)$$

This can be **linearised** to define a radiation heat transfer coefficient $h_r$:

$$q = h_r A(T_s - T_{sur})$$

where:

$$\boxed{h_r = \varepsilon\sigma(T_s + T_{sur})(T_s^2 + T_{sur}^2)}$$

This allows radiation and convection to be added in parallel in a combined resistance network:

$$q_{total} = (h + h_r)A(T_s - T_\infty) \quad \text{(when }T_{sur} = T_\infty\text{)}$$

---

## 9. Combined Radiation and Convection

For a surface losing heat by both convection and radiation simultaneously:

$$q_{total} = q_{conv} + q_{rad} = hA(T_s - T_\infty) + \varepsilon\sigma A(T_s^4 - T_{sur}^4)$$

**Thermal resistance circuit (parallel):**

$$R_{conv} = \frac{1}{hA}, \qquad R_{rad} = \frac{1}{h_r A}$$

$$R_{total} = \frac{R_{conv} R_{rad}}{R_{conv} + R_{rad}}$$

This arises in fin analysis (combined modes), spacecraft thermal control, building energy models, etc.

---

## 10. Radiation Shields

A radiation shield is a thin sheet placed between two surfaces to reduce radiation exchange.

**Single shield (surface $s$) between two parallel plates (1 and 2):**

All surfaces have emissivities $\varepsilon_1$, $\varepsilon_{s,1}$, $\varepsilon_{s,2}$, $\varepsilon_2$. The network now has two space resistances and three surface resistances.

For all emissivities equal to $\varepsilon$:

$$q_{12,shield} = \frac{\sigma A(T_1^4 - T_2^4)}{\dfrac{1}{\varepsilon_1}+\dfrac{1}{\varepsilon_2}-1 + \left(\dfrac{1}{\varepsilon_{s,1}}+\dfrac{1}{\varepsilon_{s,2}}-1\right)}$$

With a **single shield** of the same emissivity ($\varepsilon$) as the plates:

$$\frac{q_{shield}}{q_{no\,shield}} = \frac{1}{2}$$

With $N$ identical shields:

$$\frac{q_{N\,shields}}{q_{no\,shield}} = \frac{1}{N+1}$$

**Low-emissivity (polished metal) shields** are highly effective: two polished Al surfaces ($\varepsilon = 0.05$) with one identical shield:

$$q \propto \frac{1}{1/0.05 + 1/0.05 - 1 + 1/0.05 + 1/0.05 - 1} \approx \frac{1}{76} \quad \text{vs} \quad \frac{1}{39} \text{ without shield}$$

---

## 11. Radiation in Participating Media (Brief)

In gases, radiation can be **absorbed, emitted, and scattered** within the medium itself (unlike in solids/liquids where radiation is a surface phenomenon).

Key concepts:
- **Beer-Lambert Law:** $I_\lambda = I_{\lambda,0}\,e^{-\kappa_\lambda x}$ — intensity decays exponentially with path length $x$ through absorbing gas; $\kappa_\lambda$ = spectral absorption coefficient [m⁻¹]
- **Optical thickness:** $\tau_\lambda = \kappa_\lambda L$ — dimensionless measure of attenuation
- **Greenhouse effect:** CO₂ and H₂O absorb strongly in the 8–13 μm window, re-radiating back to Earth's surface
- **Engineering treatment:** For furnace calculations, use effective emissivity of gas mixtures (Hottel charts for CO₂/H₂O mixtures)

---

## 12. Summary of Key Equations

### Blackbody Laws

| Law | Formula | Notes |
|-----|---------|-------|
| Planck | $E_{b,\lambda} = C_1/[\lambda^5(e^{C_2/\lambda T}-1)]$ | Spectral distribution |
| Wien's displacement | $\lambda_{max}T = 2897.8\,\mu\text{m}\cdot\text{K}$ | Peak wavelength |
| Stefan-Boltzmann | $E_b = \sigma T^4$ | Total emissive power |
| Blackbody fraction | $F_{(0-\lambda T)}$ from tables | Fraction in $[0,\lambda]$ |

### Surface Properties

| Property | Symbol | Blackbody | Gray body | Real |
|----------|--------|-----------|-----------|------|
| Emissivity | $\varepsilon$ | 1 | const | $f(\lambda,T,\theta)$ |
| Absorptivity | $\alpha$ | 1 | $= \varepsilon$ | $f(\lambda)$ |
| Kirchhoff's law | $\varepsilon_\lambda = \alpha_\lambda$ | exact | approx. | exact |

### View Factors

| Rule | Formula |
|------|---------|
| Summation | $\sum_j F_{ij} = 1$ |
| Reciprocity | $A_i F_{ij} = A_j F_{ji}$ |
| Two parallel plates | $F_{12} = 1$ |

### Radiation Exchange (Gray, Diffuse)

| Geometry | Formula |
|----------|---------|
| Surface resistance | $R_{s} = (1-\varepsilon)/(\varepsilon A)$ |
| Space resistance | $R_{sp} = 1/(A_i F_{ij})$ |
| Any two-surface enclosure | $q = (E_{b,1}-E_{b,2})/(R_1+R_{12}+R_2)$ |
| Small body in large enclosure | $q = \varepsilon\sigma A(T_s^4-T_{sur}^4)$ |
| Two parallel plates | $q = \sigma A(T_1^4-T_2^4)/(1/\varepsilon_1+1/\varepsilon_2-1)$ |
| Radiation h.t. coeff. | $h_r = \varepsilon\sigma(T_s+T_{sur})(T_s^2+T_{sur}^2)$ |
| $N$ shields (identical) | $q_{shield}/q_0 = 1/(N+1)$ |

---

## 13. What Was Missing — Gap Analysis

Comparing the HTOA 2025 notes against classical Heat Transfer curricula (Incropera & DeWitt Ch. 12–13), the following were absent or only mentioned in passing:

| Topic | Status in Notes | Coverage Here |
|-------|----------------|---------------|
| Planck's law | Missing | §2.1 |
| Wien's displacement law | Missing | §2.2 |
| Stefan-Boltzmann law derivation | Mentioned in cheatsheet only | §2.3 |
| Blackbody fraction $F_{(0-\lambda T)}$ | Missing | §2.4 |
| Emissivity, absorptivity, Kirchhoff's law | Missing | §3 |
| Gray body approximation | Missing | §3.3 |
| View factors — definition | Missing | §4.1–4.3 |
| View factor algebra (summation, reciprocity) | Missing | §4.3–4.4 |
| Specific view factor results | Missing | §4.5 |
| Radiosity | Missing | §5.1 |
| Radiation network / resistance analogy | Missing | §5.2–5.4 |
| Two-surface enclosures (closed form) | Missing | §6 |
| Three-surface enclosures | Missing | §7 |
| Linearised radiation coefficient $h_r$ | Missing | §8 |
| Combined convection + radiation | Missing | §9 |
| Radiation shields | Missing | §10 |
| Participating media (Beer-Lambert) | Missing | §11 |

**Radiation was acknowledged** in the course overview and cheatsheet (`q = εσ(Ts⁴ - Tsur⁴)`), but no dedicated lecture module was digitised — this module fills that gap completely.

---

## Textbook References

- **Incropera & DeWitt:** Chapters 12 (Radiation: Processes & Properties) and 13 (Radiation: Exchange between Surfaces)
- **Holman & Bhattacharya:** Chapter 8 (Radiation Heat Transfer)
- **Siegel & Howell:** *Thermal Radiation Heat Transfer* (advanced reference)

---

## Connected Modules

- [Module 0](01_foundations.md) — Radiation listed as the third mode of heat transfer
- [Module 7](08_heat_exchangers.md) — Radiation matters in high-temperature HX (furnace-type)
- [Module 8](09_free_convection_boiling.md) — Combined free convection + radiation in natural environments
