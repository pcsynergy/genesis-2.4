# One Time Field Theory Research Report — Version 0.8

**Author:** Pablo Salvador Cardenas  
**Project:** GENESIS 2.4 — One Time Field Foundation  
**Research branch:** research/one-time-field-foundation  
**Date:** 23 November 2026  
**Status:** Classical Einstein–two-scalar mathematical model; not empirically validated.

## Executive summary

Version 0.8 adds Experiment 13: metric variation and dynamical FLRW gravity. The existing two-scalar matter sector is coupled minimally to the Einstein–Hilbert action. The implementation evaluates the FLRW Ricci scalar and Einstein tensor, the Friedmann constraint, the acceleration equation, and propagation of the Friedmann constraint under matter continuity.

This is a standard general-relativistic completion of the selected matter ansatz. It is not a new gravitational law, and the calculation does not establish that the scalar clock field is physical time.

## 1. Full action and metric variation

The action is
\[
S[g,\phi,T]=\int d^4x\sqrt{-g}
\left[\frac{M_{\rm Pl}^2}{2}R+\mathcal L_m\right],
\quad M_{\rm Pl}^2=(8\pi G)^{-1}>0.
\]
With
\[
T_{\mu\nu}=-\frac{2}{\sqrt{-g}}
\frac{\delta(\sqrt{-g}\mathcal L_m)}{\delta g^{\mu\nu}},
\]
metric variation gives
\[
M_{\rm Pl}^2G_{\mu\nu}=T_{\mu\nu}.
\]
The matter-field variations retain the Experiment 12 equations.

## 2. FLRW curvature and gravitational equations

For spatially-flat FLRW with signature (-+++):
\[
R=6(\dot H+2H^2),\quad
G_{00}=3H^2,\quad
G_{ij}=-(2\dot H+3H^2)g_{ij}.
\]
Thus
\[
3M_{\rm Pl}^2H^2=\rho,\qquad
-2M_{\rm Pl}^2\dot H=\rho+p.
\]
The density and pressure are those of the coupled scalar sector from Experiment 12.

## 3. Bianchi consistency and constraint propagation

The scalar equations imply
\[
\dot\rho+3H(\rho+p)=0.
\]
For the Friedmann constraint \(C=3M_{\rm Pl}^2H^2-\rho\):
\[
\dot C=6M_{\rm Pl}^2H\dot H-\dot\rho.
\]
Substituting the acceleration equation and continuity equation gives \(\dot C=0\). Therefore the Friedmann constraint is preserved by the exact homogeneous equations if it is satisfied initially. This is the FLRW form of the contracted Bianchi identity, not an independent empirical prediction.

## 4. Implementation and tests

- research/one_time_field/gravitational_flrw.py — Ricci scalar, Einstein tensor, Friedmann and acceleration residuals, scalar-matter equations, and constraint propagation.
- research/tests/test_gravitational_flrw.py — curvature tensors, Friedmann equations, scalar-matter coupling, constraint propagation, and Planck-mass validation.
- research/examples/gravitational_flrw_experiment.py — dedicated experiment runner.
- research/docs/GRAVITATIONAL_FLRW_EXPERIMENT.md — derivation, protocol, and limitations.

The implementation checks algebraic equations; it does not yet integrate full cosmological trajectories or fit measured data.

## 5. Interpretation and limitations

Experiment 13 couples the existing matter model to standard Einstein gravity. It does not establish a novel gravity theory, demonstrate that T is physical time, or show that T has any special gravitational role beyond contributing to the matter stress-energy. Radiation, baryonic matter, dark matter, perturbations, stability, parameter inference, and observational comparisons remain outside scope.

**Conclusion:** Experiment 13 establishes the homogeneous Einstein equations and their constraint-consistency relation for the selected two-scalar model. It is a mathematical GR extension, not an empirical validation of One Time Field Theory.
