# Module 3 — Conduction: Numerical Methods (FDM)
**Dates:** 11 Aug, 13 Aug 2025  
**Sources:** `htoa2511aug.pdf` (12 pages), `htoa2513aug.pdf` (11 pages)

---

## Overview

When geometries are complex, boundary conditions are non-standard, or analytical solutions don't exist, we use the **Finite Difference Method (FDM)**. The domain is discretised into a grid of nodes; the PDE is replaced by algebraic equations at each node. This module covers interior, edge, and corner nodes, and the Biot number in the discrete context.

---

## 1. Spatial Discretisation

### Grid Setup

The 2D domain is divided into a uniform grid with spacing $\Delta x$ (in $x$) and $\Delta y$ (in $y$). Each node is identified by indices $(m, n)$:

- $m$ = index in $x$-direction
- $n$ = index in $y$-direction

**Global numbering** (for matrix assembly):

$$\ell_{mn} = (n-1)(N_x + 1) + m$$

where $N_x$ = number of interior nodes in $x$. This maps the 2D grid to a 1D vector of unknowns.

---

## 2. Finite Difference Approximations

### Second Derivative (Central Difference)

$$\left.\frac{\partial^2 T}{\partial x^2}\right|_{m,n} = \frac{T_{m+\frac{1}{2},n} - T_{m-\frac{1}{2},n}}{(\Delta x)^2} = \frac{T_{m+1,n} - 2T_{m,n} + T_{m-1,n}}{(\Delta x)^2}$$

Similarly in $y$:

$$\left.\frac{\partial^2 T}{\partial y^2}\right|_{m,n} = \frac{T_{m,n+1} - 2T_{m,n} + T_{m,n-1}}{(\Delta y)^2}$$

---

## 3. Node Equations

### 3.1 Interior Node (Laplace Equation, $\Delta x = \Delta y$)

For a 2D interior node with no heat generation:

$$T_{m+1,n} + T_{m-1,n} + T_{m,n+1} + T_{m,n-1} - 4T_{m,n} = 0$$

Each interior node temperature = average of its four neighbours.

### 3.2 Edge Node with Convection

For a node on the **right edge** ($m = $ max), exposed to ambient temperature $T_\infty$ with coefficient $h$:

**Energy balance on the half-cell:**

$$T_{m,n}(Bi + 2) - (Bi)\,T_\infty - \frac{1}{2}\left[2T_{m-1,n} + T_{m,n+1} + T_{m,n-1}\right] = 0$$

where the **mesh Biot number** is:

$$\boxed{Bi = \frac{h\,\Delta x}{k}}$$

This is also the form shown in the notes for the global node 12 example:

$$T_{12}(Bi + 2) - (Bi)\,T_\infty - \frac{1}{2}\left[2T_{11} + T_{16} + T_8\right] = 0$$

### 3.3 Corner Node with Convection

For a **corner node** (e.g., bottom-right, convection on two faces):

$$T_{m,n}(Bi + 1) - (Bi)\,T_\infty - \frac{1}{2}\left[T_{m-1,n} + T_{m,n+1}\right] = 0$$

The coefficient differs because only two (not four) neighbour nodes contribute at half-weight.

---

## 4. The Biot Number — Physical Meaning

$$Bi = \frac{h\,\Delta x}{k} = \frac{\Delta x/(kA)}{1/(hA)} = \frac{\text{Resistance to conduction in solid}}{\text{Resistance to convection in liquid}}$$

> **Lecture note:** "Bi provides a measure of the temperature drop in the solid to the difference in temp between solid surface and fluid."

- **Small Bi ($\ll 1$):** Convection resistance dominates → solid is nearly isothermal → lumped capacitance valid
- **Large Bi ($\gg 1$):** Conduction resistance dominates → large temperature gradients inside solid

---

## 5. Lumped Capacitance (Transient) — Also in This Block

The 13 Aug notes also introduce **transient conduction** with lumped capacitance — when $Bi \ll 1$:

**Setup:** A solid body (e.g., a sphere or egg) initially at $T_i$, suddenly immersed in a fluid at $T_\infty$.

$$\frac{T - T_\infty}{T_i - T_\infty} = \exp\!\left[-\frac{hA}{\rho C_v V}\,t\right]$$

Where:
- $A$ = surface area of the body [m²]
- $V$ = volume of the body [m³]
- $\rho C_v V$ = thermal mass of the body [J/K]
- $\frac{hA}{\rho C_v V}$ = inverse of the time constant $\tau$

**Time constant:**

$$\tau = \frac{\rho C_v V}{hA}$$

**Validity criterion:** $Bi = \frac{hL_c}{k} < 0.1$ where $L_c = V/A$ (characteristic length).

---

## 6. Matrix Form of the FDM System

For a grid with $N$ unknown nodes, the FDM equations form a linear system:

$$[A]\{T\} = \{b\}$$

- $[A]$ is a sparse, banded matrix (coefficients from the stencil)
- $\{T\}$ is the vector of unknown nodal temperatures
- $\{b\}$ contains known boundary values and source terms

**For interior nodes ($\Delta x = \Delta y$):** The matrix $[A]$ has $-4$ on the diagonal and $+1$ at the positions of the four neighbours.

**For edge nodes with convection:** The diagonal entry becomes $-(Bi + 2)$ and the right-hand side gets a $-(Bi)T_\infty$ contribution.

---

## 7. Solution Strategy

For steady-state 2D:

1. Identify all node types: interior, edge (which faces?), corner
2. Write the FDM equation for each node type
3. Assemble into matrix $[A]\{T\} = \{b\}$
4. Solve by Gaussian elimination or iterative methods (Gauss-Seidel)

For transient problems (not covered deeply here — see lumped capacitance above), the matrix becomes time-dependent.

---

## 8. Example Node Numbering (4×4 Grid)

```
(1,4)  (2,4)  (3,4)  (4,4)
(1,3)  (2,3)  (3,3)  (4,3)  ← Convection on right face
(1,2)  (2,2)  (3,2)  (4,2)
(1,1)  (2,1)  (3,1)  (4,1)
  ↑
Convection on bottom face
```

- Node $(4,3)$ = edge node (right face, convection)
- Node $(4,1)$ = corner node (right face + bottom face, convection)
- Nodes $(1,1)$–$(3,4)$ = interior nodes (if interior boundaries are specified)

---

## Textbook References

- **Incropera & DeWitt:** Chapter 4 (Numerical Methods in Conduction)
- **Holman & Bhattacharya:** Chapter 3

---

## Connected Modules

- [Module 2](03_conduction_2D.md) — The same Laplace equation, now solved numerically
- [Module 5](06_convection_internal.md) — Biot number appears again in context of pipe flow entrance
