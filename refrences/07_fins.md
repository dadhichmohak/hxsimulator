# Module 6 — Extended Surfaces (Fins)
**Dates:** 8 Sep 2025 (critical insulation thickness), 17 Nov 2025 (fin analysis)  
**Sources:** `htoa258sep.pdf`, `htoa2517novfull.pdf`

**Textbook Reference:** Fig. 2.18 and associated derivation in Holman & Bhattacharya

---

## Overview

**Extended surfaces (fins)** are appendages attached to a base surface to enhance heat transfer by increasing effective surface area. They are ubiquitous in engineering: heat sinks for electronics, radiators, economisers, engine cooling fins. This module covers the governing ODE for a fin, its general and specific solutions, and the critical insulation thickness problem.

---

## 1. Critical Thickness of Insulation (8 Sep)

See detailed treatment in [Module 1](02_conduction_fundamentals.md), Section 5.

**Key result:**

$$r_{o,crit} = \frac{k_{insulation}}{h}$$

Adding insulation to a cylinder **increases** heat loss until $r_o = k/h$, then decreases it. Relevant for wire insulation, pipe lagging.

---

## 2. Physical Setup for a Fin (17 Nov)

A fin is an extended surface of **variable or uniform cross-section** $A_c(x)$ attached at $x = 0$ (base, temperature $T_b$) and projecting into a fluid at $T_\infty$.

**Energy balance on an element $dx$** at steady state (from lecture, Fig. 2.18 logic):

$$\text{Energy in (left face)} = \text{Energy out (right face)} + \text{Energy lost by convection}$$

$$q_x = q_{x+dx} + dq_{conv}$$

$$q_x = \left[q_x + \frac{dq_x}{dx}dx\right] + h\,dA_s\,(T_s - T_\infty)$$

Simplifying:

$$-\frac{dq_x}{dx}dx = h\,dA_s\,(T - T_\infty)$$

Substituting Fourier's law $q_x = -kA_c\frac{dT}{dx}$:

$$\frac{d}{dx}\left(A_c\frac{dT}{dx}\right) - \frac{h}{k}\frac{dA_s}{dx}(T - T_\infty) = 0$$

**General energy equation for an extended surface:**

$$\boxed{\frac{d^2T}{dx^2} + \left(\frac{1}{A_c}\frac{dA_c}{dx}\right)\frac{dT}{dx} - \left(\frac{1}{A_c}\frac{h}{k}\frac{dA_s}{dx}\right)(T - T_\infty) = 0}$$

---

## 3. Uniform Cross-Section Fin

For a fin of **constant cross-sectional area** $A_c = \text{const}$:

$$\frac{dA_c}{dx} = 0 \qquad \frac{dA_s}{dx} = P \quad \text{(perimeter)}$$

The general equation simplifies to:

$$\frac{d^2T}{dx^2} - \frac{hP}{kA_c}(T - T_\infty) = 0$$

Define the **excess temperature**:

$$\theta(x) \equiv T(x) - T_\infty$$

Define the **fin parameter**:

$$\boxed{m^2 = \frac{hP}{kA_c}}$$

The ODE becomes:

$$\boxed{\frac{d^2\theta}{dx^2} - m^2\theta = 0}$$

This is a **second-order linear ODE with constant coefficients**.

---

## 4. General Solution

The general solution is:

$$\theta(x) = C_1 e^{mx} + C_2 e^{-mx}$$

Or equivalently in hyperbolic form:

$$\theta(x) = C_1 \cosh(mx) + C_2 \sinh(mx)$$

**Boundary conditions depend on the tip condition:**

### BC 1 — At Base ($x = 0$):

$$\theta(0) = T_b - T_\infty \equiv \theta_b$$

### BC 2 — At Tip ($x = L$): Several cases

| Tip Condition | BC at $x = L$ | Physical Meaning |
|---------------|---------------|-----------------|
| Insulated tip | $\frac{d\theta}{dx}\big|_{x=L} = 0$ | No heat escapes tip |
| Prescribed temp. | $\theta(L) = \theta_L$ | Tip held at $T_L$ |
| Convection at tip | $-k\frac{d\theta}{dx}\big|_L = h\theta(L)$ | Tip also convects |
| Semi-infinite fin | $\theta(L \to \infty) = 0$ | Fin long, cools to ambient |

---

## 5. Solution — Insulated Tip (Most Common Case)

For an **adiabatic tip** ($d\theta/dx = 0$ at $x = L$):

$$\boxed{\frac{\theta(x)}{\theta_b} = \frac{\cosh[m(L-x)]}{\cosh(mL)}}$$

**Total heat transfer rate through the fin base:**

$$q_f = -kA_c\left.\frac{dT}{dx}\right|_{x=0} = \sqrt{hPkA_c}\,\theta_b \tanh(mL) = M\tanh(mL)$$

where $M = \sqrt{hPkA_c}\,\theta_b$ is a reference heat transfer quantity.

---

## 6. Solution — Semi-Infinite Fin

For a very long fin ($L \to \infty$, $\theta \to 0$ at $\infty$):

$$\theta(x) = \theta_b\, e^{-mx}$$

$$q_f = M = \sqrt{hPkA_c}\,\theta_b$$

---

## 7. Fin Efficiency and Effectiveness

### Fin Efficiency

$$\eta_f = \frac{q_f}{q_{f,max}} = \frac{\text{Actual heat transfer from fin}}{\text{Heat transfer if entire fin were at }T_b}$$

$$q_{f,max} = h A_{f}\, \theta_b$$

For an insulated-tip fin:

$$\eta_f = \frac{\tanh(mL)}{mL}$$

- High $\eta_f$ (close to 1): fin material conducts heat well relative to surface convection
- Low $\eta_f$: fin is long/poorly conducting → tip approaches ambient → wasted material

### Fin Effectiveness

$$\varepsilon_f = \frac{q_f}{h A_{c,b}\,\theta_b}$$

- $\varepsilon_f > 2$: fin is worthwhile (rule of thumb)
- To maximise effectiveness: use high-$k$ material, thin fins, low-$h$ environments (fins most valuable in air, less so in high-$h$ boiling)

---

## 8. Overall Surface Efficiency (Fin Arrays)

For a surface with $N$ fins of area $A_f$ and unfinned area $A_u$:

$$\eta_o = 1 - \frac{NA_f}{A_t}(1 - \eta_f) \qquad A_t = NA_f + A_u$$

**Effective total resistance:**

$$R_{th} = \frac{1}{\eta_o h A_t}$$

---

## 9. Design Summary

| Parameter | Effect on Performance |
|-----------|----------------------|
| $\uparrow k$ | $\uparrow \eta_f$, $\uparrow q_f$ |
| $\uparrow h$ | $\downarrow \eta_f$ (harder to transport from tip), but $\uparrow q_f$ overall |
| $\uparrow L$ | Initially $\uparrow q_f$, then diminishing returns ($\tanh \to 1$) |
| $\uparrow P/A_c$ | $\uparrow m$ → better performance per unit mass (e.g., thin fins) |

---

## Textbook References

- **Incropera & DeWitt:** Chapter 3 (Extended Surfaces, Sec. 3.6–3.7)
- **Holman & Bhattacharya:** Chapter 2, Fig. 2.18 and derivation

---

## Connected Modules

- [Module 1](02_conduction_fundamentals.md) — Critical insulation thickness (same file, 8 Sep)
- [Module 7](08_heat_exchangers.md) — Fin arrays are used inside HX tubes and on shell sides
