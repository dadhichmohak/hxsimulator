# Module 7 — Heat Exchangers
**Dates:** 11 Sep, 8 Oct, 14 Oct, 22 Oct, 23 Oct 2025  
**Sources:** `htoa2511sep.pdf`, `htoa258oct.pdf`, `htoa2514oct.pdf`, `htoa2522oct.pdf`, `htoa2522oct1.pdf`, `htoa2523oct.pdf`, `htoa2523oct1.pdf`

**Textbooks:** Incropera & DeWitt Ch. 11 (Sec. 11.4) · Holman & Bhattacharya · McCabe & Smith

---

## Overview

A **heat exchanger (HX)** transfers heat between two fluid streams without mixing them. Applications: power plants, refrigeration, chemical processing, HVAC. This module develops the two standard analysis methods: **LMTD** and **Effectiveness-NTU**, plus real-world corrections for fouling and multi-pass arrangements.

---

## 1. Double-Pipe Heat Exchanger (11 Sep)

### Physical Setup

```
Hot fluid →  ṁh, (Th,i) ————————————————→ (Th,o)
             ══════════════════════════════
Cold fluid → ṁc, (Tc,i) ————————————————→ (Tc,o)
```

**Assumptions (from lecture):**
- Fluids are not undergoing a phase change
- Steady-state operation
- Negligible heat loss to surroundings
- Constant specific heats

### Overall Energy Balance

At steady state:

$$\boxed{q = \dot{m}_h C_{p,h}(T_{h,i} - T_{h,o}) = \dot{m}_c C_{p,c}(T_{c,o} - T_{c,i})}$$

- Heat lost by hot fluid = heat gained by cold fluid

### Parallel Flow vs Counter Flow

| Configuration | Definition | Approach temperatures |
|---------------|-----------|----------------------|
| Parallel flow | Both fluids flow in same direction | $\Delta T_1 = T_{h,i} - T_{c,i}$; $\Delta T_2 = T_{h,o} - T_{c,o}$ |
| Counter flow | Fluids flow in opposite directions | $\Delta T_1 = T_{h,i} - T_{c,o}$; $\Delta T_2 = T_{h,o} - T_{c,i}$ |

Counter flow always achieves better thermodynamic performance (closer outlet approach temperatures).

---

## 2. Log Mean Temperature Difference (LMTD) Method

### Derivation Basis

The local driving force for heat transfer varies along the HX length. The **LMTD** is the effective mean temperature difference:

$$\boxed{\Delta T_{lm} = \frac{\Delta T_1 - \Delta T_2}{\ln(\Delta T_1/\Delta T_2)}}$$

where $\Delta T_1$ and $\Delta T_2$ are the "approach" temperature differences at the two ends (hot end and cold end of the exchanger).

**Total heat transfer:**

$$q = U A_s \Delta T_{lm}$$

where $U$ = **overall heat transfer coefficient** [W/m²K], $A_s$ = total heat transfer area.

### Correction Factor for Multi-Pass HX

For shell-and-tube or cross-flow exchangers, the LMTD must be corrected:

$$q = U A_s F \Delta T_{lm,CF}$$

where $F$ = correction factor (from charts, depends on geometry and temperature ratio), and $\Delta T_{lm,CF}$ = LMTD computed assuming counter-flow.

---

## 3. Overall Heat Transfer Coefficient $U$

### 3.1 Flat Wall (Double-Pipe)

For a flat wall separating two fluids:

$$\frac{1}{UA} = \frac{1}{h_i A_i} + \frac{L}{kA} + \frac{1}{h_o A_o}$$

For a **cylindrical pipe** (14 Oct derivation):

$$\frac{1}{U_o} = \left(\frac{D_o}{D_i}\right)\frac{1}{h_i} + \frac{D_o \ln(D_o/D_i)}{2k} + \frac{1}{h_o}$$

Where:
- $h_i$ = **tube-side** heat transfer coefficient (calculated using Dittus-Boelter — "1-step calc")
- $h_o$ = **shell-side** coefficient (calculated using Donohue equation — "shell-side calc")
- $U_o$ is referenced to outer area $A_o = \pi D_o L$

### 3.2 Shell-Side: Donohue Equation

For shell-side flow in a shell-and-tube HX:

$$Nu_{D_o} = 0.2\,Re_{D_o}^{0.6}\,Pr^{0.33}$$

(Donohue equation — applicable to flow across tube bundles on the shell side.)

---

## 4. Fouling Factors (8 Oct)

### What is Fouling?

During normal HX operation, surfaces are subject to **fouling** — deposition of a film/scale due to:
- Fluid impurities
- Rust formation
- Reactions between fluid and wall material

**Effect:** Creates an additional thermal resistance → decreases overall heat transfer coefficient over time.

### Accounting for Fouling

The fouling resistance $R_f''$ [m²K/W] is added to the overall resistance:

$$\frac{1}{U_f} = \frac{1}{U_c} + R_{f,i}'' \frac{A_o}{A_i} + R_{f,o}''$$

where subscripts $c$ = clean, $f$ = fouled.

**Typical fouling resistances** (from standard tables):
- Seawater: $R_f'' \approx 1.0 \times 10^{-4}$ m²K/W
- Treated cooling water: $R_f'' \approx 1.5–2.0 \times 10^{-4}$ m²K/W
- Fuel oil: $R_f'' \approx 9.0 \times 10^{-4}$ m²K/W

---

## 4b. LMTD Full Derivation (11 Sep)

**Starting point:** Differential heat transfer across area element $dA$:

$$dq = U(T_h - T_c)\,dA = U\,\Delta T\,dA$$

**Assumptions for integration (4 key assumptions from lecture):**
1. Overall coefficient $U$ is constant along HX
2. $C_{p,h}$ and $C_{p,c}$ are constant
3. Heat exchange with ambient is negligible
4. Flow is either parallel (co-current) or antiparallel (counter-current)

**Integration over the whole HX:**

Using energy balances $dq = -C_h\,dT_h = C_c\,dT_c$, the local temperature difference $\Delta T = T_h - T_c$ satisfies:

$$\frac{d(\Delta T)}{\Delta T} = -UA\,\frac{d(\Delta T_2 - \Delta T_1)}{q}$$

Integrating from end 1 to end 2:

$$\ln\!\left(\frac{\Delta T_2}{\Delta T_1}\right) = -\frac{UA}{q}\left[(T_{h,i}-T_{h,o}) + (T_{c,o}-T_{c,i})\right] = \frac{UA}{q}(\Delta T_2 - \Delta T_1)$$

Rearranging:

$$\boxed{q = UA\cdot\frac{\Delta T_1 - \Delta T_2}{\ln(\Delta T_1/\Delta T_2)} = UA\cdot\Delta T_{lm}}$$

This is the **LMTD formula** — $\Delta T_1$ and $\Delta T_2$ are the temperature differences at the two ends.

---

## 4c. Worked Rating Example (22 Oct)

**Setup:** Counter-flow HX, $U = 2000\,\text{W/m}^2\text{K}$, $A = 10\,\text{m}^2$. Hot fluid: water, $C_h = \dot{m}_h C_{p,h} = 5556\,\text{W/K}$, enters at $120°C$. Cold fluid: $C_c = 5806\,\text{W/K}$, enters at $20°C$.

**From energy balance:**

$$q_{EB} = C_h(120 - T_{h,o}) = C_c(T_{c,o} - 20)$$

**From LMTD:**

$$q_{LMTD} = UA\cdot\Delta T_{lm}$$

Set $q_{EB} = q_{LMTD}$ and solve simultaneously (two equations, two unknowns: $T_{h,o}$ and $T_{c,o}$). This is an iterative or algebraic system.

---

## 5. HX Analysis vs. Design (22 Oct)

### Two Problem Types

| Problem Type | Also Called | Given | Find |
|-------------|-------------|-------|------|
| **Analysis** ("Rating") | Performance analysis | HX geometry + inlet temps | Outlet temps, q |
| **Design** | Sizing | Inlet & outlet temps | Area $A$, type of HX |

**Analysis problem:** Know $T_{h,i}$ and $T_{c,i}$. Check if desired outlet temperature can be achieved with the existing HX (or find what the outlet temps are).

**Design problem:** Inlet and outlet temperatures all known. Find:
(a) Type of HX required
(b) Heat transfer area $A$ required

---

## 6. Effectiveness-NTU Method (23 Oct)

The LMTD method requires knowing all four temperatures. The **ε-NTU method** is better when outlet temperatures are unknown (analysis problems).

**References:** Incropera & DeWitt Sec. 11.4

### Maximum Possible Heat Transfer

$$q_{max} = C_{min}(T_{h,i} - T_{c,i})$$

where:

$$C_{min} = \min(C_c, C_h) \qquad C_c = \dot{m}_c C_{p,c} \qquad C_h = \dot{m}_h C_{p,h}$$

**Physical reasoning:** The fluid with the smaller heat capacity rate ($C_{min}$) undergoes the maximum temperature change. If $C_c < C_h$: the cold fluid's temperature changes more, $|dT_c| > |dT_h|$.

### Effectiveness

$$\boxed{\varepsilon = \frac{q}{q_{max}} = \frac{\text{Actual heat transfer rate}}{\text{Maximum possible heat transfer rate}}}$$

Range: $0 \le \varepsilon \le 1$

For a counter-flow HX with $C_c < C_h$, the maximum happens as $L \to \infty$ (the cold fluid outlet approaches $T_{h,i}$).

### Number of Transfer Units (NTU)

$$NTU = \frac{UA}{C_{min}}$$

### ε-NTU Relations (Standard Results)

For a **parallel flow** HX:

$$\varepsilon = \frac{1 - \exp[{-NTU(1 + C_r)}]}{1 + C_r}$$

For a **counter-flow** HX:

$$\varepsilon = \frac{1 - \exp[{-NTU(1 - C_r)}]}{1 - C_r\exp[{-NTU(1 - C_r)}]}$$

where $C_r = C_{min}/C_{max}$ is the **heat capacity ratio**.

**Special case** ($C_{min}/C_{max} = 0$, i.e., one fluid is condensing/evaporating):

$$\varepsilon = 1 - e^{-NTU}$$

This applies to condensers and evaporators where one fluid undergoes phase change.

### Solving Analysis Problems with ε-NTU

1. Compute $C_h = \dot{m}_h C_{p,h}$ and $C_c = \dot{m}_c C_{p,c}$
2. Find $C_{min}$, $C_{max}$, $C_r = C_{min}/C_{max}$
3. Compute $NTU = UA/C_{min}$
4. Use appropriate ε-NTU relation to get $\varepsilon$
5. Compute $q = \varepsilon\, q_{max} = \varepsilon\, C_{min}(T_{h,i} - T_{c,i})$
6. Compute outlet temperatures from energy balance

### Effectiveness Expressed Using Fluid Temperatures

**In either case** (hot or cold fluid as $C_{min}$):

$$\varepsilon = \frac{C_h(T_{h,i} - T_{h,o})}{C_{min}(T_{h,i} - T_{c,i})} \quad \text{OR} \quad \varepsilon = \frac{C_c(T_{c,o} - T_{c,i})}{C_{min}(T_{h,i} - T_{c,i})}$$

In either case:

$$\boxed{q = \varepsilon\,C_{min}(T_{h,i} - T_{c,i})}$$

> **Lecture note (23 Oct):** "This form is good for analysis/rating problems" — when you know $\varepsilon$ from NTU and $C_r$, you immediately get $q$ and then outlet temperatures from energy balance.

**For any HX:** $\varepsilon \equiv f(NTU, C_r)$ — this is the key universal relationship.

### Heat Capacity Ratio

$$C_r = \frac{C_{min}}{C_{max}} \qquad 0 \le C_r \le 1$$

Also written as $R_c$ in some textbooks/charts.

$C_{min}/C_{max}$ = $C_c/C_h$ **or** $C_h/C_c$ depending on which is smaller.

### HX Total Area

For a shell-and-tube HX:

$$A = (\text{No. of tubes}) \times (\text{outer surface area of each tube}) = N_{tubes} \times \pi D_o L$$

**Example (14 Oct):** $A = 70.96\,\text{m}^2$

---

## 7. Summary of Key Equations

| Quantity | Formula |
|----------|---------|
| Overall energy balance | $q = \dot{m}_h C_{p,h}\Delta T_h = \dot{m}_c C_{p,c}\Delta T_c$ |
| LMTD | $\Delta T_{lm} = \frac{\Delta T_1 - \Delta T_2}{\ln(\Delta T_1/\Delta T_2)}$ |
| Heat transfer (LMTD) | $q = UA\Delta T_{lm}$ (or $UAF\Delta T_{lm,CF}$ for multi-pass) |
| Overall U (cylinder) | $1/U_o = (D_o/D_i)/h_i + D_o\ln(D_o/D_i)/(2k) + 1/h_o$ |
| Maximum heat transfer | $q_{max} = C_{min}(T_{h,i}-T_{c,i})$ |
| Effectiveness | $\varepsilon = q/q_{max}$ |
| NTU | $NTU = UA/C_{min}$ |

---

## Textbook References

- **Incropera & DeWitt:** Chapter 11 (Sec. 11.1–11.4)
- **Holman & Bhattacharya**
- **McCabe & Smith:** Heat transfer chapters

---

## Connected Modules

- [Module 5](06_convection_internal.md) — LMTD first appeared for pipe flow
- [Module 6](07_fins.md) — Fins are used on tube/shell surfaces to enhance $U$
- [Module 9](10_condensation.md) — Phase-change HX uses $\varepsilon = 1 - e^{-NTU}$
