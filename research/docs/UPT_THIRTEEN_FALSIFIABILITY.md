# UPT-13 — Falsifiability and Held-Out Model Comparison

**Author:** Pablo Salvador Cardenas

## Objective

UPT-13 defines a concrete test for the memory-relaxation term rather than
treating a successful simulation as evidence for new physics. It compares:

- Coupled model: \(\dot m=r(u-m)\), with fitted \(r\geq0\).
- Null model: \(\dot m=0\), equivalent to \(r=0\).

Here \(u\) is a measured or prescribed field mean held constant over each
sampling interval. The exact interval propagator is
\[
m_{i+1}=u_i+(m_i-u_i)e^{-r\Delta t_i}.
\]

The model is a standard first-order relaxation law. UPT-13 does not claim it
is novel; it establishes a reproducible protocol for asking whether this
coupling improves predictions over a simpler null.

## Protocol

1. Predeclare the sampling times, the observable definitions for \(u\) and
   \(m\), the maximum admissible rate, and the training/hold-out split.
2. Fit the nonnegative relaxation rate using only early transitions.
3. Score both the fitted coupled model and the fixed-rate-zero null on later,
   held-out transitions.
4. Report training AICc and held-out RMSE, without changing the split after
   seeing the results.
5. Do not claim evidence for coupling unless the coupled model improves
   held-out RMSE and has lower training AICc. A non-improvement is a failure
   of this test to support added coupling, not proof that every possible
   memory model is false.

## Falsification conditions and limitations

The proposed relaxation term is not supported in a given experiment if its
held-out predictions do not improve on the null under the predeclared
measurement protocol, or if the fitted rate is consistent with zero once
measurement uncertainty is included. The current implementation uses exact
synthetic trajectories and deterministic scores; it does not yet calculate
confidence intervals or account for measurement noise, correlated errors,
or uncertainty in \(u\). Those are required before an empirical claim.

## Synthetic verification

The included experiment generates data from known rates and checks whether
the fitting routine recovers a nonzero rate and improves held-out prediction.
A separate zero-coupling test checks that the null is not spuriously
outperformed. These tests validate the estimator and protocol on constructed
data only.

## Next empirical requirements

- Define physical measurement operators for \(u\) and \(m\).
- Specify an instrument, sampling cadence, noise model, and calibration.
- Pre-register a train/hold-out split and decision thresholds.
- Compare against established relaxation and reaction-diffusion alternatives.
- Report uncertainty intervals, residual diagnostics, and replication.

## Files

- `research/one_time_field/upt13_falsifiability.py`
- `research/tests/test_upt13_falsifiability.py`
- `research/examples/upt13_falsifiability_experiment.py`
- `research/docs/UPT_THIRTEEN_FALSIFIABILITY.md`

Passing tests establish software behavior on synthetic cases, not empirical
support for UPT or a new physical mechanism.
