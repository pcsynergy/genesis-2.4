# GENESIS Research Architecture — Draft 0.2

## 1. Architectural goal

Develop experimental mathematical models alongside GENESIS 2.4 without destabilizing or silently changing the established neural simulator.

The research layer is an adjacent Python package. It is not a replacement for GENESIS, does not patch its C simulation engine, and does not currently exchange runtime state with GENESIS.

## 2. Layer boundaries

    GENESIS 2.4 (existing)
      C simulation core, neural elements, solvers, XODUS/PGENESIS
                   |
                   | future, explicit file/API adapter only
                   v
    GENESIS Research (experimental)
      mathematical specifications
      reference models
      numerical experiments
      validation and visualization

The arrow is a future integration possibility, not an implemented connection.

## 3. Current package structure

    research/
      README.md
      docs/
        ARCHITECTURE.md
        FOUNDATION.md
        FORMAL_SPECIFICATION.md
      one_time_field/
        __init__.py
        network.py
      examples/
        two_node_demo.py
      tests/
        test_network.py

## 4. Responsibilities

- docs/: normative model definitions, assumptions, limitations, and change history.
- one_time_field/: small reference implementations with minimal dependencies.
- examples/: runnable demonstrations that show expected use.
- tests/: invariant, validation, regression, and numerical convergence tests.

Keep the mathematical specification independent of implementation details. The implementation should be judged against the specification, not the reverse.

## 5. Data flow

For the current prototype:

1. User supplies graph adjacency, initial node state, coupling, and decay.
2. The model validates dimensions and parameter domains.
3. The derivative function evaluates the right-hand side.
4. The step function advances the state with explicit Euler.
5. The run function returns a state history.
6. Tests compare results with invariants and known analytic cases.

No external datasets, network calls, or GENESIS runtime state are required.

## 6. Numerical responsibilities

The model must document:
- solver and integration order;
- time-step restrictions and convergence behavior;
- floating-point assumptions;
- reproducibility expectations;
- known failure modes.

Future solver options should be added behind a stable interface and compared against analytic solutions or trusted numerical references.

## 7. Testing strategy

- Unit tests: dimensions, parameter domains, and deterministic stepping.
- Invariant tests: mean conservation and dissipation in applicable limits.
- Analytic tests: uncoupled decay against the exponential solution.
- Convergence tests: compare solutions at dt, dt/2, and dt/4.
- Regression tests: retain small, fixed examples with known outputs.

A passing unit test suite validates only the tested software behavior. It does not validate a physical interpretation.

## 8. Future GENESIS interoperability

Do not couple research code directly to private simulator internals. If integration becomes useful, define a versioned interchange format and adapter with:
- explicit units and metadata;
- stable element/node identifiers;
- declared sampling interval;
- documented missing-data behavior;
- round-trip and compatibility tests.

The first adapter should be read-only and offline. Any simulator modifications require separate review and regression testing.

## 9. Development stages

- Stage A: formal scalar network baseline.
- Stage B: stronger numerical validation and time-dependent forcing.
- Stage C: oscillator and harmonic extensions.
- Stage D: tensor/network generalizations where justified.
- Stage E: physical mapping and comparison to established theories.
- Stage F: optional GENESIS data adapter and visualization.

No later stage should be treated as evidence for an earlier physical claim.
