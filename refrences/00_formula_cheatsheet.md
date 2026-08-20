# HTOA 2025 — Master Formula Cheat Sheet
> All key equations from the full course, July–November 2025.

---

## 0. Governing Equations (Continuum Mechanics)

| Equation | Formula |
|----------|---------|
| Continuity | $\partial\rho/\partial t + \nabla\cdot(\rho\underline{v}) = 0$ |
| Momentum (N-S) | $\rho D\underline{v}/Dt = \rho\underline{g} + \nabla\cdot\underline{\underline{\sigma}}$ |
| Energy | $\rho C_p DT/Dt = -\nabla\cdot\underline{q} + \Phi_v$ |
| Stress tensor (Newtonian) | $\underline{\underline{\sigma}} = -p\underline{\underline{\delta}} + \mu[(\nabla\underline{v})+(\nabla\underline{v})^T]$ |
| Fourier's law | $\underline{q} = -k\nabla T$ |

---

## 1. Modes of Heat Transfer

| Mode | Formula | Units of $q$ |
|------|---------|-------------|
| Conduction | $q = -k\,dT/dx$ | W/m² |
| Convection | $q = h(T_s - T_\infty)$ | W/m² |
| Radiation | $q = \varepsilon\sigma(T_s^4 - T_{sur}^4)$ | W/m² |

---

## 1b. Heat Equation — Full Forms

| Condition | Equation |
|-----------|----------|
| General (solid) | $\partial T/\partial t = \alpha\nabla^2 T + \dot{H}_v/(\rho C_p)$ |
| Steady, no gen | $\nabla^2 T = 0$ (Laplace) |
| Steady, with gen | $\nabla^2 T + \dot{H}_v/k = 0$ (Poisson) |
| Transient, no gen | $\partial T/\partial t = \alpha\nabla^2 T$ (Heat equation) |

**Thermal diffusivity:** $\alpha = k/(\rho C_p)$ [m²/s]

**Macroscopic balance:** $\dot{E}_{in} - \dot{E}_{out} + \dot{E}_{gen} = dE_{acc}/dt$

---

## 2. Thermal Resistances

| Geometry | $R_{cond}$ [K/W] |
|----------|-----------------|
| Plane wall | $L/(kA)$ |
| Cylindrical shell | $\ln(r_o/r_i)/(2\pi kL)$ |
| Spherical shell | $(1/r_i - 1/r_o)/(4\pi k)$ |
| Convection (any) | $1/(hA)$ |
| Contact | $R_c'' / A$ |

**Critical insulation radius:** $r_{o,crit} = k_{ins}/h$

---

## 3. Conduction — 1D Special Solutions

**Cylinder with heat generation:**
$$T(r) = T_s + \frac{\dot{q}}{4k}(R^2 - r^2), \quad T_{max} = T_s + \frac{\dot{q}R^2}{4k}$$

**Plane wall with heat generation:**
$$T(x) = T_s + \frac{\dot{q}}{2k}(L^2 - x^2)$$

---

## 4. Conduction — 2D (Separation of Variables)

**Laplace equation:** $\nabla^2 T = 0$

**Solution for rectangle ($0\le x\le L$, $0\le y\le W$), $\Theta = 1$ at $y = W$, $\Theta = 0$ elsewhere:**

$$\Theta(x,y) = \frac{2}{\pi}\sum_{n=1,3,5,...}\frac{1}{n}\sin\!\left(\frac{n\pi x}{L}\right)\frac{\sinh(n\pi y/L)}{\sinh(n\pi W/L)}$$

**Fourier coefficient:**
$$A_m = \frac{\int_a^b f(x)\,g_m(x)\,dx}{\int_a^b g_m^2(x)\,dx}$$

---

## 5. Numerical FDM

| Node Type | Equation |
|-----------|----------|
| Interior | $T_{m+1,n} + T_{m-1,n} + T_{m,n+1} + T_{m,n-1} - 4T_{m,n} = 0$ |
| Edge (convection) | $T_{m,n}(Bi+2) - (Bi)T_\infty - \frac{1}{2}[2T_{m-1,n}+T_{m,n+1}+T_{m,n-1}] = 0$ |
| Mesh Biot number | $Bi = h\Delta x/k$ |

**Lumped Capacitance** (valid when $Bi_s = hL_c/k < 0.1$):
$$\frac{T-T_\infty}{T_i - T_\infty} = e^{-t/\tau}, \quad \tau = \frac{\rho C_v V}{hA}$$

---

## 6. Dimensionless Numbers

| Number | Formula | Meaning |
|--------|---------|---------|
| $Re$ | $\rho u L/\mu$ | Inertia / Viscous |
| $Nu$ | $hL/k$ | Convective / Conductive HT |
| $Pr$ | $\nu/\alpha = \mu C_p/k$ | Momentum / Thermal diffusivity |
| $Bi$ | $hL/k_\text{solid}$ | Surface convection / Internal conduction |
| $St$ | $h/(\rho u C_p)$ | HT / Thermal capacity of flow |
| $Pe$ | $Re\cdot Pr$ | Advection / Diffusion |
| $Gr$ | $g\beta\Delta T L^3/\nu^2$ | Buoyancy / Viscous² |
| $Ra$ | $Gr\cdot Pr$ | Free convection parameter |

**Key relation:** $St\cdot Re\cdot Pr = Nu$

---

## 7. External Forced Convection (Flat Plate)

**Film temperature:** $T_f = (T_s + T_\infty)/2$

| Regime | $Nu$ Correlation | Validity |
|--------|-----------------|----------|
| Laminar (local) | $Nu_x = 0.453\,Re_x^{1/2}\,Pr^{1/3}$ | $Pr \ge 0.6$ |
| Laminar (average) | $\overline{Nu}_L = 0.664\,Re_L^{1/2}\,Pr^{1/3}$ | $Re_L < 5\times10^5$ |
| Turbulent (average, fully turb.) | $\overline{Nu}_L = 0.037\,Re_L^{4/5}\,Pr^{1/3}$ | $Re_L > 5\times10^5$ |
| Const. heat flux lam. local | $Nu_x = 0.453\,Re_x^{1/2}\,Pr^{1/3}$ | $Pr \ge 0.6$ |
| Const. heat flux turb. local | $Nu_x = 0.0308\,Re_x^{4/5}\,Pr^{1/3}$ | $0.6\le Pr\le60$ |

**Transition:** $Re_{x_c} = 5\times10^5$

---

## 8. Internal Flows

| Quantity | Formula |
|----------|---------|
| Hydraulic entry length (lam.) | $x_{fd,h} = 0.05\,Re_D\,D$ |
| Thermal entry length (lam.) | $x_{fd,t} = 0.05\,Re_D\,Pr\,D$ |
| $Nu$ lam., const. $q_s''$ | $4.36$ |
| $Nu$ lam., const. $T_s$ | $3.66$ |
| Dittus-Boelter (turbulent) | $Nu = 0.023\,Re_D^{4/5}\,Pr^n$ ($n=0.4$ heating, $0.3$ cooling) |
| Dittus-Boelter validity | $0.6\le Pr\le160$, $Re_D\ge10{,}000$, $L/D\ge10$ |
| Total tube heat rate | $q = \dot{m}C_p(T_{m,o}-T_{m,i})$ — valid all conditions |
| Const. flux: $T_m$ rise | $dT_m/dx = q_s''P/(\dot{m}C_p) = \text{const}$, so $q_{conv} = q_s''PL$ |
| Const. $T_s$: $T_m$ decay | $(T_s-T_m(x))/(T_s-T_{m,i}) = \exp(-Px\bar{h}/(\dot{m}C_p))$ |
| Energy balance | $q = \dot{m}C_p\Delta T_m = \bar{h}A_s\Delta T_{lm}$ |
| Sieder-Tate | $Nu = 0.023\,Re_D^{4/5}\,Pr^{1/3}(\mu/\mu_s)^{0.14}$ |
| Colburn j-factor | $j_H = St\,Pr^{2/3}(\mu/\mu_s)^{-0.14} = 0.023\,Re^{-0.2} = f/2$ |
| Colburn analogy | $St\,Pr^{2/3} = f/8$ |

---

## 9. Extended Surfaces (Fins)

**Fin parameter:** $m = \sqrt{hP/(kA_c)}$

**Fin ODE:** $d^2\theta/dx^2 - m^2\theta = 0$, where $\theta = T - T_\infty$

| Tip Condition | $\theta(x)/\theta_b$ | $q_f$ |
|---------------|---------------------|-------|
| Adiabatic tip | $\cosh[m(L-x)]/\cosh(mL)$ | $\sqrt{hPkA_c}\,\theta_b\tanh(mL)$ |
| Prescribed $T_L$ | — | — |
| Semi-infinite | $e^{-mx}$ | $\sqrt{hPkA_c}\,\theta_b$ |

**Fin efficiency:** $\eta_f = \tanh(mL)/(mL)$ (adiabatic tip)

**Fin effectiveness:** $\varepsilon_f = q_f/(hA_{c,b}\theta_b)$

---

## 10. Heat Exchangers

| Quantity | Formula |
|----------|---------|
| Overall energy | $q = \dot{m}_h C_{p,h}(T_{h,i}-T_{h,o}) = \dot{m}_c C_{p,c}(T_{c,o}-T_{c,i})$ |
| LMTD | $\Delta T_{lm} = (\Delta T_1 - \Delta T_2)/\ln(\Delta T_1/\Delta T_2)$ |
| Heat transfer | $q = UA\Delta T_{lm}$ (parallel/counter) or $q = UAF\Delta T_{lm,CF}$ |
| $U$ (cylinder) | $1/U_o = (D_o/D_i)/h_i + D_o\ln(D_o/D_i)/(2k) + 1/h_o$ |
| With fouling | $1/U_f = 1/U_c + R_{f,i}''A_o/A_i + R_{f,o}''$ |
| $q_{max}$ | $C_{min}(T_{h,i}-T_{c,i})$, where $C_{min} = \min(\dot{m}_h C_{p,h},\,\dot{m}_c C_{p,c})$ |
| Effectiveness (hot) | $\varepsilon = C_h(T_{h,i}-T_{h,o})\,/\,[C_{min}(T_{h,i}-T_{c,i})]$ |
| Effectiveness (cold) | $\varepsilon = C_c(T_{c,o}-T_{c,i})\,/\,[C_{min}(T_{h,i}-T_{c,i})]$ |
| Heat from ε | $q = \varepsilon\,C_{min}(T_{h,i}-T_{c,i})$ |
| NTU | $UA/C_{min}$ |
| Counter-flow ε | $[1-\exp(-NTU(1-C_r))]\,/\,[1-C_r\exp(-NTU(1-C_r))]$ |
| Phase-change ε | $1 - e^{-NTU}$ (when $C_r = 0$) |

---

## 11. Free (Natural) Convection

**Boussinesq:** $(\rho_\infty - \rho) = \rho\beta(T - T_\infty)$

**Thermal expansion:** $\beta = -(1/\rho)(\partial\rho/\partial T)_p$ [K⁻¹]; for ideal gas: $\beta = 1/T$

**Grashof number:** $Gr_L = g\beta(T_s-T_\infty)L^3/\nu^2$

**Rayleigh number:** $Ra_L = Gr_L\cdot Pr$

**Vertical plate (Churchill-Chu):**
$$\overline{Nu}_L = \left[0.825 + \frac{0.387\,Ra_L^{1/6}}{(1+(0.492/Pr)^{9/16})^{8/27}}\right]^2$$

---

## 12. Boiling — Additional Dimensionless Groups

| Number | Formula | Physical Meaning |
|--------|---------|-----------------|
| Jakob | $Ja = C_p\Delta T/h_{fg}$ | Sensible heat / Latent heat |
| Bond | $Bo = g(\rho_\ell-\rho_v)L^2/\sigma$ | Buoyancy / Surface tension |

**Boiling Nu depends on:** $Nu_L = f\!\left[\rho g(\rho_\ell-\rho_v)L^3/\mu^2,\;Ja,\;Pr,\;Bo\right]$ (Buckingham Π)

**Phase-change heat transfer differs from single-phase** by involving: $h_{fg}$, $\sigma$, and $(\rho_\ell - \rho_v)$

---

## 12b. Boiling

**Young-Laplace:** $p_v - p_\ell = 2\sigma/r$

**Change in surface area:** $\Delta A = 8\pi r\,\Delta r$ (for bubble expanding by $\Delta r$)

**Rohsenow (nucleate boiling):**
$$q_s'' = \mu_\ell h_{fg}\left[\frac{g(\rho_\ell-\rho_v)}{\sigma}\right]^{1/2}\left[\frac{C_{p,\ell}(T_s-T_{sat})}{C_{sf}h_{fg}Pr_\ell^n}\right]^3$$

**Zuber (critical heat flux):**
$$q''_{max} = 0.131\,h_{fg}\,\rho_v\left[\frac{\sigma g(\rho_\ell-\rho_v)}{\rho_v^2}\right]^{1/4}$$

---

## 13. Condensation

**Modified latent heat:** $h'_{fg} = h_{fg} + 0.68\,C_{p,\ell}(T_{sat}-T_s)$

| Geometry | $\bar{h}$ Correlation |
|----------|----------------------|
| Vertical plate | $0.943\left[\rho_\ell g(\rho_\ell-\rho_v)h'_{fg}k_\ell^3 / (\mu_\ell L\Delta T)\right]^{1/4}$ |
| Horizontal tube | $0.729\left[\rho_\ell g(\rho_\ell-\rho_v)h'_{fg}k_\ell^3 / (\mu_\ell D\Delta T)\right]^{1/4}$ |
| Sphere | $0.826\left[\cdots\right]^{1/4}$ |
| $N$ horizontal tubes | $\bar{h}_N = \bar{h}_1\cdot N^{-1/4}$ |

---

## 14. Evaporation

**Single-effect energy balance:**
$$q = \dot{m}_s h_{fg,s} \approx \dot{m}_V h_{fg,V} + \dot{m}_F C_{p,F}(T_{bp}-T_F)$$

**Mass balance:** $\dot{m}_F x_F = \dot{m}_L x_L$ (solute)

**Full heat balance:** $Fh_F + S\lambda = Lh_L + VH_v$ where $\lambda = H_s - h_s$ (steam latent heat)

**Economy:** $E = V/S = \dot{m}_V/\dot{m}_s \approx 0.85N$ (for $N$-effect evaporator)

**Capacity** = kg water vaporised/hr; **Steam consumption** = Capacity/Economy

**Area:** $A = S\lambda\,/\,(U\Delta T)$

---

*All properties for external flow at film temperature $T_f = (T_s+T_\infty)/2$;  
for internal flow at mean temperature $T_m$;  
for condensation at $T_f = (T_s+T_{sat})/2$.*
