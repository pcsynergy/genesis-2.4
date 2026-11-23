# GENESIS Research: One Time Field Foundation

This experimental research layer is separate from the legacy GENESIS 2.4 simulator. It does not alter the simulator's C sources or build system.

## Research report
- [One Time Field Theory Research Report v0.5](docs/ONE_TIME_FIELD_THEORY_RESEARCH_REPORT_V0.5.md) — consolidated findings from Experiments 1–10, including stress-energy conservation.
- [One Time Field Theory Research Report v0.4](docs/ONE_TIME_FIELD_THEORY_RESEARCH_REPORT_V0.4.md) — prior Lorentz-covariant formulation.
- [One Time Field Theory Research Report v0.3](docs/ONE_TIME_FIELD_THEORY_RESEARCH_REPORT_V0.3.md) — consolidated findings from Experiments 1–8, including the local clock-field extension.
- [One Time Field Theory Research Report v0.2](docs/ONE_TIME_FIELD_THEORY_RESEARCH_REPORT_V0.2.md) — prior report covering Experiments 1–7.

## Specifications
- [Architecture](docs/ARCHITECTURE.md)
- [Foundation](docs/FOUNDATION.md)
- [Formal specification](docs/FORMAL_SPECIFICATION.md)
- [Extensions](docs/EXTENSIONS.md) — conservation, harmonic oscillators, tensor-array states, shared-topology composition, variational dynamics, Hamiltonian dynamics, and Rayleigh damping.
- [Dimensional analysis and symmetry](docs/DIMENSIONAL_ANALYSIS.md) — reference scales, mobility units, and conditional conservation results.
- [Action, Lagrangian, and Hamiltonian formulations](docs/ACTION_PRINCIPLE.md) — conservative and dissipative alternatives built from the shared potential.

## Implemented models
- one_time_field/network.py — scalar graph diffusion with decay and external source.
- one_time_field/harmonic.py — Kuramoto-style phase-coupled oscillator network.
- one_time_field/tensor.py — component-wise tensor-array graph diffusion prototype.
- one_time_field/engine.py — dimensional engine composing the models on one shared graph with two explicit cross-domain coupling rules.
- one_time_field/field_activity.py — field-derived mean-square derivative activity and candidate relational clock rate.
- one_time_field/temporal_comparison.py — paired external-time and relational-time integration using the chain-rule reparameterization.
- one_time_field/temporal_coupling.py — explicit delayed feedback from a field-derived clock rate into scalar-field dynamics.
- one_time_field/feedback_convergence.py — Experiment 4 timestep refinement and feedback-strength sensitivity study.
- one_time_field/clock_action.py — Experiment 5 augmented Lagrangian/Hamiltonian with a dynamical clock coordinate coupled to scalar-field amplitude.
- one_time_field/unified_action.py — Experiment 6 shared action coupling scalar, phase, tensor-array, and dynamical-clock degrees of freedom; includes global phase-shift Noether charge.
- one_time_field/continuum_action.py — Experiment 7 periodic 1-D scalar continuum-field action coupled to a global dynamical clock; includes grid-refinement and energy-drift diagnostics.
- one_time_field/local_clock_field.py — Experiment 8 spatially local clock field coupled pointwise to a scalar field, with propagation, energy, and grid-refinement diagnostics.
- one_time_field/lorentz_covariant.py — Experiment 9 Lorentz-covariant two-scalar action, boost transformations, d'Alembertian, and Euler–Lagrange residuals.
- one_time_field/stress_energy.py — Experiment 10 symmetric stress-energy tensor, Hamiltonian density, and on-shell conservation identity.
- docs/LOCAL_CLOCK_FIELD_EXPERIMENT.md — Experiment 8 local clock-field action, equations, numerical protocol, and covariance limitations.
- docs/LORENTZ_COVARIANT_EXPERIMENT.md — Experiment 9 covariant action, field equations, boost-invariance tests, and scope limitations.
- docs/STRESS_ENERGY_EXPERIMENT.md — Experiment 10 stress-energy tensor, Noether identity, and conservation tests.
- examples/local_clock_field_experiment.py — runs the Experiment 8 local clock-field refinement study.
- docs/CONTINUUM_FIELD_EXPERIMENT.md — Experiment 7 continuum ansatz, equations, numerical protocol, and physical interpretation limits.
- examples/continuum_action_experiment.py — runs the Experiment 7 spatial-grid refinement study.
- docs/UNIFIED_SHARED_ACTION_EXPERIMENT.md — Experiment 6 action, symmetries, controlled limits, and interpretation limits.
- examples/unified_action_experiment.py — demonstrates the unified clock–field action and uncoupled limit.
- docs/FIELD_DERIVED_ACTIVITY.md — Experiment 1 procedure, assumptions, and interpretation limits.
- docs/TEMPORAL_TIME_COMPARISON_EXPERIMENT.md — Experiment 2 paired-clock comparison and interpretation limits.
- docs/FIELD_CLOCK_FEEDBACK_EXPERIMENT.md — Experiment 3 field–clock feedback hypothesis and interpretation limits.
- docs/FEEDBACK_CONVERGENCE_EXPERIMENT.md — Experiment 4 numerical refinement and parameter sensitivity protocol.
- docs/CLOCK_ACTION_EXPERIMENT.md — Experiment 5 action-derived clock–field interaction and interpretation limits.
- one_time_field/variational.py — shared dimensionless potential functional and gradient flow.
- one_time_field/hamiltonian.py — canonical conservative dynamics using velocity-Verlet.
- one_time_field/damped.py — Rayleigh-damped Hamiltonian dynamics using symmetric damping/Verlet operator splitting.
- one_time_field/temporal.py — parameter, relational, and observer-time accumulators.
- one_time_field/temporal_models.py — external, relational, entropy-production, event, observer, and hybrid clock hypotheses.
- docs/TEMPORAL_COMPARISON.md — assumptions, chain-rule reparameterization, and boundaries for quantum-relational and causal-set extensions.
- docs/TEMPORAL_ARCHITECTURE.md — temporal distinctions, assumptions, and falsifiable next steps.
- tests/ — invariant, validation, extension, variational, Hamiltonian, damping, convergence, and temporal tests.
- examples/temporal_clock_demo.py — demonstrates separate temporal layers.
- examples/temporal_models_demo.py — compares distinct clock readings side by side.
- examples/field_derived_activity_experiment.py — derives a candidate clock rate from live scalar, phase, and tensor derivatives.
- examples/temporal_time_comparison.py — compares external and relational time on identical initial field states.
- examples/temporal_coupling_experiment.py — compares a control system with explicit clock-to-field feedback.
- examples/feedback_convergence_experiment.py — timestep refinement and feedback-strength sweep.
- examples/clock_action_experiment.py — conservative dynamical-clock coupling demonstration.
- examples/dynamics_comparison_demo.py — same-initial-state comparison of three dynamics regimes.
- examples/dynamics_convergence_study.py — analytic-reference timestep study with state errors, energy drift, and damping-balance residuals.
- examples/coupled_network_regimes.py — three-node scalar/phase/tensor-array network comparison across gradient, Hamiltonian, and damped dynamics.

## Run
Requires Python 3.10 or newer.

    python -m unittest discover -s research/tests -v
    python research/examples/two_node_demo.py
    python research/examples/dimensional_engine_demo.py
    python research/examples/variational_demo.py
    python research/examples/hamiltonian_demo.py
    python research/examples/dynamics_comparison_demo.py
    python research/examples/dynamics_convergence_study.py
    python research/examples/coupled_network_regimes.py
    python research/examples/temporal_clock_demo.py
    python research/examples/temporal_models_demo.py
    python research/examples/field_derived_activity_experiment.py
    python research/examples/temporal_time_comparison.py
    python research/examples/temporal_coupling_experiment.py

## Scientific discipline
These are mathematical experiments, not validated physical field theories. The tensor prototype does not define geometric tensor transformation laws. The shared potential is a selected dimensionless functional, not established physical energy. The damping coefficients and inertias are model parameters, not measured constants. Numerical behavior validates the specified equations and integrator only; it does not establish a physical mechanism or a unique unified field equation.
