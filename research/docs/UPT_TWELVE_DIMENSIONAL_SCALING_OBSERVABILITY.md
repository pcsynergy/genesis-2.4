# UPT-12 — Dimensional Scaling and Observability

**Author:** Pablo Salvador Cardenas

## Purpose

UPT-11 established a numerically convergent discretization of a periodic scalar
gradient-flow model with global memory coupling. UPT-12 asks what would be
required to connect that mathematical model to measurements. It adds
dimensionful parameter bookkeeping, a matched memory-coupled versus
memory-uncoupled experiment, and a deliberately limited identifiability test.

This is a phenomenological reaction-diffusion/gradient-flow model. The work
does not establish a new physical law or an empirical prediction.

## Dimensional audit

For
[
H=\int_0^L dx\left[\frac J2(\partial_x\phi)^2+
\frac\lambda4\phi^2(1-\phi)^2\right]
+\frac{\kappa L}{2}(\bar\phi-m)^2,
]
take dimensions [x]=L, [t]=T, [phi]=[m]=Phi, and [H]=E. Then
[
[J]=E L/Phi^2,\quad [\kappa]=E/(L Phi^2),\quad
[\lambda]=E/(L Phi^4).
]
For the L2 gradient-flow metric used in UPT-11,
[
[\Gamma_\phi]=[\Gamma_m]=Phi L/(E T).
]
The scaling module converts these to dimensionless coefficients using
reference scales L0, T0, Phi0, E0. This makes the dimensional assumptions
explicit; it does not determine the physical units or values.

## Matched model comparison

The experiment runs the same initial field and memory coordinate twice:
once with kappa>0 and once with kappa=0. It reports changes in spatial mean,
variance, memory coordinate, and energy. These are synthetic model
sensitivities, not measurements. A nonzero difference only shows that the
coupling changes this model's trajectory.

## Identifiability limit

The memory equation is
[
\dot m=\Gamma_m\kappa(\bar\phi-m).
]
If the only measured equation is m(t) with the mismatch signal
(\bar\phi-m), the data constrain the product Gamma_m*kappa. They cannot
separately determine Gamma_m and kappa without independent information,
additional observables, or an experimental intervention that breaks the
confounding. The implemented least-squares estimator demonstrates this
structural limitation using synthetic observations.

## What would be needed for a physical test

1. Specify what phi and m physically measure, including a measurement operator.
2. Assign SI units and independently calibrate at least one of Gamma_m or kappa.
3. Define a protocol that varies mismatch and coupling conditions.
4. Propagate measurement uncertainty and compare out-of-sample predictions.
5. Compare against established uncoupled reaction-diffusion and mean-field
   models using the same data and complexity controls.

## Files and verification

- `research/one_time_field/upt12_observability.py`
- `research/tests/test_upt12_observability.py`
- `research/examples/upt12_observability_experiment.py`

The unit tests cover dimensional conversion, invalid inputs, matched baseline
comparison, recovery of the identifiable parameter product, and a zero-signal
unidentifiability case. Passing tests validate these implementation properties
only, not nature or the UPT ontology.
