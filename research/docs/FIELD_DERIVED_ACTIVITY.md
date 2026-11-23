# Experiment 1: field-derived temporal activity

## Research question

Can a candidate relational clock rate be calculated from the evolving scalar,
phase, and tensor-array states, rather than supplied as an arbitrary activity
signal?

## Operational definition

For each active domain, calculate the mean square of its state derivative:

`A_phi = mean_i[(d phi_i / d lambda)^2]`

`A_theta = mean_i[(d theta_i / d lambda)^2]`

`A_T = mean_{i,k}[(d T_{ik} / d lambda)^2]`

Then combine them using explicit nonnegative weights:

`A = a_phi A_phi + a_theta A_theta + a_T A_T`

The prototype clock rate is:

`d tau / d lambda = b + eta A`

where `b > 0` and `eta >= 0`. The code uses `b=1` and `eta=0.25`
in the illustrative experiment.

## Dimensional and interpretive limits

The three derivative terms need not share units or scales. Their weights must
be assigned dimensions or the state variables must first be normalized before
the aggregate can be interpreted physically. The default equal weights are
only convenient dimensionless demonstration settings.

The phase derivative depends on the chosen phase representation and frequency
units. The tensor prototype remains a component-wise array model, not a
covariant tensor theory. This observable is a candidate activity measure, not
entropy production, proper time, or a measured physical clock.

## Experiment procedure

1. Initialize a three-node shared graph with scalar, phase, and tensor-array
   states.
2. Calculate each domain's instantaneous derivative using its implemented
   governing equation.
3. Compute per-domain mean-square derivative activity.
4. Combine the terms using declared weights.
5. Map the aggregate to a positive relational clock rate.
6. Advance the same field engine and accumulate the relational reading.
7. Emit reproducible CSV-formatted diagnostics at fixed intervals.

## What the experiment can establish

The tests can establish that the activity is calculated from the actual
implemented field derivatives, that domain weights behave as specified, and
that the resulting candidate clock rate remains positive under the stated
parameter constraints.

It cannot establish that this activity is a universal physical measure of
time, that observers experience time this way, or that the model describes a
real physical system.

## Next falsifiable questions

- Does the candidate clock remain invariant under consistent reparameterization?
- Which normalization and dimensional weights are physically justified?
- Do different field domains contribute independently or redundantly?
- Can an independently measured clock be predicted from field observables?
