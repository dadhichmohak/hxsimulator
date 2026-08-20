# HTOA 2025 — Heat Transfer & Applied Analysis
## Complete Digital Notes Index

> **Course:** Heat Transfer & Applied Analysis (HTOA 2025)  
> **Textbooks Referenced:** Incropera & DeWitt · Holman & Bhattacharya · McCabe & Smith  
> **Period:** July – November 2025  
> **Total Lecture Files:** 37 PDFs

---

## Module Map

| # | Module | Date Range | README File | Key Topics |
|---|--------|-----------|-------------|------------|
| 0 | Foundations & Governing Equations | 31 Jul | [01_foundations.md](01_foundations.md) | Continuity, N-S, Energy equation, Constitutive relations |
| 1 | Conduction — Fundamentals | 30 Jul – 4 Aug | [02_conduction_fundamentals.md](02_conduction_fundamentals.md) | Fourier's law, Thermal resistance, Cylindrical coords, Heat sources |
| 2 | Conduction — 2D Steady State | 7 Aug | [03_conduction_2D.md](03_conduction_2D.md) | Separation of variables, Orthogonal functions, Fourier series |
| 3 | Conduction — Numerical Methods | 11–13 Aug | [04_conduction_numerical.md](04_conduction_numerical.md) | FDM, Edge/corner nodes, Biot number, Matrix formulation |
| 4 | Convection — Boundary Layers & External Flow | 14–21 Aug | [05_convection_external.md](05_convection_external.md) | Velocity/thermal BL, Re, Nu, Pr, Flat plate correlations |
| 5 | Convection — Internal Flows | 25 Aug – 10 Sep | [06_convection_internal.md](06_convection_internal.md) | Entry length, Laminar/turbulent pipe flow, Dittus-Boelter, Colburn analogy |
| 6 | Conduction — Extended Surfaces (Fins) | 8 Sep + 17 Nov | [07_fins.md](07_fins.md) | Critical insulation thickness, Fin equation, Efficiency |
| 7 | Heat Exchangers | 11 Sep – 23 Oct | [08_heat_exchangers.md](08_heat_exchangers.md) | LMTD, NTU-effectiveness, Double-pipe, Shell & tube, Fouling |
| 8 | Free (Natural) Convection & Boiling | 30 Oct – 6 Nov | [09_free_convection_boiling.md](09_free_convection_boiling.md) | Buoyancy-driven flow, Boiling regimes, Bubble dynamics |
| 9 | Condensation & Evaporation | 12–17 Nov | [10_condensation.md](10_condensation.md) | Film condensation, Nusselt theory, Radial systems |

---

## Quick Formula Reference

### Three Modes of Heat Transfer

| Mode | Equation | Variables |
|------|----------|-----------|
| **Conduction** | $q = -k\nabla T$ | $k$ = thermal conductivity [W/mK] |
| **Convection** | $q = h(T_s - T_\infty)$ | $h$ = convection coefficient [W/m²K] |
| **Radiation** | $q = \varepsilon\sigma(T_s^4 - T_{sur}^4)$ | $\varepsilon$ = emissivity, $\sigma$ = Stefan-Boltzmann constant |

### Key Dimensionless Numbers

| Number | Formula | Physical Meaning |
|--------|---------|------------------|
| Reynolds | $Re = \frac{\rho u L}{\mu}$ | Inertia / Viscous forces |
| Nusselt | $Nu = \frac{hL}{k}$ | Convective / Conductive heat transfer |
| Prandtl | $Pr = \frac{\mu C_p}{k} = \frac{\nu}{\alpha}$ | Momentum / Thermal diffusivity |
| Biot | $Bi = \frac{hL}{k}$ | Surface convection / Internal conduction |
| Stanton | $St = \frac{h}{\rho u C_p} = \frac{Nu}{Re \cdot Pr}$ | Heat transfer / Thermal capacity of flow |
| Peclet | $Pe = Re \cdot Pr$ | Advection / Diffusion |

---

## Source File → Module Mapping

| PDF File | Date | Module |
|----------|------|--------|
| `htoa2531jul.pdf` | 31 Jul | Foundations (Module 0) |
| `htoa25lec130jul.pdf` | 30 Jul | Conduction Intro (Module 1) |
| `htoa254aug.pdf` | 4 Aug | Conduction – Cylindrical (Module 1) |
| `htoa256aug.pdf` | 6 Aug | Conduction – Composite cylinders (Module 1) |
| `htoa257aug.pdf` | 7 Aug | 2D Conduction (Module 2) |
| `htoa2511aug.pdf` | 11 Aug | Numerical – Edge nodes (Module 3) |
| `htoa2513aug.pdf` | 13 Aug | Numerical – FDM derivation (Module 3) |
| `htoa2514aug.pdf` | 14 Aug | Boundary layers intro (Module 4) |
| `htoa2518aug.pdf` | 18 Aug | Flat plate laminar (Module 4) |
| `htoa2520aug.pdf` | 20 Aug | Flat plate – chip cooling (Module 4) |
| `htoa2521aug.pdf` | 21 Aug | Film temperature, property tables (Module 4) |
| `htoa2525aug.pdf` | 25 Aug | Internal flows intro (Module 5) |
| `htoa2528aug.pdf` | 28 Aug | Internal flows – entry length (Module 5) |
| `htoa251sep.pdf` | 1 Sep | Pipe flow – laminar (Module 5) |
| `htoa253sep.pdf` | 3 Sep | LMTD for pipe + HX intro (Module 5/7) |
| `htoa2504sep.pdf` | 4 Sep | Dittus-Boelter turbulent (Module 5) |
| `htoa258sep.pdf` | 8 Sep | Critical thickness of insulation (Module 6) |
| `htoa2510sep.pdf` | 10 Sep | Colburn analogy & Stanton number (Module 5) |
| `htoa2511sep.pdf` | 11 Sep | Double-pipe heat exchanger (Module 7) |
| `htoa258oct.pdf` | 8 Oct | Fouling factors (Module 7) |
| `htoa2514oct.pdf` | 14 Oct | U overall calculation (Module 7) |
| `htoa2522oct.pdf` + `htoa2522oct1.pdf` | 22 Oct | HX Analysis & Design (Module 7) |
| `htoa2523oct.pdf` + `htoa2523oct1.pdf` | 23 Oct | Effectiveness-NTU method (Module 7) |
| `htoa2530oct.pdf` | 30 Oct | Free convection + Boiling intro (Module 8) |
| `htoa2503nov.pdf` + `htoa2503nov_1.pdf` | 3 Nov | Bubble dynamics in boiling (Module 8) |
| `htoa256nov.pdf` + `htoa256nov_1.pdf` | 6 Nov | Bubble dynamics continued (Module 8) |
| `htoa2512nov.pdf` + `htoa2512nov_notes.pdf` | 12 Nov | Film condensation – radial (Module 9) |
| `htoa2517novfull.pdf` | 17 Nov | Fins – heat transfer calc (Module 6) |
| `hto25aut03nov.pdf` + `hto25aut03nov_1.pdf` | 3 Nov | Additional tutorial (Module 8) |

---

## How to Navigate These Notes

These notes were digitised from handwritten whiteboard/notebook scans (July–November 2025). Each module README contains:

- **Conceptual overview** — what the topic is about and why it matters
- **Key equations** — transcribed exactly as written in lectures, with variable definitions
- **Worked logic** — step-by-step reasoning shown in the original notes
- **Boundary conditions & special cases** — conditions written alongside equations
- **Textbook cross-references** — section numbers cited in the notes

Start with [01_foundations.md](01_foundations.md) for the governing equations, then follow module order.

---

## Complete Audit — All 37 PDFs Verified

| PDF File | Pages | Status | Content Covered |
|----------|-------|--------|----------------|
| `htoa25lec130jul.pdf` | 10 | ✅ M1 | Course overview, 3 modes, HX map |
| `htoa2531jul.pdf` | 13 | ✅ M0 | Governing eqs, Fourier, composite walls, radiation resistance |
| `htoa254aug.pdf` | 14 | ✅ M1 | Cyl. heat source, Poisson eq., wire worked example (T=231.6°C) |
| `htoa256aug.pdf` | 16 | ✅ M1 | Composite cylinders, U_i formula |
| `htoa257aug.pdf` | 18 | ✅ M2 | 2D conduction, orthogonal functions, full series solution |
| `htoa2511aug.pdf` | 12 | ✅ M3 | FDM grid, edge/corner nodes, Bi interpretation |
| `htoa2513aug.pdf` | 11 | ✅ M3 | FDM second derivatives, lumped capacitance |
| `htoa2514aug.pdf` | 14 | ✅ M4 | Velocity + thermal BL, Re, transition, local h |
| `htoa2518aug.pdf` | 15 | ✅ M4 | Flat plate Nu (lam/turb/mixed), const flux Nu, film T |
| `htoa2520aug.pdf` | 10 | ✅ M4 | Chip cooling, turbulent local h, min h at last chip |
| `htoa2521aug.pdf` | 8 | ✅ M4 | Film temperature, Table A-4 property lookup |
| `htoa2525aug.pdf` | 13 | ✅ M5 | Entry length hydro + thermal, fully developed condition |
| `hto25a25825.pdf` | 13 | ✅ M5 | **Duplicate** of htoa2525aug — same pages |
| `htoa2528aug.pdf` | 13 | ✅ M5 | Tm fully developed thermal derivation |
| `Copy_of_htoa2528aug.pdf` | 13 | ✅ M5 | **Duplicate** of htoa2528aug |
| `htoa251sep.pdf` | 14 | ✅ M5 | Laminar pipe: energy eq., const flux, const Ts, Tm decay |
| `htoa253sep.pdf` | 10 | ✅ M5/M7 | LMTD for pipe, worked numerical example |
| `htoa2504sep.pdf` | 5 | ✅ M5 | Dittus-Boelter (blackboard), validity conditions |
| `htoa258sep.pdf` | 14 | ✅ M6/M5 | Critical insulation thickness + turbulent pipe worked example |
| `htoa2510sep.pdf` | 9 | ✅ M5 | Sieder-Tate → Colburn analogy, St, j_H, mass transfer analogy |
| `htoa2511sep.pdf` | 13 | ✅ M7 | Double-pipe HX, LMTD derivation (4 assumptions) |
| `htoa258oct.pdf` | 4 | ✅ M7 | Fouling factors, R_f values |
| `htoa2514oct.pdf` | 7 | ✅ M7 | U overall, LMTD worked example (ΔTlm=88°C), A=70.96m² |
| `htoa2522oct.pdf` | 11 | ✅ M7 | HX analysis vs design; rating problem setup |
| `htoa2522oct1.pdf` | 11 | ✅ M7 | Ch=5556, Cc=5806 example; q from EB + LMTD |
| `htoa2523oct.pdf` | 14 | ✅ M7 | ε-NTU intro, q_max, ε definition |
| `htoa2523oct1.pdf` | 14 | ✅ M7 | ε from hot/cold sides, Cr, ε=f(NTU,Cr) |
| `htoa2530oct.pdf` | 14 | ✅ M8 | Free conv. BL, Boussinesq, β, Gr, Ra, boiling intro |
| `hto25aut03nov.pdf` | 3 | ✅ M8 | Boiling: hfg/σ/Δρ; Nu=f(Ja,Pr,Bo); Jakob + Bond definitions |
| `hto25aut03nov_1.pdf` | 3 | ✅ M8 | **Duplicate** of hto25aut03nov |
| `htoa2503nov.pdf` | 3 | ✅ M8 | Bubble dynamics: setup, Young-Laplace derivation |
| `htoa2503nov_1.pdf` | 3 | ✅ M8 | **Duplicate** of htoa2503nov |
| `htoa256nov.pdf` | 4 | ✅ M8 | Bubble: not in equil., collapse vs. growth, pv−pl=2σ/r |
| `htoa256nov_1.pdf` | 4 | ✅ M8 | **Duplicate** of htoa256nov |
| `htoa2512nov.pdf` | 14 | ✅ M9 | Film cond. (radial), evaporation, economy, full heat balance |
| `htoa2512nov_notes.pdf` | 14 | ✅ M9 | **Duplicate** of htoa2512nov |
| `htoa2517novfull.pdf` | 14 | ✅ M6 | Full fin derivation: energy balance, ODE, BCs, q_f formula |

**Total: 37 PDFs · ~363 pages · 10 module READMEs + master index + cheat sheet = 12 files**

**Duplicates identified (6 files):** `hto25a25825`, `Copy_of_htoa2528aug`, `hto25aut03nov_1`, `htoa2503nov_1`, `htoa256nov_1`, `htoa2512nov_notes` — all content captured from primary copies.
