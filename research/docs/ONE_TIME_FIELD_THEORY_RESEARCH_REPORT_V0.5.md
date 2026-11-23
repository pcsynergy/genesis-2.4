# One Time Field Theory Research Report — Version 0.5

**Author:** Pablo Salvador Cardenas  
**Project:** GENESIS 2.4 — One Time Field Foundation  
**Research branch:** `research/one-time-field-foundation`  
**Date:** 23 November 2026  
**Status:** Mathematical prototype with a Lorentz-covariant action and its flat-spacetime Noether stress-energy conservation law; not an empirically validated physical theory.

## Executive summary

Version 0.5 adds **Experiment 10: stress-energy tensor and conservation**. It follows the Lorentz-covariant two-scalar field action developed in Experiment 9. The symmetric stress-energy tensor is derived, its energy density is checked against the Hamiltonian density, and its divergence is shown to equal the Euler–Lagrange residuals multiplied by the corresponding field gradients.

The earlier experiments and Lorentz-covariant action are documented in [Report v0.4](ONE_TIME_FIELD_THEORY_RESEARCH_REPORT_V0.4.md).

## 1. Stress-energy tensor

For the fixed Minkowski metric with signature ((- ,+)),

[
T^{mu
u}=
partial^muphipartial^
uphi+
Z_Tpartial^mu Tpartial^
u T+
eta^{mu
u}mathcal L.
]

The components are

[
T^{00}=dotphi^2+Z_Tdot T^2-mathcal L,quad
T^{01}=T^{10}=-dotphiphi_x-Z_Tdot T T_x,
]

[
T^{11}=phi_x^2+Z_T T_x^2+mathcal L.
]

The energy density (T^{00}) matches the Hamiltonian density obtained from the action.

## 2. Local conservation identity

Define the field-equation residuals

[
R_phi=Boxphi-m^2phi+gT f'(phi),
qquad
R_T=Z_TBox T-mu_T^2T+g f(phi).
]

Differentiating the tensor gives the off-shell identity

[
partial_mu T^{mu
u}
=R_phipartial^
uphi+R_Tpartial^
u T.
]

On solutions of both Euler–Lagrange equations, (R_phi=R_T=0), and therefore

[
oxed{partial_mu T^{mu
u}=0.}
]

This is the expected Noether energy-momentum conservation law from translation invariance of the action in flat spacetime.

## 3. Experiment 10 implementation and tests

The research layer now includes:
- `research/one_time_field/stress_energy.py`: symmetric stress-energy tensor, divergence identity, and on-shell derivative helper.
- `research/tests/test_stress_energy.py`: symmetry, Hamiltonian-density agreement, on-shell conservation, and off-shell identity tests.
- `research/examples/stress_energy_experiment.py`: standalone test runner.
- `research/docs/STRESS_ENERGY_EXPERIMENT.md`: derivation and limitations.

The GitHub Actions workflow now runs the experiment on Python 3.10, 3.11, and 3.12. The CI result for this commit must be checked separately; the derivation itself is a mathematical identity under the stated action and metric conventions.

## 4. Interpretation and limitations

This experiment establishes the expected local conservation law for the specified classical two-scalar theory on fixed flat Minkowski spacetime, assuming the field equations hold. It is not independent evidence that the proposed clock field exists in nature. Translation invariance implies this conservation law; the result is a consistency check, not a new empirical prediction.

The spacetime metric remains nondynamical. The model does not yet include general relativity, curved-background dynamics, metric backreaction, a full 3+1-dimensional implementation, gauge sectors, quantization, or experimental calibration. In curved spacetime, the relevant identity would be covariant conservation (
abla_mu T^{mu
u}=0), and coupling to a dynamical metric would require varying the full action with respect to that metric.

## 5. Next steps

1. Extend the formulation and stress-energy tests to 3+1-dimensional Minkowski spacetime.
2. Establish physical dimensions and field normalizations.
3. Study linearized modes, hyperbolicity, and perturbative stability.
4. Formulate a curved-background version and verify its covariant conservation identity before considering dynamical gravity.

**Conclusion:** Experiment 10 completes the flat-spacetime Noether consistency check for the Lorentz-covariant scalar/clock action. It does not establish physical time or a theory of gravity.
