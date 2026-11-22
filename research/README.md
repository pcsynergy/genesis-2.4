# GENESIS Research: One Time Field Foundation

This experimental research layer is separate from the legacy GENESIS 2.4 simulator. It does not alter the simulator's C sources or build system.

## Specifications
- [Architecture](docs/ARCHITECTURE.md)
- [Foundation](docs/FOUNDATION.md)
- [Formal specification](docs/FORMAL_SPECIFICATION.md)
- [Extensions](docs/EXTENSIONS.md) — conservation, harmonic oscillators, tensor-array states, and the shared-topology dimensional engine.

## Implemented models
- one_time_field/network.py — scalar graph diffusion with decay and external source.
- one_time_field/harmonic.py — Kuramoto-style phase-coupled oscillator network.
- one_time_field/tensor.py — component-wise tensor-array graph diffusion prototype.
- one_time_field/engine.py — dimensional engine composing the models on one shared graph with two explicit cross-domain coupling rules.
- tests/ — invariant, validation, extension, and mixed-domain engine tests.
- examples/two_node_demo.py — runnable scalar example.

## Run
Requires Python 3.10 or newer.

    python -m unittest discover -s research/tests -v
    python research/examples/two_node_demo.py
    python research/examples/dimensional_engine_demo.py

## Scientific discipline
These are mathematical experiments, not validated physical field theories. The tensor prototype does not define geometric tensor transformation laws. The dimensional engine is a software composition of distinct equations, not a derivation of a single fundamental field equation. Cross-domain gains are user-defined modeling parameters, not measured physical constants. Numerical patterns are not proof of a physical mechanism.
