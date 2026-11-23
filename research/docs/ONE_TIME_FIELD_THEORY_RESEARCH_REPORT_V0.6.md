# One Time Field Theory Research Report — Version 0.6

**Author:** Pablo Salvador Cardenas  
**Project:** GENESIS 2.4 — One Time Field Foundation  
**Research branch:** `research/one-time-field-foundation`  
**Date:** 23 November 2026  
**Status:** Mathematical prototype; fixed-background classical scalar-field model, not an empirically validated physical theory.

## Executive summary

Version 0.6 adds **Experiment 11**, extending the Lorentz-covariant two-scalar model and its stress-energy consistency checks from 1+1 to 3+1-dimensional Minkowski spacetime. The implementation checks scalar-gradient contractions and the full Lagrangian under boosts along coordinate axes and oblique directions, constructs the complete symmetric 4×4 contravariant stress-energy tensor, checks its energy density against the Hamiltonian density, and evaluates the off-shell Noether divergence identity and its on-shell consequence.

This is an algebraic dimensional extension on a fixed flat background. It does not establish that the clock scalar represents physical time or that the model describes nature.

## 1. Model

With metric \(\eta_{\mu\nu}=\mathrm{diag}(-1,+1,+1,+1)\) and natural units \(c=1\), the action density is
\[
\mathcal L=-\frac12\partial_\mu\phi\partial^\mu\phi
-\frac12m^2\phi^2
-\frac{Z_T}{2}\partial_\mu T\partial^\mu T
-\frac{\mu_T^2}{2}T^2+gT f(\phi),
\qquad f(\phi)=\frac12\frac{\phi^2}{1+\phi^2}.
\]
Both \(\phi\) and \(T\) are real Lorentz scalar fields. The flat-space wave operator is
\[
\Box=-\partial_t^2+\partial_x^2+\partial_y^2+\partial_z^2.
\]
The field-equation residuals are
\[
R_\phi=\Box\phi-m^2\phi+gT f'(\phi),\qquad
R_T=Z_T\Box T-\mu_T^2T+g f(\phi).
\]

## 2. Stress-energy and conservation

The symmetric contravariant tensor is
\[
T^{\mu\nu}=\partial^\mu\phi\partial^\nu\phi
+Z_T\partial^\mu T\partial^\nu T+\eta^{\mu\nu}\mathcal L.
\]
Its local Noether identity is
\[
\partial_\mu T^{\mu\nu}
=R_\phi\partial^\nu\phi+R_T\partial^\nu T.
\]
Thus \(\partial_\mu T^{\mu\nu}=0\) when both Euler–Lagrange equations hold. This follows from translation invariance and is a consistency condition, not an independent empirical prediction.

## 3. Experiment 11 implementation and tests

- `research/one_time_field/minkowski_3plus1.py`: 3+1 Minkowski gradient contractions, arbitrary-direction boost transformation, Lagrangian density, 4×4 stress-energy tensor, field-equation residuals, divergence identity, and on-shell time-derivative helper.
- `research/tests/test_minkowski_3plus1.py`: tests boost invariance for axis-aligned and oblique boosts, Lagrangian invariance, tensor symmetry, Hamiltonian-density agreement, on-shell zero divergence, off-shell identity, and rejection of invalid boosts.
- `research/examples/minkowski_3plus1_experiment.py`: standalone test runner.
- `research/docs/MINKOWSKI_3PLUS1_EXPERIMENT.md`: derivation, scope, and limitations.

The automated workflow runs the test suite and dedicated experiment on Python 3.10, 3.11, and 3.12. Its actual result is reported only after the workflow completes.

## 4. Scope and limitations

The metric remains fixed and flat. This work does not include curvature, metric backreaction, Einstein's field equations, gauge sectors, quantization, physical-unit calibration, or empirical data. The boost tests validate the transformation conventions and the chosen scalar action, not a new physical mechanism. The clock field remains a model degree of freedom, not measured proper time.

A curved-background extension would use \(g_{\mu\nu}\), the invariant measure \(\sqrt{-g}\,d^4x\), and covariant conservation. A dynamical gravitational model would additionally require varying the complete action with respect to the metric and solving the resulting coupled field equations.

## 5. Next research questions

1. Establish consistent physical dimensions and field normalizations.
2. Derive and analyze the linearized dispersion relations, hyperbolicity, and perturbative stability.
3. Formulate the action on a prescribed curved background and verify \(\nabla_\mu T^{\mu\nu}=0\).
4. Only after those steps, consider metric backreaction and compare any distinctive predictions with observations.

**Conclusion:** Experiment 11 establishes executable 3+1-dimensional flat-spacetime consistency checks for this specific two-scalar action. It does not establish physical time, curved spacetime dynamics, or a validated unified field theory.
