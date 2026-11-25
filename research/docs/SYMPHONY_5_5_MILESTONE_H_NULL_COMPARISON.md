# Symphony 5.5 / UPT — Milestone H: Null-model comparison

**Status:** implemented; local runner and unit tests pass. CI validation pending.  
**Runner:** `research/examples/symphony_harmonic_null_comparison.py`  
**Tests:** `research/tests/test_symphony_null_comparison.py`

## Question

Does the specified coupled oscillator model make a distinguishable prediction from the uncoupled null model for the same initial conditions and intrinsic frequencies?

## Protocol

The experiment uses eight oscillators on a complete, unweighted graph. Intrinsic frequencies are \(\omega_i=1+0.03(i-3.5)\). Four fixed, nonsymmetric initial phase vectors are evolved for 3,000 RK4 steps with \(\Delta t=0.01\). The only changed parameter is coupling: \(K=0\) for the null model and \(K=1\) for the coupled model. The endpoint observable is the global order parameter

\[
R=\left|\frac{1}{N}\sum_{j=1}^{N}e^{i\theta_j}\right|.
\]

This is a deterministic, controlled model comparison, not a statistical test on empirical observations. The four starts are deliberately fixed test conditions, not a random sample from a population.

## Results

| Initial condition | Uncoupled \(K=0\) | Coupled \(K=1\) |
|---|---:|---:|
| 1 | 0.148731 | 0.998182 |
| 2 | 0.084875 | 0.998182 |
| 3 | 0.127682 | 0.998182 |
| 4 | 0.162721 | 0.998182 |
| **Mean** | **0.131002** | **0.998182** |

Mean difference in endpoint coherence: **0.867179**.

## Interpretation

For this chosen finite network, frequency spread, integration interval, and set of initial conditions, the coupled model predicts strong global phase coherence while the uncoupled model does not. The result makes the coupling term identifiable through a model-level observable under this protocol. It is consistent with the earlier coupling sweep, but it is not independent physical evidence: both models are evaluated inside the same mathematical framework.

## Falsifiability and next tests

The model-level prediction would be weakened if independently reproduced runs under the stated conditions failed to separate the two cases, if numerical refinement erased the difference, or if a better-specified null model reproduced the coupled model's endpoint and transient observables without the coupling term. Stronger follow-up work should use preregistered randomized initial conditions, multiple graph families, parameter uncertainty, transient trajectories, and held-out conditions. Any proposed physical application additionally requires a derived mapping from physical quantities to \(\theta_i\), \(K\), time units, graph edges, and measured observables.

## Scientific boundary

Milestones C–H test a finite phase-oscillator model: numerical behavior, topology sensitivity, convergence, local linear stability, and discrimination from an uncoupled null. They do **not** establish a physical spacetime field, a cosmological mechanism, consciousness dynamics, or empirical confirmation of Unified Potential Theory / One Time Field Theory. The bridge to physics remains a hypothesis requiring equations with units, independent data, competing-model comparison, and a risk of falsification.
