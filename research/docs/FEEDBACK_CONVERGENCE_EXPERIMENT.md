# Experiment 4: feedback convergence and parameter sensitivity

## Purpose

Experiment 3 found that its explicitly added, delayed clock-rate source
separates the feedback trajectory from the control trajectory. Experiment 4
checks whether that result is stable under timestep refinement and how its
magnitude responds to the selected feedback coefficient.

## Numerical protocol

Both systems begin from identical initial states and are integrated to the
same parameter-time horizon, lambda = 5. The control uses the original
equations. The coupled system adds the Experiment 3 scalar source
epsilon * (r_previous - b), where r_previous is the prior step's
field-activity clock rate.

The convergence schedule is dt = 0.02, 0.01, 0.005, 0.0025, 0.00125.
For each run, the reported diagnostic is the Euclidean distance between
control and coupled final states. A second sweep fixes dt = 0.0025 and varies
epsilon = 0, 0.01, 0.025, 0.05, 0.1.

This is a refinement/sensitivity study, not a claim that a particular
continuum limit is a physical law. Because the clock feedback is delayed by
one numerical step, reducing dt also reduces the delay in parameter-time.

## Interpretation

- The epsilon = 0 case is a null control: the trajectories should coincide.
- A finite nonzero response at positive epsilon verifies that the implemented
  additional source affects this model.
- Convergence of the separation across smaller dt values supports numerical
  robustness of this particular discretized model. It does not validate the
  physical premise of clock-to-field feedback.
- The strength sweep characterizes sensitivity for the chosen initial state
  and parameterization; monotonicity is not assumed as a universal property.

## Limits and next tests

The state distance mixes variables with different units and therefore remains
a dimensionless prototype diagnostic. Physical interpretation requires
normalization, calibrated coefficients, a derived interaction law, and an
independent operational observable. Further work should compare alternative
integrators, test stability over broader parameter ranges, and derive or
constrain the coupling from an action or symmetry principle.
