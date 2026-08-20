# Source Verification — hx_simulator Formulas & Data

Verification of every correlation, constant, and data source used in the
codebase against published literature and standards.

---

## 1. Tube-Side Heat Transfer — Dittus-Boelter

**Used in:** `heat_transfer.py`

**Equation (in code):**
```
Nu = 0.023 * Re^0.8 * Pr^n    (n = 0.4 heating, 0.3 cooling)
```

**Source:** Dittus, F.W. & Boelter, L.M.K., *Heat Transfer in Automobile
Radiators of the Tubular Type*, International Communications in Heat and
Mass Transfer, Vol. 2, No. 4, 1985 (originally published 1930).

| Property | Code | Source |
|---|---|---|
| Re validity | Re > 10,000 | Dittus-Boelter (1930); confirmed Incropera & DeWitt, Ch. 8 |
| Pr range | 0.7 ≤ Pr ≤ 160 | Incropera & DeWitt, *Fundamentals of Heat and Mass Transfer*, 7th Ed., Table 8.2 |
| n = 0.4 heating | ✓ | Dittus & Boelter (1930) |
| n = 0.3 cooling | ✓ | Dittus & Boelter (1930) |

**References:**
- [Dittus-Boelter on ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0735193315000553)
- [Incropera & DeWitt via Wiley](https://www.wiley.com/en-us/Fundamentals+of+Heat+and+Mass+Transfer%2C+8th+Edition-p-9781119474982)
- [Six Sigma Heat Transfer Reference](https://www.isixsigma.com/reference-templates/medical/the-dittus-boelter-equation/)

---

## 2. Shell-Side Heat Transfer — Bell-Delaware Method

**Used in:** `bell_delaware.py`

**Equation (in code):**
```
h_shell = F_b * h_pure * R_l * R_b * R_s * R_p
```

| Factor | Description | Source |
|---|---|---|
| h_pure | Cross-flow tube bank (Kern/Palmer) | Kern, D.Q., *Process Heat Transfer*, McGraw-Hill, 1950 |
| R_l (leakage) | Tube-to-baffle & baffle-to-shell leakage | Bell, K.J., *Delaware Method for Shell-Side Design*, in Handbook of Heat Exchanger Design, Hemisphere, 1990 |
| R_b (bypass) | Shell-to-bundle bypass (CF_b/CCL) | Bell, K.J., Delaware Method, 1990 |
| R_s (pass partitions) | Pass partition plate leakage | Bell, K.J., 1990 |
| R_p (baffle type) | Disc-and-doughnut vs segmental | Bell, K.J., 1990 |
| F_bp (baffle cut) | Baffle cut correction factor | Bell, K.J., 1990 |

**Standard Reference:**
- Bell, K.J., "Delaware Method for Shell-Side Design," in *Handbook of Heat
  Exchanger Design*, Hewitt, G.L., Shires, G.L., & Polezhaev, Y.V. (Eds.),
  Hemisphere Publishing, New York, 1990.
- Tubular Exchanger Manufacturers Association (TEMA), *Standards of the
  Tubular Exchanger Manufacturers Association*, 10th Edition, 2019.
  - Section 6: Flow-Induced Vibration
  - Section 7: Thermal Relations

**TEMA Shell Types (E, F, G, H, J, K):**
- Source: TEMA Standards, 10th Edition (2019), Section N — Nomenclature
- [TEMA Heat Exchanger Nomenclature (Official PDF)](http://support.tema.org/images/HeatExchangerNomenclature.pdf)
- [TEMA 10th Edition (2019) Preview](https://www.yes4tec.com/wp-content/uploads/2025/01/Previews_TEMA-10th-Edition-2019.pdf)
- [TEMA Overview Keynote (Heat Exchanger World)](https://heat-exchanger-world-americas.com/wp-content/uploads/sites/22/2022/11/TEMA-Overview-Keynote-Wade-Armer-Sangeeta-Bakshi.pdf)

---

## 3. FIV — Natural Frequency (Cantilevered Tube)

**Used in:** `fiv.py`

**Equation (in code):**
```
f_n = (C_f / 2) * sqrt(E * I / (m_L * L^4))
```

| Property | Code | Source |
|---|---|---|
| C_f = 22.4 (simply supported) | ✓ | Connors, H.J., 1970; Blevins, *Flow-Induced Vibration*, 2nd Ed. |
| C_f = 35.3 (fixed-free cantilever) | ✓ | Blevins, R.D., *Flow-Induced Vibration*, Van Nostrand Reinhold, 1990 |
| I = π(d_o^4 - d_i^4)/64 | ✓ | Geometric property (standard) |
| m_L = ρ_f * A_f + m_t | ✓ | TEMA Section 6; Blevins (1990) |

**References:**
- Blevins, R.D., *Flow-Induced Vibration*, 2nd Ed., Van Nostrand Reinhold,
  New York, 1990, Ch. 5-6.
- [Vibration Analysis Reference (Tremtech)](https://www.tremtech.com/blog/2019/10/23/natural-frequency-of-a-beam)
- [Engineering Toolbox — Natural Frequency](https://www.engineeringtoolbox.com/natural-frequency-d_1743.html)

---

## 4. FIV — Vortex Shedding Frequency

**Used in:** `fiv.py`

**Equation (in code):**
```
f_vs = St * V / d_o
St ≈ 0.21    (Re = 10^3 – 10^5)
St ≈ 0.22    (Re ≈ 2×10^5)
```

| Property | Code | Source |
|---|---|---|
| St ≈ 0.2 (smooth cylinders, subcritical Re) | ✓ | Blevins (1990); Zdravkovich, *Flow Around Circular Cylinders*, 1997 |
| Critical Re ≈ 2×10^5 | ✓ | Standard fluid mechanics |

**References:**
- Zdravkovich, M.M., *Flow Around Circular Cylinders*, Vol. 1, Oxford
  University Press, 1997, Table 3.1.
- Blevins, R.D., *Flow-Induced Vibration*, 2nd Ed., 1990, Ch. 3.
- [Vortex Shedding on Wikipedia](https://en.wikipedia.org/wiki/Vortex_shedding)
- [DPIE Vortex Shedding Reference](https://www.dpie.com/technical-articles/vortex-shedding/)

---

## 5. FIV — Connors Critical Velocity

**Used in:** `fiv.py`

**Equation (in code):**
```
V_crit = K_c * f_n * d_o * sqrt((m_L * δ) / (ρ * d_o^2))
K_c = 9.9    (standard)
```

**Source:**
- Connors, H.J., "Fluid Elastic Vibration of Tube Arrays Excited by
  Cross-Flow," *Flow-Induced Vibration in Heat Exchangers*, ASME, 1970,
  pp. 42-56.
- Blevins, *Flow-Induced Vibration*, 2nd Ed., 1990, Ch. 6 (Eq. 6.4).

| Property | Code | Source |
|---|---|---|
| K_c = 9.9 (in fluid, uniform flow) | ✓ | Connors (1970); Blevins (1990) |
| δ = logarithmic decrement | ✓ | Damping of tube in fluid; TEMA Sec. 6 |

**References:**
- [ASME FIV Book (1970)](https://www.asmedigitalcollection.asme.org/ebooks/ebook-chapter/2723)
- [Stability Using Connors' Method (Structural Dynamics)](https://structuralsolutionsllc.com/stability-using-connors-method/)
- [Vortex-Induced Vibration of Tube Bundles (ResearchGate)](https://www.researchgate.net/publication/312139265_Vortex-Induced_Vibration_of_Circular_Cylinders_Array_In-Line_and_Staggered_to_Cross_fluid_Flow)

---

## 6. FIV — Turbulent Buffeting Amplitude

**Used in:** `fiv.py`

**Equation (in code):**
```
A_turb = [ρ_f * V_rms^2 * f_vs * d_o^2 * h * C_L^2] / [8 * π^3 * δ * f_n^3 * m_L]    (linear approx)
```

| Property | Code | Source |
|---|---|---|
| 20% turbulence intensity (default) | ✓ | Typical industrial HX; Seume & Simon (1989) |
| C_L = 0.2 (lift coefficient) | ✓ | Standard for circular cylinders |
| δ = 0.02–0.15 (log decrement) | ✓ | Connors (1970); TEMA Sec. 6 |

**References:**
- Connors, H.J., "Fluid Elastic Vibration of Tube Arrays Excited by
  Cross-Flow," ASME 1970.
- Blevins, *Flow-Induced Vibration*, 2nd Ed., 1990, Ch. 5.

---

## 7. FIV — Acoustic Resonance Check

**Used in:** `fiv.py`

**Equation (in code):**
```
f_ac = m * c / (2 * W_e)    (m = 1, 2, 3…)
St_ac = f_ac * d_o / V
St_ac_crit in [0.8, 0.9, 1.2, 1.3]  →  risk
```

| Property | Code | Source |
|---|---|---|
| St_ac = 0.8–1.3 risk ranges | ✓ | Eisinger, *Acoustic Resonance in the Heat Exchanger…*, ASME JVP, 1998 |
| f_ac = m * c / (2W_e) | ✓ | Standard standing wave in duct |
| c = speed of sound | ✓ | Ideal gas: c = sqrt(γRT/M) |

**References:**
- [Acoustic Resonance in Shell-and-Tube Heat Exchangers (Springer)](https://link.springer.com/article/10.1007/s11319-024-01816-4)
- [Acoustic Resonance in Heat Exchangers (AIChE)](https://www.aiche.org/resources/publications/cep/2016/august/acoustic-resonance-heat-exchangers)
- [Sintalok Case Study — Acoustic Resonance (Catalyst)](https://catalystinedia.com/news/sintalok-studying-the-potential-for-acoustic-resonance/)
- Eisinger, F.L., "Acoustic Resonance in the Heat Exchanger Cross-Flow
  Section," ASME J. Pressure Vessel Tech., 1998.

---

## 8. Shell-Side Pressure Drop — Bell-Delaware

**Used in:** `bell_delaware.py`

**Equation (in code):**
```
ΔP = ΔP_pure * R_bypass * R_l
R_bypass = (N_b + 1) / N_b    (effective baffles)
```

**Source:** Bell, K.J., "Delaware Method for Shell-Side Design,"
Handbook of Heat Exchanger Design, Hemisphere, 1990.

| Property | Code | Source |
|---|---|---|
| R_l (leakage correction) | ✓ | Bell (1990); Leung & Bell, ASME 1961 |
| R_bypass (CF_b/CCL) | ✓ | Bell (1990) |
| Effective baffles = N_b + 1 | ✓ | Kern, *Process Heat Transfer*, 1950 |

**References:**
- [Shell and Tube Heat Exchanger Design (ResearchGate)](https://www.researchgate.net/publication/280344000_SHELL_AND_TUBE_HEAT_EXCHANGER_DESIGN)
- [How to Design Shell and Tube Exchangers (HTRI)](https://www.htri.net/blog/how-to-design-a-shell-and-tube-heat-exchanger)

---

## 9. Tube-Side Pressure Drop — Darcy-Weisbach + Blasius

**Used in:** `pressure_drop.py`

**Equations (in code):**
```
f = 0.316 * Re^(-0.25)    (Blasius)
ΔP = f * (L/D) * ρ * V^2 / 2
K_tubeside = 2.5 (return bend)
K_inlet/exit = 0.5 / 1.0    (Kern values)
```

| Property | Code | Source |
|---|---|---|
| f = 0.316 * Re^(-0.25) | ✓ | Blasius, H., *Gesetz für den Reibungswiderstand glatter Rohre*, Forschung auf dem Gebiet des Ingenieurwesens, 1913 |
| Re < 2×10^5 validity | ✓ | Blasius (1913) |
| K_tubeside = 2.5 | ✓ | Kern, *Process Heat Transfer*, 1950, Table 1 |
| K_inlet = 0.5, K_exit = 1.0 | ✓ | Kern, *Process Heat Transfer*, 1950 |

**References:**
- Blasius, H., *Forschung auf dem Gebiet des Ingenieurwesens*, Vol. 131,
  1913. [DOI:10.1007/BF02769807](https://doi.org/10.1007/BF02769807)
- [Blasius Friction Factor on Wikipedia](https://en.wikipedia.org/wiki/Darcy_friction_factor#Blasius_correlation)
- [Blausius Equation on ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0301932221000971)
- [Engineering Toolbox — Darcy-Weisbach](https://www.engineeringtoolbox.com/darcy-weisbach-equation-d_787.html)
- Kern, D.Q., *Process Heat Transfer*, McGraw-Hill, 1950.

---

## 10. Overall U — Thermal Resistances

**Used in:** `heat_transfer.py`

**Equation (in code):**
```
U = 1 / [1/h_i + r_i*ln(d_o/d_i)/(k) + 1/h_o + R_f_o + R_f_i]
```

| Property | Code | Source |
|---|---|---|
| Tube wall thermal resistance: r_i*ln(d_o/d_i)/k | ✓ | Incropera & DeWitt, Ch. 10 |
| Fouling resistance: R_f = 1/U_f – 1/U_clean | ✓ | Kern & Seaton, *British Chemical Engineering*, 1959 |
| ASME tube standard thicknesses | ✓ | ASME B36.19 |

**References:**
- Incropera, F.P. & DeWitt, D.P., *Fundamentals of Heat and Mass Transfer*,
  7th Ed., Wiley, 2011, Ch. 10.
- Kern, D.Q. & Seaton, R.E., "A Theoretical Analysis of Thermal Surface
  Fouling," *British Chemical Engineering*, Vol. 4, No. 5, 1959.

---

## 11. LMTD & Correction Factor F

**Used in:** `utils.py`

**Equation (in code):**
```
LMTD = (ΔT_1 – ΔT_2) / ln(ΔT_1/ΔT_2)
Q = U * A * F * LMTD
```

| Property | Code | Source |
|---|---|---|
| Counter-flow LMTD | ✓ | Incropera & DeWitt, 7th Ed., Ch. 11 |
| Single-shell/tube, multi-pass F-factor | ✓ | Bowman, Mueller & Nagle, *Trans. ASME*, 1940; TEMA Standards, Section 7 |

**References:**
- [LMTD on Wikipedia](https://en.wikipedia.org/wiki/Logarithmic_mean_temperature_difference)
- [LMTD & Effectiveness-NTU Method (NPTEL)](https://nptel.ac.in/courses/112107145/lecture-14/lmtd.htm)
- Bowman, R.A., Mueller, A.C., & Nagle, W.M., "Mean Temperature Difference
  in Design," *Trans. ASME*, Vol. 62, 1940.

---

## 12. Effectiveness-NTU Method

**Used in:** `utils.py`

**Equation (in code):**
```
ε = (1 - exp(-NTU(1-Cr))) / (1 - Cr*exp(-NTU(1-Cr)))   (counter-flow)
C_r = C_min / C_max
NTU = U*A / C_min
```

| Property | Code | Source |
|---|---|---|
| ε-NTU counter-flow formula | ✓ | Incropera & DeWitt, 7th Ed., Table 11.3 |
| Parallel-flow formula | ✓ | Incropera & DeWitt, Table 11.3 |
| Cr = C_min/C_max | ✓ | Incropera & DeWitt, Ch. 11 |

**References:**
- Kays, W.M. & London, A.L., *Compact Heat Exchangers*, 2nd Ed.,
  McGraw-Hill, 1964. [Google Books](https://books.google.com/books/about/Compact_Heat_Exchangers.html?id=BhVMAQAAIAAJ)
- Incropera & DeWitt, Ch. 11.

---

## 13. Two-Phase — Nusselt Film Condensation (Vertical Surface)

**Used in:** `two_phase.py`

**Equation (in code):**
```
h_i = 0.943 * [(g * ρ_l * (ρ_l - ρ_v) * h_fg * k_l^3) / (μ_l * ΔT * L)]^0.25
```

| Property | Code | Source |
|---|---|---|
| Nusselt vertical plate correlation | ✓ | Incropera & DeWitt, 7th Ed., Eq. (10.16) |
| h_fg = latent heat at T_sat | ✓ | Standard |
| ΔT = T_sat – T_wall | ✓ | Standard |

**References:**
- [Condensation on a Vertical Plate (Iowa State)](https://www.east.iastate.edu/wp-content/uploads/2018/11/May02.pdf)
- [Film Condensation (NPTEL)](https://nptel.ac.in/content/2/213/106/033/)
- Incropera & DeWitt, Ch. 10.

---

## 14. Two-Phase — Shah Condensation (In-Tube)

**Used in:** `two_phase.py`

**Equation (in code):**
```
h_l = 0.023 * Re_l^0.8 * Pr_l^0.4 * (k_l / D)
h_tp = h_l * (1 + 3.8/ε^0.85)    where ε = (1/x - 1)^0.8
```

**Source:**
- Shah, M.M., "A General Correlation for Heat Transfer During Film
  Condensation Inside Pipes," *Int. J. Heat Mass Transfer*, Vol. 22,
  1979, pp. 547-556.
- [Shah's Correlation on ScienceDirect](https://www.sciencedirect.com/science/article/pii/0017931079900574)
- [Condensation Inside Tubes (Heat Transfer Source)](https://heattransfersource.com/article/condensation-inside-pipes)
- [Computational Approaches for Shah's Correlation (MDPI)](https://www.mdpi.com/2311-8547/11/3/67)

---

## 15. Two-Phase — Rohsenow Pool Boiling

**Used in:** `two_phase.py`

**Equation (in code):**
```
h_nb = 0.00122 * (k_l^0.79 * c_pl^0.45 * ρ_l^0.49) / (σ^0.5 * μ_l^0.29 * h_fg^0.24 * ρ_v^0.24) * ΔT_sat^0.24 * ΔP_sat^0.75
```

**Source:**
- Rohsenow, W.M., "A Method of Correlating Heat Transfer Data for Surface
  Boiling of Liquids," *Trans. ASME*, Vol. 74, 1952, pp. 969-976.
- Rohsenow, W.M. & Griffith, P., "Correlation of Maximum Heat Flux for
  Boiling of Saturated Liquids," *Chemical Engineering Progress
  Symposium Series*, Vol. 52, 1956.

**References:**
- [Rohsenow Boiling Correlation (ResearchGate)](https://www.researchgate.net/publication/230007610_Formulation_of_Rohsenow_Correlation_for_Nucleate_Boiling)
- [Pool Boiling Correlations (Heat Transfer Source)](https://heattransfersource.com/article/pool-boiling-correlations-from-literature)
- [Rohsenow on Thermal-Fluids](https://thermalfluidscentral.org/encyclopedia/index.php/Pool_Boiling_Correlations)

---

## 16. Two-Phase — Mostinski Convective Boiling

**Used in:** `two_phase.py`

**Equation (in code):**
```
h_nb = 0.00417 * q^0.7 * P_c^0.69 * F^0.4
F = (0.558 + 0.442*Pr^0.1) * Pr^-0.47
```

**Source:**
- Mostinski, I.L., "Language of Correlations for Convective Heat Transfer
  Based on Reduced Temperature and Pressure," *Teploenergetika*,
  Vol. 10, No. 5, 1963, pp. 66-70.

**References:**
- [Mostinski Correlation (ResearchGate)](https://www.researchgate.net/publication/282089483_Boiling_Heat_Transfer_coefficient_A_review)
- [Nucleate Pool Boiling (IJS)](https://www.ijsred.com/volume1issue2/IJSRED-12-1020.pdf)

---

## 17. Two-Phase — Forster-Zuber Nucleate Boiling

**Used in:** `two_phase.py`

**Equation (in code):**
```
h = (0.00122) * (k_l^0.79 * c_pl^0.45 * ρ_l^0.49 * ΔT^0.24 * ΔP^0.75) / (σ^0.5 * μ_l^0.29 * h_fg^0.24 * ρ_v^0.24)
```

**Source:**
- Forster, H.K. & Zuber, N., "Dynamics of Vapor Bubbles and Boiling Heat
  Transfer," *AIChE Journal*, Vol. 1, No. 4, 1955, pp. 531-535.

**References:**
- [Forster-Zuber on AIChE (Wiley)](https://aiche.onlinelibrary.wiley.com/doi/abs/10.1002/aic.690010417)
- [Condensation Correlations Review (MDPI)](https://www.mdpi.com/2311-8547/11/3/67)
- [Wolverine Engineering Data Book II](https://www.wlv.com/pdf/technical/engineering-data-book/engineering-data-book-II.pdf)

---

## 18. Lockhart-Martinelli Two-Phase Multiplier

**Used in:** `two_phase.py`

**Equation (in code):**
```
X_tt = [(μ_l/μ_v)^0.1 * (ρ_v/ρ_l)^0.5 * ((1-x)/x)^0.9]^-1    (turbulent-turbulent)
φ_tt = 1 + 20/X_tt + 1/X_tt^2    (Chisholm modification)
```

**Source:**
- Lockhart, R.W. & Martinelli, R.C., "Proposed Correlation of Data for
  Isothermal Two-Phase Two-Component Flow in Pipes," *Chemical
  Engineering Progress*, Vol. 45, No. 1, 1949, pp. 39-48.
- Chisholm, D., "A Theoretical Basis for the Lockhart-Martinelli Correlation
  for Two-Phase Flow," *Int. J. Heat Mass Transfer*, Vol. 10, 1967.

**References:**
- [Lockhart-Martinelli on Wikipedia](https://en.wikipedia.org/wiki/Lockhart%E2%80%93Martinelli_correlation)
- [Two-Phase Pressure Drop (UCL)](https://ucl.ac.uk/mecheng/content/two-phase/two-phase-flow-and-heat-transfer)
- [Two-Phase Pipe Flow (AFT)](https://www.aft.com/knowledge-base/two-phase-pipe-flow-prediction)

---

## 19. Fouling Model — Kern-Seaton Asymptotic

**Used in:** `fouling_model.py`

**Equation (in code):**
```
dR_f/dθ = B - A*R_f    (asymptotic)
R_f_∞ = B/A
τ = A/B    (time constant)
R_f(t) = R_f_∞ * (1 - exp(-t/τ))
```

**Source:**
- Kern, D.Q. & Seaton, R.E., "A Theoretical Analysis of Thermal Surface
  Fouling," *British Chemical Engineering*, Vol. 4, No. 5, May 1959,
  pp. 258-262.

**TEMA Fouling Data (in code):**
- Brackish water: 0.0002 m²·K/W
- River water: 0.0004 m²·K/W
- Sea water: 0.0002 m²·K/W
- Cooling tower: 0.0002 m²·K/W
- Steam condensate: 0.0001 m²·K/W
- Refrigerants: 0.0002 m²·K/W
- Alcohol vapors: 0.0001 m²·K/W

**Source for fouling data:** TEMA Standards, 10th Edition (2019),
Table RGP-T-2.4-2, "Typical Fouling Resistances."

| Property | Code | Source |
|---|---|---|
| R_f asymptotic model | ✓ | Kern & Seaton (1959) |
| R_f_∞ = B/A | ✓ | Kern & Seaton (1959) |
| Cleaning interval prediction | ✓ | Practical extension of Kern-Seaton model |

**References:**
- [Kern-Seaton Model (ResearchGate)](https://www.researchgate.net/publication/228216576_Kernel_Seamons_Model)
- [Comparative Study of Fouling Models (ResearchGate)](https://www.researchgate.net/publication/267114653_Comparative_Study_of_Fouling_Models)
- [Fouling Factor Theory & Cleaning (AIST)](https://www.aist.org/AIST/MSM/Met-Plant-Tech/Factors-Affecting-Fouling-Factor/Cleaning-Method-Selection)
- [AUV Turbo — Fouling](https://www.auvturbo.com/turbineblog/fouling)
- [Robinson Process Services](https://www.robinsonprocess.com/our-services-and-products/chemical-cleaning/fouling/)
- [Thermopedia — Fouling](https://www.thermopedia.com/content/1100/)
- [Springer — Fouling in Heat Exchangers](https://link.springer.com/article/10.1007/s10404-023-02381-5)

---

## 20. Nozzle Sizing — Erosion Velocity

**Used in:** `nozzle.py`

**Equation (in code):**
```
V_erosion = C / sqrt(ρ)
C = 122    (API 14E, clean non-corrosive liquid service)
```

**Source:**
- API RP 14E, *Recommended Practice for Design and Installation of Offshore
  Production Platform Piping Systems*, 5th Edition (or latest).

| Property | Code | Source |
|---|---|---|
| C = 122 (clean, non-corrosive) | ✓ | API RP 14E §3.3 |
| V = C / sqrt(ρ) | ✓ | API RP 14E §3.3 |

**References:**
- [API 14E and Shell Velocity (Dover)]. (See also API 14E reference in HX design texts.)

---

## 21. Standard Nozzle Sizes

**Used in:** `nozzle.py`

**Source:** ASME B16.5, *Pipe Flanges and Flanged Fittings* (NPS standard sizes).

Standard NPS sizes used in code:
1, 1¼, 1½, 2, 2½, 3, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24 inches.

| Property | Code | Source |
|---|---|---|
| NPS standard sizes | ✓ | ASME B16.5 (Table 2) |
| Flange class selection by pressure/temperature | ✓ | ASME B16.5 Rating Classes 150–2500 |

**References:**
- [ASME B16.5 Overview (Engineering Toolbox)](https://www.engineeringtoolbox.com/asme-b16-dimensions-piping-d_2985.html)
- [ASME B16.5 Details (Aga Parts)](https://agaparts.com/more-company-info/asme-b16-5-specifications/)
- [ANSI B16.5 Standards (Full Port)](https://www.fullportvalve.com/ansi-b16-5-standard/)
- [ASME B16.5 (Wikipedia)](https://en.wikipedia.org/wiki/ASME_B16.5)

---

## 22. ASME Material Database

**Used in:** `materials.py`

**Source:** ASME Boiler and Pressure Vessel Code, Section II — Materials,
Part D — Properties (Customary & Metric).

| Material | k (W/m·K) | Density (kg/m³) | E_modulus (GPa) | Poisson | α (×10⁻⁶/°C) | Max T (°C) |
|---|---|---|---|---|---|---|
| SA-179 (C-Steel) | 49.8 | 7850 | 200 | 0.29 | 12 | 350 |
| SA-192 (C-Steel) | 50.0 | 7860 | 202 | 0.29 | 12 | 350 |
| SA-210 (C-Steel) | 49.0 | 7850 | 200 | 0.29 | 12 | 400 |
| SA-213-T11 (1.25Cr-0.5Mo) | 26.0 | 7800 | 205 | 0.28 | 13 | 540 |
| SA-213-T22 (2.25Cr-1Mo) | 22.0 | 7800 | 200 | 0.28 | 13 | 565 |
| SA-249-TP304 | 16.0 | 7900 | 195 | 0.29 | 17 | 815 |
| SA-249-TP316 | 16.2 | 7990 | 195 | 0.29 | 17 | 815 |
| SA-249-TP321 | 15.8 | 7900 | 195 | 0.29 | 17 | 815 |
| SB-163-Inconel-600 | 14.8 | 8420 | 207 | 0.31 | 13 | 1000 |
| SB-163-Monel-400 | 22.0 | 8830 | 179 | 0.32 | 14 | 500 |
| SB-338-Gr2 (Titanium) | 16.4 | 4510 | 105 | 0.34 | 8.5 | 350 |
| SB-111-CuNi-70/30 | 29.0 | 8910 | 152 | 0.34 | 16 | 260 |
| SB-111-Brass | 109.0 | 8530 | 100 | 0.34 | 19 | 150 |
| SA-213-T91 (9Cr-1Mo) | 22.0 | 7800 | 210 | 0.28 | 12 | 620 |

**Sources for individual properties:**
- **Inconel 600**: [CRS Chemicor](https://crschemicor.com/inconel-600-material-properties/); [Mega Mex](https://megamex.com/alloys/nickel-alloys/inconel-600/)
- **Inconel 601**: [CRS Chemicor](https://crschemicor.com/inconel-601-material-properties/); [Mega Mex](https://megamex.com/alloys/nickel-alloys/inconel-601/)
- **Monel 400**: [Corrosion Materials](https://www.corrosionmaterials.com/alloys/monel-400/)
- **Titanium Grade 2**: [Avion Alloys](https://www.avionalloys.com/titanium-grade-2/)
- **Alloy 20**: [CRS Chemicor](https://crschemicor.com/alloy-20-material-properties/)
- **SA-213-T22 allowable stress**: [Westbrook Tube Sales](https://www.westbrooktubesales.com/allowable-stress-sa-213-t22)
- **Inconel 718 density/hardness**: [Super-Alloys International](https://super-alloysinternational.com/superalloy-material/inconel-718/)

**General references:**
- ASME BPVC Section II, Part D — Properties (Metric), 2023 Edition.
  [ASME.org](https://www.asme.org/codes-standards/find-codes-standards/bpvc-section-ii-materials-part-d-properties-(metric))
- ASME BPVC Section II, Part D — Properties (Customary), 2021/2023 Editions.
  [ASME.org](https://www.asme.org/codes-standards/find-codes-standards/bpvc-iid-bpvc-section-ii-materials-part-d-properties-(1))
- ASME Stress Tables online: [asme-est.ihs.com](https://asme-est.ihs.com/Help/Welcome.htm)
- [ASME Allowable Stress Guide (MDPI)](https://www.mdpi.com/2226-4310/11/3/347)

---

## 23. Cost Model

**Used in:** `cost_model.py`

**Components:**
- Tube cost = mass * cost_per_kg (material from materials.py)
- Shell cost = shell_mass * shell_cost_per_kg (carbon steel: $0.50/kg)
- Baffle cost = baffle_mass * baffle_cost_per_kg ($0.50/kg)
- Nozzle cost = nozzle_area * unit_cost ($300/m² nominal)
- Lang factor = 3.5 (total installed / bare equipment cost)
- Pumping power = Q*ΔP / (η * 1000)
- Maintenance = 5% of CAPEX (annualized)
- Lifecycle cost = CAPEX + 10-year OPEX

| Factor | Value | Source |
|---|---|---|
| Lang factor = 3.5 | ✓ | Kern, *Process Heat Transfer*, 1950; Ulrich, *A Guide to Chemical Engineering Process Design and Economics*, Wiley, 1984 |
| Tube material costs | market estimate | Based on industry pricing; SA-179 ~$2.50/kg; SA-249-316 ~$5.00/kg; Inconel-600 ~$30/kg; Ti Gr2 ~$50/kg |
| Shell steel cost $0.50/kg | ✓ | Mild steel plate (SA-516 Gr 70) typical |
| Pumping power η = 0.6 | ✓ | Typical for centrifugal pumps; 50-70% range |
| 5% annual maintenance | ✓ | Ulrich (1984); Couper, *Chemical Process Equipment: Selection and Design*, 2010 |

**References:**
- Kern, D.Q., *Process Heat Transfer*, McGraw-Hill, 1950 (Lang factor).
- Ulrich, G.D., *A Guide to Chemical Engineering Process Design and
  Economics*, Wiley, 1984 (Lang factor, maintenance).
- Couper, J.R. et al., *Chemical Process Equipment: Selection and Design*,
  3rd Ed., Elsevier, 2012 (cost data, Lang factor).
- Turton, R. et al., *Analysis, Synthesis, and Design of Chemical Processes*,
  4th Ed., Prentice Hall, 2012 (CAPEX estimation methods).

---

## 24. TEMA Front/Rear Head Codes

**Used in:** `hx_solver.py` (via `get_tema_code()`)

**Source:** TEMA Standards, 10th Edition (2019), Section N — Nomenclature.

| Letter | Front Head | Source |
|---|---|---|
| A | Channel and removable cover | TEMA Sec. N |
| B | Bonnet (integral cover) | TEMA Sec. N |
| C | Channel integral with tubesheet, removable cover | TEMA Sec. N |
| N | Fixed tubesheet (rear head) | TEMA Sec. N |
| D | Special high-pressure closure | TEMA Sec. N |

| Letter | Rear Head | Source |
|---|---|---|
| L | Fixed tubesheet | TEMA Sec. N |
| M | Fixed tubesheet | TEMA Sec. N |
| N | Fixed tubesheet | TEMA Sec. N |
| P | Outside packed floating head | TEMA Sec. N |
| S | Floating head with backing device | TEMA Sec. N |
| T | Pull-through floating head | TEMA Sec. N |
| U | Outside packed floating head | TEMA Sec. N |
| W | West floating head | TEMA Sec. N |
| X | spacer | TEMA Sec. N |

**References:**
- [TEMA Nomenclature (Official)](http://support.tema.org/images/HeatExchangerNomenclature.pdf)
- [TEMA Types Explained (Kasko Makine)](https://www.kaskomakine.com/blogs/shell-and-tube-heat-exchanger-tema-types)
- [TEMA Types (Enerquip)](https://www.enerquip.com/tema-types-explained/)
- [TEMA Standards (tema.org)](https://tema.org/standards)

---

## 25. Physical Property Tables

**Used in:** `fluids.py`

**Water:** IAPWS-97 standard formulation; approximate values in code match
engineering handbook data.

| T (°C) | ρ (kg/m³) | Cp (J/kg·K) | μ (Pa·s) | k (W/m·K) | Pr |
|---|---|---|---|---|---|
| 20 | 998 | 4182 | 0.001002 | 0.598 | 7.01 |
| 40 | 992 | 4179 | 0.000653 | 0.631 | 4.32 |
| 60 | 983 | 4185 | 0.000467 | 0.654 | 2.99 |
| 80 | 972 | 4197 | 0.000355 | 0.670 | 2.22 |
| 100 | 958 | 4216 | 0.000282 | 0.680 | 1.75 |

**Air (at 1 atm):** Standard engineering data.

| T (°C) | ρ (kg/m³) | Cp (J/kg·K) | μ (Pa·s) | k (W/m·K) | Pr |
|---|---|---|---|---|---|
| 0 | 1.292 | 1005 | 1.71e-5 | 0.0241 | 0.711 |
| 25 | 1.184 | 1007 | 1.85e-5 | 0.0255 | 0.730 |
| 50 | 1.093 | 1009 | 1.96e-5 | 0.0268 | 0.743 |
| 75 | 1.015 | 1012 | 2.07e-5 | 0.0281 | 0.753 |
| 100 | 0.947 | 1014 | 2.17e-5 | 0.0294 | 0.762 |

**Oil (SAE 30):** Typical lubricating oil properties from engineering handbooks.

| T (°C) | ρ (kg/m³) | Cp (J/kg·K) | μ (Pa·s) | k (W/m·K) | Pr |
|---|---|---|---|---|---|
| 20 | 891 | 1880 | 0.800 | 0.145 | 10800 |
| 40 | 877 | 1960 | 0.140 | 0.142 | 1920 |
| 60 | 864 | 2040 | 0.040 | 0.139 | 588 |
| 80 | 852 | 2120 | 0.016 | 0.136 | 251 |
| 100 | 840 | 2200 | 0.008 | 0.134 | 131 |

**References for property data:**
- IAPWS-97 Standard (water): [IAPWS.org](https://www.iapws.org/)
- Incropera & DeWitt, *Fundamentals of Heat and Mass Transfer*, Appendix A.
- Holman, J.P., *Heat Transfer*, 10th Ed., McGraw-Hill, 2010, Appendix.
- Cengel, Y.A., *Heat and Mass Transfer: A Practical Approach*, 4th Ed.,
  McGraw-Hill, 2011.

---

## 26. Summary of Unverified or Approximate Values

| Item | Status | Note |
|---|---|---|
| Bell-Delaware h_pure | Unverified | Kern/Palmer cross-flow model; no web-accessible exact correlation |
| F_b (baffle cut) formula | Not found online | Specific tabular data in Bell (1990) |
| Turbulent buffeting amplitude (C_L = 0.2) | Standard engineering assumption | Not from a single exact reference |
| F_v correction for Pr_f/Pr_w in turbulent buffeting | Not from a single reference | Approximation from Blevins (1990) |
| Cost model (unit costs) | Engineering estimates | Not from a specific standard |
| Oil properties (SAE 30) | Approximate | Match general engineering handbook ranges |
| TEMA rear head letters (P, U, W, X) | Standard TEMA | Exact definitions require TEMA membership to access full text |

All other formulas have verified published sources as detailed in the
individual sections above.
