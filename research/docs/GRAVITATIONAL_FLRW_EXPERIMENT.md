# Experiment 13 — Metric Variation and Dynamical FLRW Gravity

**Author:** Pablo Salvador Cardenas  
**Status:** Classical Einstein–Hilbert plus two-scalar model; mathematical consistency experiment, not an observationally validated theory.

## 1. Full action and metric variation

Promote the metric to a dynamical variable:
\[
S[g,\phi,T]=\int d^4x\sqrt{-g}
\left[\frac{M_{\rm Pl}^2}{2}R+\mathcal L_m\right],
\]
where \(\mathcal L_m\) is the Experiment 12 matter Lagrangian and
\(M_{\rm Pl}^2=(8\pi G)^{-1}>0\). The usual boundary prescription is assumed for the Einstein–Hilbert variation.

Define
\[
T_{\mu\nu}=-\frac{2}{\sqrt{-g}}\frac{\delta(\sqrt{-g}\mathcal L_m)}
{\delta g^{\mu\nu}}.
\]
Metric variation gives
\[
M_{\rm Pl}^2G_{\mu\nu}=T_{\mu\nu}.
\]
Scalar variation gives the Experiment 12 matter equations. This is minimally coupled general relativity with the existing two-scalar matter ansatz, not a new gravity law.

## 2. Spatially-flat FLRW equations

For \(ds^2=-dt^2+a(t)^2d\vec x^2\), \(H=\dot a/a\):
\[
R=6(\dot H+2H^2),\quad G_{00}=3H^2,\quad
G_{ij}=-(2\dot H+3H^2)g_{ij}.
\]
The independent homogeneous equations are
\[
3M_{\rm Pl}^2H^2=\rho,\qquad
-2M_{\rm Pl}^2\dot H=\rho+p.
\]
Here rho and p are the coupled scalar energy density and pressure from Experiment 12.

## 3. Constraint propagation

The scalar equations imply
\[
\dot\rho+3H(\rho+p)=0.
\]
Differentiating \(C=3M_{\rm Pl}^2H^2-\rho\):
\[
\dot C=6M_{\rm Pl}^2H\dot H-\dot\rho=0
\]
when the acceleration equation and matter continuity hold. Thus an initially satisfied Friedmann constraint remains satisfied in the exact homogeneous equations. This is the FLRW form of the contracted Bianchi consistency condition, not an additional prediction.

## 4. Implementation and tests

- research/one_time_field/gravitational_flrw.py: Ricci scalar, Einstein tensor, Friedmann and acceleration residuals, coupled matter residuals, and constraint propagation.
- research/tests/test_gravitational_flrw.py: curvature tensors, both Friedmann equations, scalar-matter coupling, constraint propagation, and positive Planck-mass validation.
- research/examples/gravitational_flrw_experiment.py: dedicated runner.

The implementation evaluates equations algebraically. It does not yet integrate a cosmological history, add radiation or matter fluids, or compare with measured expansion data.

## 5. Interpretation and limitations

This experiment adds standard Einstein gravity to the two-scalar matter ansatz. It does not show that T is physical time, that it is a new source of gravity beyond its ordinary stress-energy, or that One Time Field Theory is empirically correct. Stability, perturbations, initial conditions, and observational constraints remain open.

**Conclusion:** Experiment 13 derives and tests the homogeneous Einstein equations for the coupled scalar model. It establishes a mathematical route to dynamical geometry, not a novel or validated theory of gravity.
