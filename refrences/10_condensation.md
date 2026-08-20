# Module 9 — Condensation & Evaporation
**Dates:** 12 Nov, 17 Nov 2025  
**Sources:** `htoa2512nov.pdf` (14 pages), `htoa2512nov_notes.pdf` (14 pages), `htoa2517novfull.pdf`

**Textbooks:** Incropera & DeWitt Sec. 10.9 · McCabe & Smith Ch. 16 · C.J. Geankoplis Ch. 8

---

## Overview

**Condensation** occurs when vapour contacts a surface below the saturation temperature — vapour gives up latent heat and changes to liquid. **Evaporation** concentrates a solution by removing the volatile solvent (usually water) through boiling. Both are critical in chemical engineering: distillation, refrigeration, power cycles, food processing.

---

## Part A: Condensation

---

## A1. Types of Condensation

| Type | Description | Heat Transfer |
|------|-------------|---------------|
| **Film condensation** | Liquid film covers entire surface; vapour condenses onto film | Lower (film adds resistance) |
| **Dropwise condensation** | Liquid forms discrete drops, rolls off; surface constantly renewed | Much higher (2–10× film) |

Film condensation is the more common case in engineering (most surfaces are wettable).

---

## A2. Film Condensation — Nusselt Theory (Vertical Plate)

**Setup:** Vapour at $T_{sat}$ condenses on a cooled vertical plate at $T_s < T_{sat}$. A liquid film grows from top to bottom.

**Nusselt's analytical result for a vertical plate of height $L$:**

$$\overline{Nu}_L = \frac{\bar{h}_L L}{k_\ell} = 0.943\left[\frac{\rho_\ell(\rho_\ell - \rho_v)g\,h'_{fg}\,L^3}{\mu_\ell\,k_\ell(T_{sat} - T_s)}\right]^{1/4}$$

**Modified latent heat:**

$$h'_{fg} = h_{fg} + 0.68\,C_{p,\ell}(T_{sat} - T_s)$$

(Accounts for sensible cooling of the condensate film below $T_{sat}$.)

### Properties (evaluated at film temperature $T_f = (T_s + T_{sat})/2$):
- $\rho_\ell$ = liquid density
- $\rho_v$ = vapour density (usually $\rho_v \ll \rho_\ell$, so $\rho_\ell - \rho_v \approx \rho_\ell$)
- $\mu_\ell$ = liquid dynamic viscosity
- $k_\ell$ = liquid thermal conductivity
- $h_{fg}$ = latent heat of vaporisation at $T_{sat}$

---

## A3. Film Condensation on Radial Systems (12 Nov)

### Horizontal Tube or Sphere

From the lecture (Sec. 10.9 in Incropera & DeWitt):

$$\overline{Nu}_D = \frac{\bar{h}_D D}{k_\ell} = C\left[\frac{\rho_\ell g(\rho_\ell - \rho_v)\,h'_{fg}\,D^3}{\mu_\ell\,k_\ell(T_{sat} - T_s)}\right]^{1/4}$$

Where the constant $C$ depends on geometry:

$$C = \begin{cases} 0.826 & \text{for a sphere} \\ 0.729 & \text{for a horizontal tube} \end{cases}$$

**Note:** The horizontal tube correlation ($C = 0.729$) gives **higher** $\bar{h}$ than the vertical plate ($C = 0.943$) because the film drains sideways and stays thinner.

### Multiple Horizontal Tubes (Vertical Tier)

For $N$ tubes stacked vertically, condensate from upper tubes drips onto lower ones, thickening the film:

$$\bar{h}_{D,N} = \bar{h}_{D,1} \cdot N^{-1/4}$$

This means each additional tube row reduces the average coefficient — an important practical consideration for condenser design.

---

## A4. Condensation Regime — Reynolds Number

The **condensate film Reynolds number** determines whether the film is laminar or turbulent:

$$Re_\delta = \frac{4\dot{m}}{\mu_\ell P} = \frac{4\bar{h}(T_{sat} - T_s)L}{\mu_\ell h'_{fg}}$$

where $\dot{m}$ = condensate mass flow rate, $P$ = wetted perimeter.

| Regime | $Re_\delta$ |
|--------|------------|
| Laminar (wavy-free) | $Re_\delta < 30$ |
| Wavy-laminar | $30 < Re_\delta < 1800$ |
| Turbulent | $Re_\delta > 1800$ |

Nusselt's theory applies strictly to the laminar regime. For turbulent film condensation, empirical correlations (Labuntsov or Chun-Seban) apply.

---

## Part B: Evaporation

---

## B1. What is Evaporation?

**Evaporation** (from McCabe & Smith Ch. 16 and Geankoplis Ch. 8) concentrates a solution by evaporating the volatile solvent:

> "Concentrate a solution consisting of a **non-volatile solute** and a **volatile solvent** (usually water)"

It differs from boiling because the goal is not to produce vapour as the product but to concentrate the **remaining liquid**.

---

## B2. Single-Effect Evaporator

**Schematic (12 Nov notes):**

```
                    ↑ Vapour out
                    |
         ┌──────────────────────┐
Feed →   │   ≈≈≈≈≈≈≈≈  (liquid)|
Steam → ════════════════════════ ← Condensate out
         │   [tubes for HT]    │
         └──────────┬───────────┘
                    ↓ Concentrated liquid out
```

- Steam (or other hot utility) enters tubes → condenses, giving up $h_{fg}$
- Feed enters → heated to boiling point → solvent evaporates
- Vapour exits the top; concentrated liquid exits the bottom; steam condensate exits separately

**Energy balance on single-effect evaporator:**

$$q = UA_s \Delta T = \dot{m}_s h_{fg,s} = \dot{m}_V h_{fg,V} + \dot{m}_F C_{p,F}(T_{bp} - T_F)$$

where:
- $\dot{m}_s$ = steam (heating medium) mass flow rate
- $\dot{m}_V$ = evaporation rate of solvent (vapour produced)
- $\dot{m}_F$ = feed flow rate
- $T_{bp}$ = boiling point of solution
- $\Delta T = T_s - T_{bp}$ (driving force)
- $A_s$ = heat transfer area of the evaporator

**Mass balance:**
$$\dot{m}_F = \dot{m}_V + \dot{m}_L \qquad \dot{m}_F x_F = \dot{m}_L x_L$$

where $x$ = solute mass fraction.

---

## B3. Multiple-Effect Evaporation

**Key idea:** Use the vapour from one effect as the heating medium for the next effect, reducing total steam consumption.

```
Feed →  [Effect 1]  →  [Effect 2]  →  [Effect 3]  → Conc. product
Steam →              V1 heats E2    V2 heats E3
                    (at lower T, P)  (even lower T, P)
```

**Economy** = kg water evaporated per kg steam consumed.  
Single-effect: economy ≈ 0.8–0.9 (< 1)  
N-effect: economy ≈ N × 0.8–0.9

**Trade-off:** More effects = lower steam cost but higher capital cost (more vessels, pumps, controls).

---

## B3b. Evaporator Performance Metrics (12 Nov)

**Capacity** = Number of kg of water vaporised per hour [kg/hr]

**Economy** = $\dfrac{\text{kg of water vaporised per hour}}{\text{kg of steam fed to unit per hour}}$

**Steam consumption per hour** = $\dfrac{\text{Capacity}}{\text{Economy}}$

---

## B3c. Full Evaporator Energy Balance (12 Nov)

**Variables:**
- $F$ = feed flow rate [kg/s], enthalpy $h_F$ [J/kg]
- $S$ = steam flow rate [kg/s], vapour enthalpy $H_s$, condensate enthalpy $h_s$
- $L$ = concentrated liquid flow rate [kg/s], enthalpy $h_L$
- $V$ = vapour produced [kg/s], enthalpy $H_v$

**Total mass balance:**

$$F = L + V$$

**Solute mass balance:**

$$F\,x_F = L\,x_L$$

**Full heat balance (assuming no heat loss):**

$$(\text{heat in feed}) + (\text{heat in steam}) = (\text{heat in conc. liquid}) + (\text{heat in vapour}) + (\text{heat in condensate})$$

$$F h_F + S H_s = L h_L + V H_v + S h_s$$

Since steam gives off only its **latent heat** $\lambda = H_s - h_s$:

$$\boxed{F h_F + S\lambda = L h_L + V H_v}$$

**Heat transferred within evaporator:**

$$q = S\lambda = S(H_s - h_s)$$

**Note:** For solutions with a **heat of dilution** (e.g., $H_2SO_4$, $NaOH$, $CaCl_2$), an additional term must be added to the energy balance. The heat of dilution can be positive (exothermic dilution) or negative (endothermic).

**Required heat transfer area:**

$$A = \frac{q}{U\,\Delta T} = \frac{S\lambda}{U(T_{steam} - T_{bp})}$$

---

## B4. Boiling Point Rise (BPR)

Dissolving a solute raises the boiling point above pure solvent:

$$T_{bp,solution} = T_{bp,solvent} + BPR$$

BPR depends on the solute and its concentration. This reduces the effective driving temperature difference $\Delta T$ in the evaporator:

$$\Delta T_{effective} = (T_{steam} - T_{bp,solvent}) - BPR$$

---

## Summary of Key Equations

### Condensation

| Geometry | Correlation | Constant |
|----------|-------------|----------|
| Vertical plate | $\bar{h} = 0.943[...]^{1/4}$ | — |
| Horizontal tube | $\bar{h} = 0.729[...]^{1/4}$ | $C = 0.729$ |
| Sphere | $\bar{h} = 0.826[...]^{1/4}$ | $C = 0.826$ |
| $N$ tubes vertical tier | $\bar{h}_N = \bar{h}_1 N^{-1/4}$ | — |

All correlations use: $\left[\dfrac{\rho_\ell g(\rho_\ell - \rho_v)h'_{fg}D^3}{\mu_\ell k_\ell(T_{sat}-T_s)}\right]^{1/4}$

### Evaporation

| Quantity | Formula |
|----------|---------|
| Overall energy balance | $q = \dot{m}_s h_{fg,s} = \dot{m}_V h_{fg,V} + \text{sensible}$ |
| Mass balance | $\dot{m}_F x_F = \dot{m}_L x_L$ |
| Economy (single) | $E = \dot{m}_V / \dot{m}_s \approx 0.8$–$0.9$ |
| Economy ($N$-effect) | $E \approx N \times 0.85$ |

---

## Textbook References

- **Incropera & DeWitt:** Sec. 10.9 (Film Condensation on Radial Systems)
- **McCabe & Smith:** Chapter 16 (Evaporation)
- **C.J. Geankoplis:** Chapter 8 (Evaporation)
- Self-study: Sub-part 1 of Solved example 10.4 in Incropera & DeWitt

---

## Connected Modules

- [Module 7](08_heat_exchangers.md) — Condensers & evaporators are specialised HX; ε-NTU with $C_r = 0$
- [Module 8](09_free_convection_boiling.md) — Boiling is the reverse process to condensation
