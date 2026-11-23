# GENESIS Research: One Time Field Foundation

This experimental research layer is separate from the legacy GENESIS 2.4 simulator. It does not alter the simulator's C sources or build system.

## Research reports
- [One Time Field Theory Research Report v0.9](docs/ONE_TIME_FIELD_THEORY_RESEARCH_REPORT_V0.9.md) — Experiment 14: numerical evolution of the coupled scalar–clock FLRW model; 2,400+ word peer-review-style report.
- [Experiment 14 protocol](docs/COSMOLOGICAL_EVOLUTION_EXPERIMENT.md) — equations, numerical method, tests, and limitations.
- [Research Report v0.8](docs/ONE_TIME_FIELD_THEORY_RESEARCH_REPORT_V0.8.md) — Experiment 13: Einstein–Hilbert metric variation and homogeneous FLRW gravitational equations.
- [Research Report v0.7](docs/ONE_TIME_FIELD_THEORY_RESEARCH_REPORT_V0.7.md) — Experiment 12: prescribed-FLRW curved-background extension.
- [Research Report v0.6](docs/ONE_TIME_FIELD_THEORY_RESEARCH_REPORT_V0.6.md) — 3+1-dimensional Minkowski extension.
- [Research Report v0.5](docs/ONE_TIME_FIELD_THEORY_RESEARCH_REPORT_V0.5.md) — Experiments 1–10.
- [Research Report v0.4](docs/ONE_TIME_FIELD_THEORY_RESEARCH_REPORT_V0.4.md)
- [Research Report v0.3](docs/ONE_TIME_FIELD_THEORY_RESEARCH_REPORT_V0.3.md)
- [Research Report v0.2](docs/ONE_TIME_FIELD_THEORY_RESEARCH_REPORT_V0.2.md)

## Specifications
- [Architecture](docs/ARCHITECTURE.md)
- [Foundation](docs/FOUNDATION.md)
- [Formal specification](docs/FORMAL_SPECIFICATION.md)
- [Extensions](docs/EXTENSIONS.md)
- [Dimensional analysis and symmetry](docs/DIMENSIONAL_ANALYSIS.md)
- [Action, Lagrangian, and Hamiltonian formulations](docs/ACTION_PRINCIPLE.md)

## Implemented models
- one_time_field/network.py — scalar graph diffusion.
- one_time_field/harmonic.py — phase-coupled oscillator network.
- one_time_field/tensor.py — component-wise tensor-array graph diffusion prototype.
- one_time_field/engine.py — shared-graph multi-domain engine.
- one_time_field/field_activity.py — field-derived derivative activity and candidate relational clock rate.
- one_time_field/temporal_comparison.py — external-time versus relational-time integration.
- one_time_field/temporal_coupling.py — delayed field-clock feedback.
- one_time_field/feedback_convergence.py — timestep refinement and feedback-strength sensitivity.
- one_time_field/clock_action.py — action-derived dynamical clock coordinate.
- one_time_field/unified_action.py — shared action for scalar, phase, tensor-array, and clock degrees of freedom.
- one_time_field/continuum_action.py — periodic 1-D continuum-field/global-clock model.
- one_time_field/local_clock_field.py — spatially local clock-field model.
- one_time_field/lorentz_covariant.py — Lorentz-covariant two-scalar action in 1+1 dimensions.
- one_time_field/stress_energy.py — stress-energy tensor and flat-space Noether identity.
- one_time_field/minkowski_3plus1.py — 3+1 Minkowski action, boosts, stress tensor, and conservation identity.
- one_time_field/flrw_curved.py — Experiment 12: prescribed-FLRW geometry and matter equations.
- one_time_field/gravitational_flrw.py — Experiment 13: Einstein tensor, Friedmann equations, and constraint propagation.
- one_time_field/cosmological_evolution.py — Experiment 14: coupled RK4 evolution of scale factor, Hubble rate, and two scalar fields.
- docs/FLRW_CURVED_EXPERIMENT.md — Experiment 12 derivation and limitations.
- docs/GRAVITATIONAL_FLRW_EXPERIMENT.md — Experiment 13 metric variation and gravity checks.
- docs/COSMOLOGICAL_EVOLUTION_EXPERIMENT.md — Experiment 14 numerical protocol and limitations.
- examples/flrw_curved_experiment.py — Experiment 12 runner.
- examples/gravitational_flrw_experiment.py — Experiment 13 runner.
- examples/cosmological_evolution_experiment.py — Experiment 14 runner.
- tests/ — numerical and algebraic consistency tests.

## Run
Requires Python 3.10 or newer.

    python -m unittest discover -s research/tests -v
    python research/examples/minkowski_3plus1_experiment.py
    python research/examples/flrw_curved_experiment.py
    python research/examples/gravitational_flrw_experiment.py
    python research/examples/cosmological_evolution_experiment.py

## Scientific discipline
These are mathematical experiments, not validated physical field theories. Experiment 14 numerically evolves the two-scalar matter ansatz with standard Einstein gravity and monitors Friedmann constraint drift. It does not establish that T is physical time, derive a novel gravity law, or provide empirical support against observations. The v0.9 report states the findings and limitations for independent review.
