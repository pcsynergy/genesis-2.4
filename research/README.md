# GENESIS Research: One Time Field Foundation

This experimental research layer is separate from the legacy GENESIS 2.4 simulator. It does not alter the simulator's C sources or build system.

## Specifications
- [Architecture](docs/ARCHITECTURE.md)
- [Foundation](docs/FOUNDATION.md)
- [Formal specification](docs/FORMAL_SPECIFICATION.md)
- [Extensions](docs/EXTENSIONS.md) — conservation, harmonic oscillators, tensor-array states, the shared-topology dimensional engine, and a variational common-potential prototype.
- [Dimensional analysis and symmetry](docs/DIMENSIONAL_ANALYSIS.md) — reference scales, mobility units, and conditional conservation results.

## Implemented models
- one_time_field/network.py — scalar graph diffusion with decay and external source.
- one_time_field/harmonic.py — Kuramoto-style phase-coupled oscillator network.
- one_time_field/tensor.py — component-wise tensor-array graph diffusion prototype.
- one_time_field/engine.py — dimensional engine composing the models on one shared graph with two explicit cross-domain coupling rules.
- one_time_field/variational.py — shared dimensionless potential functional coupling scalar, phase, and tensor-array states through gradient flow.
- tests/ — invariant, validation, extension, dimensional-engine, and variational-gradient tests.
- examples/two_node_demo.py — runnable scalar example.

## Run
Requires Python 3.10 or newer.

    python -m unittest discover -s research/tests -v
    python research/examples/two_node_demo.py
    python research/examples/dimensional_engine_demo.py
    python research/examples/variational_demo.py

## Scientific discipline
These are mathematical experiments, not validated physical field theories. The tensor prototype does not define geometric tensor transformation laws. The dimensional engine is a software composition of distinct equations. The variational prototype couples them through a chosen dimensionless functional, but does not derive a unique fundamental field equation. Cross-domain gains are user-defined modeling parameters, not measured physical constants. Numerical patterns are not proof of a physical mechanism.
