# Experiment 12 — Curved Background: Spatially Flat FLRW

**Author:** Pablo Salvador Cardenas  
**Status:** Mathematical consistency experiment on a prescribed background; not a dynamical gravity model.

## 1. Geometry

Use comoving coordinates and signature (-+++):
\[
ds^2=-dt^2+a(t)^2(dx^2+dy^2+dz^2).
\]
The metric, inverse, determinant, and invariant volume factor are
\[
g_{\mu\nu}=\mathrm{diag}(-1,a^2,a^2,a^2),\quad
g^{\mu\nu}=\mathrm{diag}(-1,a^{-2},a^{-2},a^{-2}),
\]
\[
g=-a^6,\qquad \sqrt{-g}=a^3,\qquad H=\dot a/a.
\]
For any homogeneous scalar X(t),
\[
\Box_gX=\frac{1}{\sqrt{-g}}\partial_t
(\sqrt{-g}g^{00}\dot X)
=-(\ddot X+3H\dot X).
\]

## 2. Action and equations

The fixed-background action is
\[
S=\int d^4x\sqrt{-g}\,\mathcal L,
\]
\[
\mathcal L=-\frac12g^{\mu\nu}\partial_\mu\phi\partial_\nu\phi
-\frac12m^2\phi^2
-\frac{Z_T}{2}g^{\mu\nu}\partial_\mu T\partial_\nu T
-\frac{\mu_T^2}{2}T^2+g_cT f(\phi),
\quad f(\phi)=\frac12\frac{\phi^2}{1+\phi^2}.
\]
The covariant Euler–Lagrange equations are
\[
\Box_g\phi-m^2\phi+g_cT f'(\phi)=0,
\quad
Z_T\Box_gT-\mu_T^2T+g_cf(\phi)=0.
\]
For homogeneous fields:
\[
\ddot\phi+3H\dot\phi+m^2\phi-g_cT f'(\phi)=0,
\]
\[
Z_T(\ddot T+3H\dot T)+\mu_T^2T-g_cf(\phi)=0.
\]
The code reuses the Experiment 9 parameter object. The coupling is named g_c here to distinguish it from the metric.

## 3. Stress-energy and conservation

Metric variation of the matter action on the prescribed geometry gives
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
The covariant tensor in comoving coordinates is diagonal:
\[
T_{\mu\nu}=\mathrm{diag}(\rho,a^2p,a^2p,a^2p).
\]
With residuals R_phi=Box_g phi-m^2 phi+g_c T f' and
R_T=Z_T Box_g T-mu_T^2 T+g_c f, the homogeneous continuity identity is
\[
\dot\rho+3H(\rho+p)=-\dot\phi R_\phi-\dot T R_T.
\]
It vanishes on shell. This is the matter-sector Noether identity on a fixed background, not evidence that the fields source the metric.

## 4. Executable protocol

- research/one_time_field/flrw_curved.py: FLRW metric/inverse/determinant, volume factor, Hubble rate, homogeneous scalar wave operator, Lagrangian, E-L residuals, on-shell accelerations, stress tensor, and continuity identity.
- research/tests/test_flrw_curved.py: geometry, determinant, positive-scale-factor validation, flat limit, homogeneous wave operator, on-shell residuals, off-shell continuity identity, isotropic stress tensor, de Sitter and power-law expansion checks.
- research/examples/flrw_curved_experiment.py: dedicated runner.

The test suite checks exact algebraic identities to floating-point tolerance. It does not fit parameters to cosmological data or infer an expansion history.

## 5. Scope and limitations

The scale factor a(t) is an input. No Friedmann equation is solved; no metric backreaction, gravitational coupling, perturbation spectrum, or observational likelihood is included. The model remains a classical two-scalar ansatz. A successful test suite establishes internal consistency of the coded equations only; it does not establish that T is physical time or that One Time Field Theory describes the universe.
