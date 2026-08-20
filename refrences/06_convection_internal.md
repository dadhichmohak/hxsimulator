# Module 5 — Convection: Internal Flows
**Dates:** 25 Aug, 28 Aug, 1 Sep, 3 Sep, 4 Sep, 10 Sep 2025  
**Sources:** `htoa2525aug.pdf`, `htoa2528aug.pdf`, `htoa251sep.pdf`, `htoa253sep.pdf`, `htoa2504sep.pdf`, `htoa2510sep.pdf`

**Textbooks:** Incropera & DeWitt Ch. 8 · Holman & Bhattacharya Ch. 5 & 6

---

## Overview

**Internal flow** = fluid is constrained to flow inside a duct/pipe/channel. Unlike external flow, the boundary layer cannot grow indefinitely — it eventually fills the pipe cross-section, creating **fully developed flow**. This changes the physics of heat transfer fundamentally.

---

## 1. Hydrodynamic (Velocity) Entrance Region

### Entry Length Development

When fluid enters a pipe, boundary layers grow from the wall and merge at the centreline. Beyond the **hydrodynamic entry length** $x_{fd,h}$, the velocity profile no longer changes axially:

$$\frac{\partial u}{\partial x} = 0 \quad \text{(fully developed condition)}$$

```
Flat profile     Boundary     Parabolic profile
→→→→→→→         layer        →
→→→→→→→  ——→    merging  ——→  →→→→→→→→→→→→→
→→→→→→→         δ ↑ δ        →
             entrance        fully developed
              region
             ←  x_fd,h  →
```

**Hydrodynamic entry length:**
- Laminar ($Re_D < 2300$): $\quad x_{fd,h} \approx 0.05\,Re_D \cdot D$
- Turbulent: $\quad x_{fd,h} \approx 10–60\,D$ (much shorter)

---

## 2. Thermal Entrance Region

A **thermal entry length** also exists. Even if the flow is hydrodynamically fully developed, the temperature profile needs distance to develop. The notes confirm (25 Aug): "Does a fully developed condition exist for the thermal case? **YES** (but we need a couple of definitions to start with)."

**Key observation (28 Aug):** In the thermal entrance region, the heat transfer coefficient $h$ starts very high and decreases to a constant value in the fully developed region:

```
h ↑
  |↘
  |  ↘______________
  |
  0     x_fd,t        →x
```

**Thermal entry length:**
- Laminar: $\quad x_{fd,t} \approx 0.05\,Re_D\,Pr\,D$
- Turbulent: Similar to hydrodynamic, $x_{fd,t} \approx 10\,D$

---

## 3. Mean (Bulk) Temperature

Since temperature varies radially inside the pipe, a **mean temperature** $T_m$ (also called bulk or mixing-cup temperature) is defined:

$$T_m = \frac{\displaystyle\int_0^{r_o} \rho C_p u T\, r\, dr}{\displaystyle\dot{m} C_p}$$

- $T_m$ is the temperature a perfectly mixed cross-section would have
- It changes along the pipe due to wall heat transfer
- The fully developed thermal condition (constant $T_s$) means $\frac{d}{dx}\left(\frac{T_s - T}{T_s - T_m}\right) = 0$

**Mean temperature evolution (28 Aug derivation):**

At fully developed thermal conditions (constant wall temperature $T_s$):

$$\frac{\partial T_s}{\partial x} = \frac{\partial T_m}{\partial x}$$

This means the wall–fluid temperature difference maintains a fixed shape along the pipe.

---

## 4. Heat Transfer in a Pipe — Laminar Flow (1 Sep)

### 4.1 Governing Energy Equation

For fully developed laminar flow (Hagen-Poiseuille velocity profile) in a circular tube, the energy equation is:

$$u_0\left[1 - \left(\frac{r}{r_0}\right)^2\right]\frac{\partial T}{\partial x} = \frac{\alpha}{r}\frac{\partial}{\partial r}\left(r\frac{\partial T}{\partial r}\right)$$

where $u_0$ = centreline velocity, $r_0$ = pipe radius, $\alpha = k/(\rho C_p)$ = thermal diffusivity.

**Two boundary conditions for the thermal problem:**

1. **Constant heat flux** $q_s''$: $\frac{dT_m}{dx} = \text{const}$
2. **Constant wall temperature** $T_s$: $\frac{T_s - T}{T_s - T_m}\frac{dT_m}{dx} = \text{const}$

### 4.2 Nusselt Numbers (Fully Developed, Laminar)

| Boundary Condition | $Nu_D$ |
|--------------------|--------|
| Uniform heat flux ($q_s'' = \text{const}$) | $Nu_D = 4.36$ |
| Uniform wall temperature ($T_s = \text{const}$) | $Nu_D = 3.66$ |

These are **constants** — the Nusselt number is independent of $Re$, $Pr$, and position $x$ in fully developed laminar flow. This is a remarkable result.

### 4.3 Total Tube Heat Transfer Rate

The differential rate of heat transfer across a cross-section is:

$$dq_{conv} = \dot{m}C_p\,dT_m$$

Integrating over the full tube length:

$$\boxed{q_{conv} = \dot{m}C_p(T_{m,o} - T_{m,i})}$$

**Notes from lecture (1 Sep):**
- This is simply an energy balance
- Applicable for **all surface thermal conditions** (const. $q_s''$ or const. $T_s$)
- Applicable for **both laminar and turbulent** flow

### 4.4 Constant Surface Flux — Tm Evolution

For $q_s'' = \text{const}$, integrating $dq_{conv} = q_s'' P\,dx$:

$$q_{conv} = q_s'' P L$$

Mean temperature rises **linearly** along the pipe:

$$\frac{dT_m}{dx} = \frac{q_s'' P}{\dot{m}C_p} = \text{const}$$

### 4.5 Constant Surface Temperature — Tm Decay (1 Sep derivation)

For $T_s = \text{const}$, define $\Delta T = T_s - T_m$. Then:

$$\frac{dT_m}{dx} = -\frac{d(\Delta T)}{dx} = \frac{P\,h}{\dot{m}C_p}\Delta T$$

Separating and integrating from 0 to $L$:

$$\int_{\Delta T_i}^{\Delta T_o} \frac{d(\Delta T)}{\Delta T} = -\frac{PL}{\dot{m}C_p}\left[\frac{1}{L}\int_0^L h\,dx\right] = -\frac{PL\,\bar{h}}{\dot{m}C_p}$$

$$\ln\!\left(\frac{\Delta T_o}{\Delta T_i}\right) = -\frac{PL\,\bar{h}}{\dot{m}C_p}$$

**Temperature decay along the pipe (general):**

$$\boxed{\frac{T_s - T_m(x)}{T_s - T_{m,i}} = \exp\!\left(-\frac{Px\,\bar{h}}{\dot{m}C_p}\right)}$$

The bulk temperature approaches $T_s$ **exponentially** — plotted as a curve asymptotically approaching the wall temperature.

**Exit temperature** (at $x = L$):

$$\frac{T_s - T_{m,o}}{T_s - T_{m,i}} = \exp\!\left(-\frac{PL\,\bar{h}}{\dot{m}C_p}\right)$$

Combining with $q_{conv} = \dot{m}C_p(T_{m,o} - T_{m,i})$ and the LMTD definition gives the pipe LMTD formula.

---

## 5. Convective Heat Transfer in Turbulent Flow — Dittus-Boelter (4 Sep)

### Setup (from blackboard notes, 4 Sep)

For **fully developed, hydrodynamically and thermally, turbulent flow** in a smooth circular tube at constant surface temperature $T_s$:

$$\boxed{Nu_D = 0.023\,Re_D^{4/5}\,Pr^n}$$

where:
- $n = 0.4$ for heating ($T_s > T_m$)
- $n = 0.3$ for cooling ($T_s < T_m$)

**Applicability conditions (validated experimentally):**

$$0.6 \le Pr \le 160 \qquad Re_D \ge 10{,}000 \qquad \frac{L}{D} \ge 10$$

- May be used for small to moderate $T_s - T_m$
- All properties evaluated at **mean temperature $T_m$**

---

## 6. Log Mean Temperature Difference for Pipes (3 Sep)

### Mean Temperature Difference Along a Pipe

For a pipe with constant wall temperature $T_s$, the fluid temperature varies exponentially:

$$T_s - T_m(x) = (T_s - T_{m,i})\exp\!\left(-\frac{hA_s}{\dot{m}C_p}\right)$$

**Log Mean Temperature Difference (LMTD) for a pipe:**

$$\boxed{\Delta T_{lm} = \frac{(T_s - T_{m,o}) - (T_s - T_{m,i})}{\ln\!\left[\dfrac{T_s - T_{m,o}}{T_s - T_{m,i}}\right]}}$$

**Example (from notes):** $T_s = 100°C$, $T_{m,i} = 15°C$, $T_{m,o} = 57°C$:

$$\Delta T_{lm} = \frac{(100-57)-(100-15)}{\ln(43/85)} = \frac{-42}{\ln(43/85)} = 61.6°C$$

**Energy balance:**

$$q_{conv} = \bar{h} A_s \Delta T_{lm} = \dot{m} C_p (T_{m,o} - T_{m,i})$$

Equating these two gives the unknown $\bar{h}$ or exit temperature.

---

## 6b. Sieder-Tate Equation (Turbulent, Variable Properties)

When the temperature difference $T_s - T_m$ is large (significant property variation), the Sieder-Tate equation accounts for viscosity variation from bulk to wall:

$$Nu_D = 0.023\,Re_D^{4/5}\,Pr^{1/3}\left(\frac{\mu}{\mu_s}\right)^{0.14}$$

where $\mu_s$ = viscosity at wall temperature $T_s$, all other properties at $T_m$.

**Colburn j-factor derivation (10 Sep):** Divide Sieder-Tate by $Re\cdot Pr$ to get:

$$St\,Pr^{2/3}\,\phi_v^{-1} = j_H = 0.023\,Re^{-0.2} = \frac{f}{2}$$

where $\phi_v = (\mu/\mu_s)^{0.14}$ and $f$ = Fanning friction factor.

**Mass transfer analogy:**

$$Nu \Longleftrightarrow Sh \qquad Pr \Longleftrightarrow Sc$$

The same Colburn analogy applies to mass transfer by replacing $Nu$ with Sherwood number $Sh$ and $Pr$ with Schmidt number $Sc$.

---

## 6c. Worked Example — Turbulent Pipe Flow (8 Sep, Problem 8.38)

**Setup:** Circular tube, $D = 0.05\,\text{m}$, $L = 5\,\text{m}$. Air enters at $T_{m,i} = 17°C$, $\dot{m} = 0.03\,\text{kg/s}$. Tube wall: saturated steam condensing at $T_s = 2.455\,\text{atm}$. Find: (1) $T_{m,o}$, (2) Heat transfer rate $P$.

**Step 1 — Check flow regime:**

$$Re_{D,i} = \frac{4\dot{m}}{\pi D\mu} = \frac{4\times1\,\text{kg/s}}{\pi\times0.0063\times16.3\times10^{-3}} = 1560 \rightarrow \text{laminar!}$$

$$Re_{D,o} = \frac{4\dot{m}}{\pi D_o\mu} = \frac{4\times1}{\pi\times0.005\times3.625\times10^{-3}} = 7840 \rightarrow \text{transition zone}$$

**Step 2 — Check entry lengths:**

$$x_{fd,h} = 0.05\,Re_D\,D = 0.05\times1930\times0.05 = 0.48\,\text{m}$$
$$x_{fd,t} = x_{fd,h}\cdot Pr = 0.48\times0.05 = 898\,\text{m (much > L)}$$

Thermally developing flow throughout! Must use entrance-region correlation.

**Step 3 — Iterate** using mean temperature $T_m = 52°C$ at half-length as first guess; evaluate properties at $T_m$, apply Dittus-Boelter or Graetz solution.

---

## 7. Colburn Analogy and Stanton Number (10 Sep)

### Stanton Number

$$St = \frac{h}{\rho u C_p} = \frac{h}{G\,C_p}$$

where $G = \rho\bar{v}$ is the **mass velocity** [kg/m²s].

**Physical meaning:** Heat transfer rate / fluid's thermal capacity per unit volume.

**Relation to other numbers:**

$$\boxed{St\,Re\,Pr = Nu}$$

$$Re\,Pr = Pe \qquad \text{(Peclet number)}$$

### Colburn j-Factor

The Colburn analogy relates heat transfer to momentum transfer (friction factor $f$):

$$St\,Pr^{2/3} = j_H = \frac{f}{8}$$

This allows heat transfer coefficients to be estimated from friction measurements.

---

## 8. Summary of Internal Flow Key Equations

| Quantity | Formula |
|----------|---------|
| Hydrodynamic entry length (lam.) | $x_{fd,h} = 0.05\,Re_D\,D$ |
| Thermal entry length (lam.) | $x_{fd,t} = 0.05\,Re_D\,Pr\,D$ |
| Nu (lam., const. $q_s''$) | $Nu = 4.36$ |
| Nu (lam., const. $T_s$) | $Nu = 3.66$ |
| Nu (turbulent, Dittus-Boelter) | $Nu = 0.023\,Re_D^{4/5}\,Pr^n$ |
| LMTD (const. $T_s$ pipe) | $\Delta T_{lm} = \frac{\Delta T_o - \Delta T_i}{\ln(\Delta T_o/\Delta T_i)}$ |
| Energy balance | $q = \dot{m}C_p\Delta T_m = \bar{h}A_s\Delta T_{lm}$ |

---

## Textbook References

- **Incropera & DeWitt:** Sections 8.1–8.5 (Internal Flows)
- **Holman & Bhattacharya:** Chapters 5 & 6

---

## Connected Modules

- [Module 4](05_convection_external.md) — External flow BL; same dimensionless groups
- [Module 7](08_heat_exchangers.md) — LMTD and energy balance appear directly in HX design
