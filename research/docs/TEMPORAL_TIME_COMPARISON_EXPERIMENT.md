# Experiment 2: fundamental-time and relational-time comparison

## Research question

With identical initial field states and the same field equations, does a
field-derived relational clock produce a different physical trajectory, or
does it relabel the parameter along the same trajectory?

## Competing descriptions

The external-time description is

`d Psi / d lambda = F(Psi),    t_external = lambda.`

The candidate relational clock from Experiment 1 is

`d tau / d lambda = r(Psi) = b + eta A(Psi),    r(Psi) > 0.`

By the chain rule, the same state evolution expressed in relational time is

`d Psi / d tau = F(Psi) / r(Psi).`

The paired experiment starts both engines from exactly the same scalar,
phase, and tensor-array state. At each step it evaluates the same activity
rate, advances the external branch by d_lambda, and advances the relational
branch by d_tau = r*d_lambda using the reparameterized right-hand side.

## Numerical result expected from the mathematics

For a strictly positive rate, this is a change of parameter. In the
continuous limit, both descriptions trace the same path through state space;
they differ in the clock reading assigned to each point. With a matched
explicit-Euler step, the relational state increment is

`d_tau * (F/r) = (r*d_lambda) * (F/r) = d_lambda*F.`

The implementation checks the maximum component-wise state difference,
reports field observables against both clock readings, and verifies that the
relational clock advances monotonically. This identity is a mathematical
consistency check, not evidence that physical time is emergent.

## Interpretation

If the model contains only a positive state-dependent reparameterization,
the two time descriptions are observationally equivalent for observables
that depend only on the field-state path and do not independently measure
the clock. A distinct physical prediction requires additional structure:
for example, a clock-coupling term in the field equations, a calibrated
operational clock observable, or an independently specified physical law
that distinguishes the candidate clock from a coordinate relabeling.

This is important for One Time Field Theory: a dual-aspect view (a parameter
used to describe evolution plus a relational clock built from interactions)
can be explored, but the present prototype does not decide whether time is
fundamental, emergent, or both.

## Dimensional limits

The activity aggregate combines derivatives from domains with different
state units. Its weights and baseline require dimensional calibration before
physical interpretation. Current values are dimensionless toy parameters.
The tensor state remains a component-wise array, and phase activity depends
on the chosen phase/frequency convention.

## Reproducibility

Run:

`python research/examples/temporal_time_comparison.py`

Tests:

`python -m unittest research/tests/test_temporal_comparison.py -v`

The CSV-like output includes lambda, tau, clock rate, activity, scalar mean,
phase coherence, tensor RMS, and maximum state discrepancy.
