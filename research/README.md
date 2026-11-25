# GENESIS Research: One Time Field Foundation

This experimental research layer is separate from the legacy GENESIS 2.4 simulator. It does not alter the simulator's C sources or build system.

## Unified Potential Theory integration
- [UPT Foundational Specification 0.1](docs/UPT_FOUNDATION.md) — Potential → One → Both → Many → All → Becoming → renewed Potential; defines ontological Potential separately from model potential energy.
- [UPT–OTFT Integration 0.1](docs/UPT_OTFT_INTEGRATION.md) — maps UPT onto the existing GENESIS research architecture and cosmological model without changing the validated equations or overstating physical claims.
- [UPT Configuration-Space Formalization 0.1](docs/UPT_CONFIGURATION_SPACE.md) — defines model admissibility, constraints, relations, actualization, equivalence, and observables.

## UPT experiments
- [UPT-3: Two-Component Relational Unity Experiment](docs/UPT_THREE_EXPERIMENT.md) — exact two-node graph-coupling model, common/difference modes, analytic solution, and software tests.

## UPT experiments
- [UPT-3: Two-Component Relational Unity Experiment](docs/UPT_THREE_EXPERIMENT.md) — exact two-node model and common/difference modes.
- [UPT-4 and UPT-5: Multi-Component Relational Network Tests](docs/UPT_GRAPH_MILESTONES_4_5.md) — connected/disconnected networks, admissibility preservation, and coupled-versus-uncoupled observable comparison.
- [UPT-6: Conservation, Symmetry, and Physical Realization](docs/UPT_SIX_CONSERVATION_CONTINUUM.md) — Noether shift charge, graph-to-continuum distinctions, and the current absence of a distinctive empirical prediction.\n- [UPT-7: Potential, Field Interaction, and Observable Emergence](docs/UPT_SEVEN_POTENTIAL_INTERACTION.md) — exact finite configuration-space ensemble with a fixed-count constraint and relational-coherence observable.

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
- one_time_field/upt6_continuum.py — Noether shift-charge and periodic continuum-equation probes.
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
    python research/examples/upt6_continuum_probe.py\n    python research/examples/upt7_configuration_experiment.py
    python research/examples/upt10_action_principle_experiment.py
    python research/examples/upt11_continuum_limit_experiment.py

## Scientific discipline
These are mathematical experiments, not validated physical field theories. Experiment 14 numerically evolves the two-scalar matter ansatz with standard Einstein gravity and monitors Friedmann constraint drift. It does not establish that T is physical time, derive a novel gravity law, or provide empirical support against observations. The v0.9 report states the findings and limitations for independent review.

- [UPT-8: Renewed Potential and Adaptive Admissibility](docs/UPT_EIGHT_RENEWED_POTENTIAL.md) — interaction-driven expansion of a finite admissible domain, with closure and threshold tests.

- [UPT-9: Reversibility, Memory, and Thermodynamic Consistency](docs/UPT_NINE_REVERSIBILITY_MEMORY.md) — an 80-state reversible Markov model tests probability conservation, detailed balance, memory dependence, and adaptive admissibility.
- [UPT-10: Variational Relational-Memory Dynamics](docs/UPT_TEN_ACTION_PRINCIPLE.md) — derives a dissipative graph-field and memory flow from an Onsager/Rayleighian principle, with explicit distinction from conservative action and Markov jump dynamics.
- [UPT-11: Continuum Limit and Model-Level Observables](docs/UPT_ELEVEN_CONTINUUM_LIMIT.md) — constructs a periodic 1-D continuum gradient flow, defines mean/variance/memory observables, and tests finite-difference refinement.

## Symphony 5.5 manuscript integration

- [Symphony 5.5 → GENESIS map](docs/SYMPHONY_5_5_GENESIS_MAP.md) — manuscript-to-project architecture and implementation milestones.
- [Symphony 5.5 manuscript index](docs/SYMPHONY_5_5_MANUSCRIPT_INDEX.md) — working page/heading navigation for the 346-page manuscript.
- [Symphony 5.5 evidence register](docs/SYMPHONY_5_5_EVIDENCE_REGISTER.md) — initial separation of established background, model assumptions, mathematical results, interpretation, speculation, and open verification tasks.

The manuscript integration is documentation-first. It does not change GENESIS simulator sources or alter existing mathematical models. The index is a working navigation aid; verify exact printed-page placement before formal citation. The evidence register is initial triage, not a completed line-by-line fact-check.

- [Symphony 5.5 Milestone C: Harmonic Creation Experiment](docs/SYMPHONY_5_5_MILESTONE_C_HARMONIC_EXPERIMENT.md) — Kuramoto-style phase synchronization, coherence observable, numerical setup, and scientific limitations.
- Run `python research/examples/symphony_harmonic_creation.py` for the coupling-strength comparison.

- [Symphony 5.5 Milestone D: Topology and Robustness](docs/SYMPHONY_5_5_MILESTONE_D_ROBUSTNESS.md) — compares complete, path, and ring graphs across frequency dispersion and coupling strengths.
- Run `python research/examples/symphony_harmonic_robustness.py` for the topology and frequency-dispersion sweep.

- [Symphony 5.5 Milestone E: Multi-start thresholds and local/global coherence](docs/SYMPHONY_5_5_MILESTONE_E_THRESHOLDS.md) — 384-run deterministic grid over topology, frequency dispersion, coupling, and initial phase configurations; reports global and local edge observables.
- Run `python research/examples/symphony_harmonic_thresholds.py` for the Milestone E sweep.

- [Symphony 5.5 Milestone F: Numerical stability and convergence](docs/SYMPHONY_5_5_MILESTONE_F_NUMERICS.md) — compares Euler and RK4, refines time steps, and probes relaxation of a perturbed complete graph.
- Run `python research/examples/symphony_harmonic_numerics.py` for the Milestone F numerical checks.

- [Symphony 5.5 Milestone G: Analytical linear stability](docs/SYMPHONY_5_5_MILESTONE_G_STABILITY.md) — computes Jacobian spectra for synchronized and twisted states and tests transverse stability.
- Run `python research/examples/symphony_harmonic_stability.py` for the Milestone G stability analysis.


- [Symphony 5.5 Milestone H: Null-model comparison](docs/SYMPHONY_5_5_MILESTONE_H_NULL_COMPARISON.md) — compares coupled and uncoupled predictions over four fixed initial conditions; explicitly documents the model-level scope and falsification path.
- Run `python research/examples/symphony_harmonic_null_comparison.py` for the Milestone H null comparison.
