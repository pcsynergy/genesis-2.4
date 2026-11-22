# GENESIS Research: One Time Field Foundation

This is an experimental research layer, kept separate from the legacy GENESIS 2.4 simulator. It does not alter the simulator's C sources, build system, or scientific behavior.

## First milestone

A graph of interacting field states: each node has a scalar state phi_i(t), edges encode pairwise coupling, local decay and external sources are explicit, and numerical evolution is deterministic.

The first implementation is a graph-coupled scalar-field toy model. It is a mathematical sandbox, not a validated physical field theory and not evidence for One Time Field Theory.

## Specifications

- [Architecture](docs/ARCHITECTURE.md) — component boundaries, data flow, testing, and future simulator interoperability.
- [Foundation](docs/FOUNDATION.md) — definitions, assumptions, equations, and initial validation plan.
- [Formal specification](docs/FORMAL_SPECIFICATION.md) — baseline axioms, governing dynamics, boundary conditions, derived properties, and testable predictions.

## Layout

- one_time_field/network.py — dependency-free reference implementation.
- tests/test_network.py — unit tests.
- examples/two_node_demo.py — runnable example.

## Run

Requires Python 3.10 or newer.

    python -m unittest discover -s research/tests -v
    python research/examples/two_node_demo.py

## Scientific discipline

State units and meanings must be specified before physical interpretation. Distinguish established mathematics, modeling assumptions, and speculative interpretation. Numerical patterns are not proof of a physical mechanism.
