# Module 2 — Conduction: 2D Steady State
**Date:** 7 August 2025  
**Source:** `htoa257aug.pdf` (18 pages)

---

## Overview

When temperature varies in more than one spatial direction and generation/transient terms are absent, the governing equation is the **Laplace equation**. Analytical solution requires **separation of variables** and the theory of **orthogonal functions** (Fourier series). This lecture develops the full solution procedure for a rectangular domain.

---

## 1. Governing Equation

For 2D, steady-state conduction with no heat generation in a rectangular domain:

$$\frac{\partial^2 T}{\partial x^2} + \frac{\partial^2 T}{\partial y^2} = 0 \qquad \text{(Laplace equation)}$$

This is an elliptic PDE — the solution at every point depends on the entire boundary.

---

## 2. Dimensionless Form

Define the dimensionless temperature:

$$\Theta(x, y) \equiv \frac{T(x,y) - T_1}{T_2 - T_1}$$

where $T_1$ and $T_2$ are reference boundary temperatures. The PDE becomes:

$$\frac{\partial^2 \Theta}{\partial x^2} + \frac{\partial^2 \Theta}{\partial y^2} = 0$$

with $\Theta \in [0, 1]$.

---

## 3. Separation of Variables

Assume the solution is a product of functions of $x$ only and $y$ only:

$$\Theta(x, y) = X(x) \cdot Y(y)$$

Substituting into the PDE:

$$Y \frac{d^2X}{dx^2} + X \frac{d^2Y}{dy^2} = 0$$

Dividing by $XY$:

$$\frac{1}{X}\frac{d^2X}{dx^2} = -\frac{1}{Y}\frac{d^2Y}{dy^2} = -\lambda^2$$

Each side must equal the same constant (separation constant $-\lambda^2$), yielding two ODEs:

$$\frac{d^2X}{dx^2} + \lambda^2 X = 0 \implies X(x) = A\sin(\lambda x) + B\cos(\lambda x)$$

$$\frac{d^2Y}{dy^2} - \lambda^2 Y = 0 \implies Y(y) = C\sinh(\lambda y) + D\cosh(\lambda y)$$

---

## 4. Boundary Conditions and Eigenvalues

**Standard problem (rectangular domain $0 \le x \le L$, $0 \le y \le W$):**

- Three sides at $\Theta = 0$ (homogeneous)
- One side (top, $y = W$) at $\Theta = 1$ (non-homogeneous)

Applying BCs:
- $\Theta(0, y) = 0 \implies B = 0$, so $X(x) = A\sin(\lambda x)$
- $\Theta(L, y) = 0 \implies \sin(\lambda L) = 0 \implies \lambda_n = \frac{n\pi}{L}$, $n = 1, 2, 3, \ldots$
- $\Theta(x, 0) = 0 \implies D = 0$, so $Y(y) = C\sinh(\lambda_n y)$

General solution (superposition of all modes):

$$\Theta(x, y) = \sum_{n=1}^{\infty} C_n \sin\!\left(\frac{n\pi x}{L}\right) \sinh\!\left(\frac{n\pi y}{L}\right)$$

---

## 5. Orthogonal Functions and Fourier Coefficients

### Definition of Orthogonality

An infinite set of functions $g_1(x), g_2(x), \ldots, g_n(x)$ is **orthogonal** on the interval $a \le x \le b$ if:

$$\int_a^b g_m(x)\, g_n(x)\, dx = 0 \quad \text{when } m \neq n$$

**Examples:** $\sin\!\left(\dfrac{n\pi x}{L}\right)$, $\cos\!\left(\dfrac{n\pi x}{L}\right)$, Legendre polynomials.

### Expanding an Arbitrary Function

Any function $f(x)$ can be written as a series of orthogonal basis functions:

$$\boxed{f(x) = \sum_{n=1}^{\infty} A_n\, g_n(x)}$$

The coefficients $A_m$ are found by exploiting orthogonality — multiply both sides by $g_m(x)$ and integrate:

$$\boxed{A_m = \frac{\displaystyle\int_a^b f(x)\, g_m(x)\, dx}{\displaystyle\int_a^b g_m^2(x)\, dx}}$$

This eliminates all terms except the $n = m$ term (all cross terms are zero by orthogonality).

---

## 6. Applying the Non-Homogeneous BC

At $y = W$, $\Theta(x, W) = 1$:

$$1 = \sum_{n=1}^{\infty} C_n \sin\!\left(\frac{n\pi x}{L}\right) \sinh\!\left(\frac{n\pi W}{L}\right)$$

Using orthogonality, multiply by $\sin(m\pi x / L)$ and integrate from $0$ to $L$:

$$A_n = \frac{\displaystyle\int_0^L \sin\!\left(\frac{n\pi x}{L}\right) dx}{\displaystyle\int_0^L \sin^2\!\left(\frac{n\pi x}{L}\right) dx} = \frac{2}{\pi}\frac{(-1)^{n+1} + 1}{n}$$

So:

$$C_n = \frac{A_n}{\sinh(n\pi W/L)} = \frac{2[(-1)^{n+1}+1]}{n\pi \sinh(n\pi W/L)}$$

**Note:** $(-1)^{n+1} + 1 = 2$ for odd $n$, and $= 0$ for even $n$ — so only **odd harmonics** survive.

---

## 7. Complete Solution

$$\boxed{\Theta(x, y) = \frac{2}{\pi} \sum_{n=1}^{\infty} \frac{(-1)^{n+1}+1}{n} \sin\!\left(\frac{n\pi x}{L}\right) \frac{\sinh(n\pi y/L)}{\sinh(n\pi W/L)}}$$

Or equivalently from the lecture's final boxed form:

$$\Theta(x, y) = \frac{2}{\pi}\sum_{n=1,3,5,\ldots} \frac{1}{n} \sin\!\left(\frac{n\pi x}{L}\right) \frac{\sinh(n\pi y/L)}{\sinh(n\pi W/L)}$$

---

## 8. Key Physical Observations

- The solution is a **superposition of modes** — each mode is an eigenfunction satisfying the boundary conditions on three sides
- **Higher modes** ($n = 3, 5, \ldots$) decay more rapidly in $y$ (the $\sinh$ ratio decays faster for larger $n$)
- Far from the non-homogeneous boundary, the $n = 1$ mode dominates
- The solution converges uniformly except at corners where boundary values may be discontinuous

---

## 9. Summary of Procedure

1. Write the PDE in dimensionless form
2. Apply homogeneous BCs → identify separated solutions and eigenvalues
3. Write general solution as superposition (series)
4. Apply non-homogeneous BC → expand using orthogonality
5. Compute Fourier coefficients by integration
6. Write complete series solution

---

## Textbook References

- **Incropera & DeWitt:** Chapter 4 (Two-Dimensional Steady-State Conduction)
- **Holman & Bhattacharya:** Chapter 3

---

## Connected Modules

- [Module 1](02_conduction_fundamentals.md) — 1D basis extended here to 2D
- [Module 3](04_conduction_numerical.md) — When analytical solution is intractable, use FDM
