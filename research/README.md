# GENESIS Research: One Time Field Foundation

This experimental research layer is separate from the legacy GENESIS 2.4 simulator. It does not alter the simulator's C sources or build system.

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
- one_time_field/variational.py — shared dimensionless potential functional and gradient flow.
- one_time_field/hamiltonian.py — canonical conservative dynamics using velocity-Verlet.
- one_time_field/damped.py — Rayleigh-damped Hamiltonian dynamics using symmetric damping/Verlet operator splitting.
- one_time_field/temporal.py — parameter, relational, and observer-time accumulators.\n- one_time_field/temporal_models.py — external, relational, entropy-production, event, observer, and hybrid clock hypotheses.\n- docs/TEMPORAL_COMPARISON.md — assumptions, chain-rule reparameterization, and boundaries for quantum-relational and causal-set extensions.\n- docs/TEMPORAL_ARCHITECTURE.md — temporal distinctions, assumptions, and falsifiable next steps.
- tests/ — invariant, validation, extension, variational, Hamiltonian, damping, convergence, and temporal tests.
- examples/temporal_clock_demo.py — demonstrates separate temporal layers.\n- examples/temporal_models_demo.py — compares distinct clock readings side by side.\n- examples/dynamics_comparison_demo.py — same-initial-state comparison of three dynamics regimes.
- examples/dynamics_convergence_study.py — analytic-reference timestep study with state errors, energy drift, and damping-balance residuals.\n- examples/coupled_network_regimes.py — three-node scalar/phase/tensor-array network comparison across gradient, Hamiltonian, and damped dynamics.

## Run
Requires Python 3.10 or newer.

    python -m unittest discover -s research/tests -v
    python research/examples/two_node_demo.py
    python research/examples/dimensional_engine_demo.py
    python research/examples/variational_demo.py
    python research/examples/hamiltonian_demo.py
    python research/examples/dynamics_comparison_demo.py
    python research/examples/dynamics_convergence_study.py\n    python research/examples/coupled_network_regimes.py
    python research/examples/temporal_clock_demo.py\n    python research/examples/temporal_models_demo.py\n
## Scientific discipline
These are mathematical experiments, not validated physical field theories. The tensor prototype does not define geometric tensor transformation laws. The shared potential is a selected dimensionless functional, not established physical energy. The damping coefficients and inertias are model parameters, not measured constants. Numerical behavior validates the specified equations and integrator only; it does not establish a physical mechanism or a unique unified field equation.
