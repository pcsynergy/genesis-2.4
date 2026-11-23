# Experiment 3: field–clock feedback

## Question

Can a field-derived relational clock become dynamically consequential, rather
than acting only as a new parameter along an unchanged trajectory?

## Hypothesis and model

The clock rate is calculated from field activity:

\`r_n = b + eta A(Psi_n)\`.

The control system uses the original scalar, phase, and tensor-array
equations. The feedback system adds an explicit, one-step-delayed clock source
to the scalar equation:

\`d(phi_i)/d(lambda) = F_phi_i(Psi) + epsilon [r_(n-1) - b]\`.

The phase and tensor equations and all original cross-domain couplings remain
unchanged. The added source is uniform across scalar nodes. The one-step lag
makes the update explicit and avoids solving an implicit clock/field equation
at every step. The initial states and all baseline parameters are identical.

## Why this is not just reparameterization

A pure clock reparameterization divides every state derivative by the same
positive clock rate and preserves the path in state space. This experiment
adds a new source to only the scalar field. That term is not proportional to
the original full state-space vector field, so it can change the trajectory.
A measured nonzero difference is therefore a consequence of the newly
postulated interaction, not evidence that the clock definition alone changes
the physics.

## Procedure and diagnostics

1. Initialize control and feedback systems identically.
2. Calculate scalar, phase, and tensor mean-square derivative activity.
3. Map activity to a positive clock rate.
4. Use the previous step's clock-rate excess to form the scalar feedback.
5. Advance both systems with the same explicit time step.
6. Record activity, clock rates, feedback source, and state-space distance.

The default run uses dimensionless toy parameters: dt=0.01, eta=0.25,
b=1, and epsilon=0.05. These are not empirically fitted constants.

## Falsifiable checks

- With epsilon=0, the feedback and control trajectories must coincide.
- With eta=0, the rate equals the baseline and the proposed feedback source
  must vanish.
- With nonzero gains, the implementation tests whether the field trajectories
  separate while remaining finite.
- A timestep-refinement study is needed to distinguish robust behavior from
  numerical artifacts before interpreting any quantitative effect.

## Interpretation limits

A nonzero trajectory separation demonstrates only that the added source
changes this toy model. It does not establish a physical clock-field coupling,
a universal law, or a measured effect. The aggregate activity combines
different state variables; physical use requires dimensional normalization,
calibrated coefficients, and an operational clock observable. The tensor
state is still a component-wise array prototype, not a covariant tensor field.

A later research stage should derive the interaction from a stated action or
symmetry principle, identify its units, establish stability, and specify an
independent observable that could distinguish the model from existing
dynamical theories.
