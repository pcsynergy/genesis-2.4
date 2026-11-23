# One Time Field Theory Research Report — Version 0.7

**Author:** Pablo Salvador Cardenas  
**Project:** GENESIS 2.4 — One Time Field Foundation  
**Research branch:** research/one-time-field-foundation  
**Date:** 23 November 2026  
**Status:** Mathematical prototype on a prescribed curved background; not an empirically validated physical theory.

## Executive summary

Version 0.7 adds **Experiment 12**, extending the Experiment 11 two-scalar model from fixed 3+1 Minkowski spacetime to a prescribed spatially-flat Friedmann–Lemaître–Robertson–Walker (FLRW) background. The implementation represents the metric and inverse, determinant and invariant volume factor, Hubble parameter, homogeneous scalar d'Alembertian, Euler–Lagrange residuals, on-shell accelerations, stress-energy tensor, and the homogeneous continuity identity.

The scale factor is prescribed. This is not a solution of the Einstein or Friedmann equations and does not include gravitational backreaction.

## 1. Geometry and field model

With signature (-+++):
\[
ds^2=-dt^2+a(t)^2(dx^2+dy^2+dz^2),\quad
g=-a^6,\quad \sqrt{-g}=a^3,\quad H=\dot a/a.
\]
For homogeneous scalar X(t):
\[
\Box_gX=-(\ddot X+3H\dot X).
\]
The action is
\[
S=\int d^4x\sqrt{-g}\left[
-\frac12(\nabla\phi)^2-\frac12m^2\phi^2
-\frac{Z_T}{2}(\nabla T)^2-\frac{\mu_T^2}{2}T^2
+g_cT f(\phi)\right],
\quad f(\phi)=\frac12\frac{\phi^2}{1+\phi^2}.
\]
Its covariant equations are
\[
\Box_g\phi-m^2\phi+g_cT f'(\phi)=0,
\quad Z_T\Box_gT-\mu_T^2T+g_cf(\phi)=0.
\]
The homogeneous equations are
\[
\ddot\phi+3H\dot\phi+m^2\phi-g_cT f'(\phi)=0,
\]
\[
Z_T(\ddot T+3H\dot T)+\mu_T^2T-g_cf(\phi)=0.
\]

## 2. Stress-energy and conservation

The metric stress tensor is
\[
T_{\mu\nu}=\partial_\mu\phi\partial_\nu\phi
+Z_T\partial_\mu T\partial_\nu T+g_{\mu\nu}\mathcal L.
\]
For homogeneous fields:
\[
\rho=\frac12\dot\phi^2+\frac{Z_T}{2}\dot T^2
+\frac12m^2\phi^2+\frac{\mu_T^2}{2}T^2-g_cTf(\phi),
\]
\[
p=\frac12\dot\phi^2+\frac{Z_T}{2}\dot T^2
-\frac12m^2\phi^2-\frac{\mu_T^2}{2}T^2+g_cTf(\phi).
\]
For residuals R_phi and R_T as defined by the left sides of the covariant equations:
\[
\dot\rho+3H(\rho+p)=-\dot\phi R_\phi-\dot T R_T.
\]
Therefore the continuity equation holds when both scalar equations hold. This is a consistency identity for matter on a prescribed geometry, not an independent observational prediction.

## 3. Implementation and tests

- research/one_time_field/flrw_curved.py — FLRW metric/inverse/determinant, volume factor, Hubble parameter, homogeneous scalar wave operator, Lagrangian density, field residuals, on-shell accelerations, energy density/pressure, covariant stress tensor, and continuity residual.
- research/tests/test_flrw_curved.py — metric inverse and determinant; scale-factor validation; homogeneous wave operator and flat limit; on-shell residuals; off-shell continuity identity; stress-tensor isotropy; de Sitter and power-law Hubble checks.
- research/examples/flrw_curved_experiment.py — dedicated runner.
- research/docs/FLRW_CURVED_EXPERIMENT.md — derivation and scientific limitations.

## 4. Interpretation

The checks validate algebraic and differential identities for the selected classical action and the implemented FLRW conventions. They do not show that the scalar T is physical time, that it is a new fundamental field, or that the model explains cosmic expansion. No observational parameters are fitted.

## 5. Limitations and next steps

The scale factor is an external input. The implementation does not vary the metric, solve Friedmann equations, include perturbations, or compare with cosmological observations. The next mathematically distinct stage would be to derive metric variation and then decide whether a consistent dynamical-gravity completion is justified. Such a step must keep gravitational assumptions and matter-sector assumptions explicit.

**Conclusion:** Experiment 12 establishes executable homogeneous-field consistency checks on a prescribed spatially-flat FLRW background. It is a curved-background extension of the mathematical prototype, not a validated cosmological theory.
