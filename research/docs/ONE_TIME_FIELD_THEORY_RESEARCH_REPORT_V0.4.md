# One Time Field Theory Research Report — Version 0.4

**Author:** Pablo Salvador Cardenas  
**Project:** GENESIS 2.4 — One Time Field Foundation  
**Research branch:** `research/one-time-field-foundation`  
**Date:** 23 November 2026  
**Status:** Mathematical prototype; Experiment 9 supplies a Lorentz-covariant classical field ansatz and algebraic symmetry tests, not empirical validation.

## Executive summary

Version 0.4 adds **Experiment 9: Lorentz-covariant scalar and clock fields** to the research program. The prior numerical and conceptual results from Experiments 1–8 are retained in [Report v0.3](ONE_TIME_FIELD_THEORY_RESEARCH_REPORT_V0.3.md).

Experiment 9 replaces the preferred-frame, unequal-speed clock-field model of Experiment 8 with a two-scalar action on fixed 1+1-dimensional Minkowski spacetime. Both fields share the same Minkowski wave operator. Executable tests check boost invariance of the kinetic contractions, complete Lagrangian density, d'Alembertian, and Euler–Lagrange residuals.

## 1. Covariant action

Use metric signature ((- ,+)), coordinates (x^mu=(t,x)), and natural units (c=1). Treat (phi(x)) and (T(x)) as real Lorentz-scalar fields:

[
S=int d^2x,mathcal L,
]

[
mathcal L=
-rac12partial_muphipartial^muphi
-rac12m^2phi^2
-rac{Z_T}{2}partial_mu Tpartial^mu T
-rac{mu_T^2}{2}T^2
+gT f(phi),
qquad
f(phi)=rac12rac{phi^2}{1+phi^2}.
]

The parameters are constants, with (Z_T>0), (m^2ge0), and (mu_T^2>0). No preferred timelike vector or separate propagation speed appears.

## 2. Field equations

For (Box=partial_mupartial^mu=-partial_t^2+partial_x^2),

[
Boxphi-m^2phi+gTrac{phi}{(1+phi^2)^2}=0,
]

[
Z_TBox T-mu_T^2T+g f(phi)=0.
]

The principal parts are the same Minkowski d'Alembertian. This is the key structural change from Experiment 8, whose independent propagation speeds select a preferred frame unless further structure is supplied.

## 3. Lorentz-covariance test suite

The test suite applies finite boosts with several subluminal velocities and checks:

- ( partial_muphipartial^muphi ) and ( partial_mu Tpartial^mu T ) remain invariant.
- The complete Lagrangian density is unchanged when scalar field values and derivative components are transformed consistently.
- The d'Alembertian is invariant, including the contribution of mixed second derivatives.
- Both Euler–Lagrange residuals are frame-independent scalars.
- Invalid, luminal, or superluminal boost parameters are rejected.

These tests are algebraic symmetry checks of the action and equations. They do not simulate or experimentally measure physical Lorentz symmetry.

## 4. Stability observation

The potential is

[
V(phi,T)=rac12m^2phi^2+rac12mu_T^2T^2-gTf(phi).
]

Completing the square,

[
V=rac12mu_T^2left(T-rac{g f(phi)}{mu_T^2}ight)^2
+rac12m^2phi^2-rac{g^2f(phi)^2}{2mu_T^2}.
]

Since (0le f(phi)<1/2), the negative contribution is bounded. Under the stated parameter restrictions, this potential is bounded below. This is a basic classical potential check, not a complete perturbative or quantum stability analysis.

## 5. Interpretation and limitations

Experiment 9 supports the narrower mathematical statement that this two-scalar action is Lorentz covariant in flat 1+1-dimensional spacetime, assuming both fields transform as scalars. It does **not** establish that (T) is elapsed proper time, that the field exists in nature, or that One Time Field Theory is a complete physical theory.

The construction has no dynamical spacetime metric, Einstein–Hilbert term, curved-spacetime backreaction, gauge-sector completion, quantization, or empirical calibration. General covariance and gravity remain untested. Dimensional assignments for all fields and couplings must be fixed before physical parameter interpretation.

## 6. Reproducibility

Run the focused experiment:

```bash
python research/examples/lorentz_covariant_experiment.py
```

Run the complete research test suite:

```bash
python -m unittest discover -s research/tests -v
```

The CI workflow includes Experiment 9 on Python 3.10, 3.11, and 3.12. The corrected full workflow run [45168489466](https://github.com/pcsynergy/genesis-2.4/actions/runs/45168489466) completed successfully on commit `0032a72f295226d1f1ffc34f6ccc3c2635a57448`: all three Python matrix jobs passed, including the full unit-test suite and the dedicated Lorentz-covariance experiment. An earlier run exposed and helped correct a standalone test-runner import-path issue; the successful run is the corrected commit.

## 7. Next research steps

1. Extend the transformation and action tests to 3+1-dimensional Minkowski spacetime.
2. Derive the symmetric stress-energy tensor and verify on-shell conservation under translations.
3. Establish physical dimensions and normalized field units.
4. Study the linearized spectrum, hyperbolicity, and perturbative stability around vacuum solutions.
5. Only after the flat-spacetime tests, consider a curved-background extension and then a dynamical metric. Do not equate these stages with a completed theory of gravity.

**Conclusion:** Experiment 9 is a first explicit Lorentz-covariant formulation of the local clock–field coupling. It passes or fails a well-defined mathematical symmetry test; it does not yet demonstrate a physical time field.
