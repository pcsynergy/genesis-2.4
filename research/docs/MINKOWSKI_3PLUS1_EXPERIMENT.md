# Experiment 11 — 3+1-dimensional Minkowski formulation

**Status:** Executable algebraic consistency tests.  
**Scope:** Two classical real scalar fields on a fixed 3+1-dimensional Minkowski background, metric signature (-,+,+,+), natural units c=1.

## 1. Action density

The same two-scalar model used in Experiments 9–10 is extended to three spatial dimensions:

\[
\mathcal L=-\frac12\partial_\mu\phi\partial^\mu\phi
-\frac12m^2\phi^2
-\frac{Z_T}{2}\partial_\mu T\partial^\mu T
-\frac{\mu_T^2}{2}T^2+gT f(\phi),
\qquad f(\phi)=\frac12\frac{\phi^2}{1+\phi^2}.
\]

The fields remain Lorentz scalars. The d'Alembertian is
\[
\Box=-\partial_t^2+\partial_x^2+\partial_y^2+\partial_z^2.
\]
The Euler–Lagrange residuals retain their previous form:
\[
R_\phi=\Box\phi-m^2\phi+gT f'(\phi),\qquad
R_T=Z_T\Box T-\mu_T^2T+g f(\phi).
\]

## 2. Stress-energy tensor

\[
T^{\mu\nu}=\partial^\mu\phi\partial^\nu\phi
+Z_T\partial^\mu T\partial^\nu T+\eta^{\mu\nu}\mathcal L.
\]
The implementation returns all sixteen components and checks symmetry and agreement of T^{00} with the Hamiltonian density.

## 3. Lorentz and conservation checks

The test suite checks invariance of Minkowski gradient contractions and the full Lagrangian under boosts along each coordinate axis and oblique boost directions. It checks the off-shell Noether identity
\[
\partial_\mu T^{\mu\nu}=R_\phi\partial^\nu\phi+R_T\partial^\nu T,
\]
and its on-shell zero-divergence consequence. The four-vector divergence identity is evaluated algebraically from the field-equation residuals; it is not a finite-difference simulation.

## 4. Interpretation and limits

This is a dimensional extension of the fixed-background classical scalar model. It does not introduce curved spacetime, a dynamical metric, Einstein's equations, gauge fields, quantization, measured constants, or empirical data. Lorentz invariance of the selected action is a mathematical consistency property, not evidence that the clock scalar is physical time.

A curved-background extension would replace the flat metric contractions with g_{\mu\nu}, include the invariant volume element \sqrt{-g}, and verify covariant conservation. A dynamical gravitational theory would additionally require a metric field equation derived by varying the complete action with respect to the metric.
