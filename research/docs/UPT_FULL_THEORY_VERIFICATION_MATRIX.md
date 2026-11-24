# UPT Integrated Reference — Verification Matrix

| Layer | Executable representation | Invariants / checks | What passing establishes | What it does not establish |
|---|---|---|---|---|
| Potential | Finite binary configuration domain | Domain expands monotonically; finite closure | Renewal algorithm behaves as specified | Ontological or physical creation |
| Relations | Symmetric weighted graph | Valid weights; shared graph dimensions | Relational topology is well-formed | A new fundamental interaction |
| Reversible memory | Finite-state CTMC | Generator conservation, Gibbs normalization, detailed balance | Equilibrium stochastic implementation is consistent | Equivalence to deterministic field flow |
| Continuous becoming | Onsager graph gradient flow | Energy nonincrease; finite state; valid step | Dissipative numerical trajectory is consistent | Conservative dynamics or a physical law |
| Continuum | Periodic scalar gradient-flow discretization | Refinement error and variational checks | Numerical approximation converges for tested setup | A universal continuum limit for every UPT layer |
| Observation | Gaussian measurement model | Reproducibility, rate fit, bootstrap interval, null Monte Carlo | Inference code follows declared synthetic assumptions | Empirical evidence or correct real-world noise model |

## Integrated run acceptance criteria

The full reference runner is considered computationally healthy when:
1. the finite potential domain grows and reaches closure;
2. the CTMC stationary distribution sums to one and detailed-balance residual is numerically negligible;
3. the continuous field energy does not increase;
4. the tested continuum refinement errors decrease with resolution;
5. the noisy observation layer returns a nonnegative rate estimate, an ordered interval, and a valid Monte Carlo p-value;
6. the integration report explicitly records the non-equivalence of model classes.

These are software/model checks, not scientific confirmation of the UPT ontology. Empirical validation requires operational measurement definitions, calibrated units, independently justified noise assumptions, out-of-sample data, and comparison with established alternatives.

**Author:** Pablo Salvador Cardenas.
