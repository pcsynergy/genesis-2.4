# GENESIS Research Architecture — Draft 0.3

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
      scalar, phase, and tensor-array reference models
      numerical experiments and validation
      future visualization

The arrow is a future integration possibility, not an implemented connection.

## 3. Current package structure

    research/
      README.md
      docs/
        ARCHITECTURE.md
        EXTENSIONS.md
        FOUNDATION.md
        FORMAL_SPECIFICATION.md
      one_time_field/
        __init__.py
        network.py
        harmonic.py
        tensor.py
      examples/
        two_node_demo.py
      tests/
        test_network.py
        test_extensions.py

## 4. Responsibilities

- docs/: normative model definitions, assumptions, limitations, and change history.
- one_time_field/: small reference implementations with minimal dependencies.
- examples/: runnable demonstrations.
- tests/: invariant, validation, regression, and numerical convergence tests.

Keep mathematical specifications independent of implementation details. Implementations are judged against specifications, not the reverse.

## 5. Current data flow

1. User supplies graph, initial states, parameters, and optional scalar source.
2. Each model validates dimensions and parameter domains.
3. Derivative methods evaluate the governing right-hand side.
4. Step methods advance state using explicit Euler.
5. Run methods return state histories.
6. Tests compare behavior with invariants and analytic expectations.

No external datasets, network calls, or GENESIS runtime state are required.

## 6. Numerical responsibilities

Document solver order, time-step restrictions, convergence behavior, floating-point assumptions, reproducibility, and failure modes. Future solver options should be compared against analytic solutions or trusted numerical references.

## 7. Testing strategy

- Unit tests: dimensions, parameter domains, deterministic stepping.
- Invariant tests: mean conservation and dissipation in applicable limits.
- Analytic tests: uncoupled decay against the exponential solution.
- Convergence tests: compare solutions at dt and dt/2.
- Harmonic tests: identical-phase invariance, phase-difference relaxation, and phase coherence.
- Tensor-array tests: component-wise evolution and conservation.

Passing software tests validates only the tested implementation behavior, not a physical interpretation.

## 8. Future GENESIS interoperability

Do not couple research code directly to private simulator internals. If integration becomes useful, define a versioned interchange format and adapter with explicit units and metadata, stable identifiers, declared sampling interval, missing-data behavior, and round-trip compatibility tests.

The first adapter should be read-only and offline. Any simulator modifications require separate review and regression testing.

## 9. Development stages

- Stage A: formal scalar network baseline.
- Stage B: stronger numerical validation and time-dependent forcing.
- Stage C: phase oscillator and harmonic extensions.
- Stage D: tensor-array generalizations and, later, proper geometric tensor definitions.
- Stage E: physical mapping and comparison to established theories.
- Stage F: optional GENESIS data adapter and visualization.
