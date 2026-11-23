# Experiment 8 — Local clock-field dynamics

**Author:** Pablo Salvador Cardenas  
**Program:** One Time Field Theory (OTFT), GENESIS 2.4 research layer

## Objective

Replace Experiment 7's single global clock coordinate with a spatially local clock field (T(x,t)). The question is whether the scalar and clock fields can propagate and exchange energy locally in a controlled periodic model, and whether the discretized dynamics are stable under spatial refinement.

## Action ansatz

On a periodic one-dimensional domain (0\le x<L), define

[
S=\int dt\int_0^L dx\left[
\frac12\phi_t^2-\frac12c_\phi^2\phi_x^2-\frac12m^2\phi^2
+\frac12 I T_t^2-\frac12c_T^2T_x^2-\frac12\kappa T^2
+gT f(\phi)
\right],
]

where

[
f(\phi)=\frac12\frac{\phi^2}{1+\phi^2}.
]

The Euler–Lagrange equations are

[
\phi_{tt}=c_\phi^2\phi_{xx}-m^2\phi+
gT\frac{\phi}{(1+\phi^2)^2},
]

[
I T_{tt}=c_T^2T_{xx}-\kappa T+g f(\phi).
]

The autonomous energy is

[
E=\int_0^L dx\left[
\frac12\phi_t^2+\frac12c_\phi^2\phi_x^2+\frac12m^2\phi^2
+\frac12I T_t^2+\frac12c_T^2T_x^2+\frac12\kappa T^2
-gT f(\phi)
\right].
]

Both fields now have local spatial degrees of freedom. The interaction is pointwise in space, rather than mediated by a single global clock coordinate.

## Numerical method

The code uses periodic centered second differences for both spatial Laplacians and velocity-Verlet for the coupled second-order equations. A CFL-scaled timestep is used. The refinement experiment compares 32, 64, and 128 nodes against a 256-node reference at a common final time, recording RMS errors for both fields and total-energy drift.

## Interpretation limits

This is a classical 1-D toy model with a preferred evolution parameter (t), a flat periodic spatial domain, constant propagation speeds, and dimensionless parameters. It is not yet a Lorentz-covariant field theory. In particular, the two propagation speeds and the clock inertia have not been constrained by a common spacetime metric. Calling (T(x,t)) a local clock field is a model designation, not evidence that it measures proper time.

A physically meaningful relativistic extension would need a covariant action, defined field transformation properties, consistent units, causal/hyperbolic well-posedness analysis, and independent observable predictions. Numerical convergence alone cannot establish any of these.

## Reproduction

`python -m unittest discover -s research/tests -v`

`python research/examples/local_clock_field_experiment.py`
