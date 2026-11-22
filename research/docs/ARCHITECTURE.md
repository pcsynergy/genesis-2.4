# GENESIS Research Architecture — Draft 0.5

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
      shared-topology dimensional engine
      variational common-potential prototype
      numerical experiments and validation
      future visualization

The arrow is a future integration possibility, not an implemented connection.

## 3. Current package structure

    research/
      README.md
      docs/
        ARCHITECTURE.md
        DIMENSIONAL_ANALYSIS.md
        ACTION_PRINCIPLE.md
        EXTENSIONS.md
        FOUNDATION.md
        FORMAL_SPECIFICATION.md
      one_time_field/
        __init__.py
        network.py
        harmonic.py
        tensor.py
        engine.py
        variational.py
      examples/
        two_node_demo.py
      tests/
        test_network.py
        test_extensions.py
        test_engine.py
        test_variational.py

## 4. Responsibilities

- docs/: normative model definitions, assumptions, limitations, and change history.
- network.py: scalar graph diffusion with decay and source.
- harmonic.py: nonlinear phase synchronization.
- tensor.py: component-wise graph diffusion for fixed-shape arrays.
- engine.py: composition of present state domains on one shared graph and explicitly declared cross-domain mappings.
- variational.py: a shared dimensionless potential functional with mobility-weighted gradient flow for scalar, phase, and tensor-array states.
- examples/: runnable demonstrations.
- tests/: invariant, validation, regression, and numerical convergence tests.

Keep mathematical specifications independent of implementation details. Implementations are judged against specifications, not the reverse.

## 5. Dimensional engine semantics

Every present submodel must use exactly the same weighted adjacency matrix. The engine advances each domain with its own governing equation. It does not flatten unlike states into one vector or pretend that phase, scalar, and tensor components have identical units.

Two optional cross-domain mappings are currently defined:

1. Scalar mean to phase-frequency offset:
       omega_i,eff = omega_i + g_sf * mean(phi)
2. Phase coherence to scalar source:
       s_i,eff = s_i,base + g_fs * R

Here R is the phase order parameter. The gains g_sf and g_fs are user-defined dimensional conversion parameters. Their units must be selected for the intended model; no physical values are assumed.

All cross-domain signals are calculated from the pre-step snapshot. Each present submodel is then advanced once with explicit Euler. This is a simultaneous explicit update, not a continuous-time coupled solver. The tensor domain currently shares topology but has no cross-domain forcing term.

## 6. Current data flow

1. User supplies a graph, initial domain states, parameters, and optional cross-domain gains.
2. Each submodel validates its own dimensions and parameter domains.
3. The engine verifies that all present domains share the same graph.
4. Cross-domain signals are computed from a common pre-step snapshot.
5. Scalar, phase, and tensor models advance under their own equations.
6. The engine returns a detached state snapshot and can record a history.
7. Tests compare behavior with invariants and analytic expectations.

No external datasets, network calls, or GENESIS runtime state are required.

## 7. Variational potential layer

The variational prototype is separate from the modular dimensional engine. It defines one dimensionless functional over the currently implemented scalar, phase, and tensor-array coordinates. Each domain follows its own mobility-weighted negative gradient. Relative phase modulates scalar and tensor graph penalties, while scalar and tensor differences feed back into the phase gradient. Natural-frequency forcing is an external drive and removes the guarantee of monotonic potential decrease.

This is a chosen model functional, not a derived physical law. Reference scales and units are required before interpreting it as physical energy. Tensor components still lack geometric transformation laws.

## 8. Numerical responsibilities

Document solver order, time-step restrictions, convergence behavior, floating-point assumptions, reproducibility, and failure modes. Future solver options should be compared against analytic solutions or trusted numerical references. Explicit Euler stability must be investigated for each coupled configuration.

## 9. Testing strategy

- Unit tests: dimensions, parameter domains, deterministic stepping.
- Invariant tests: mean conservation and dissipation in applicable limits.
- Analytic tests: uncoupled decay against the exponential solution.
- Convergence tests: compare solutions at dt and dt/2.
- Harmonic tests: identical-phase invariance, phase-difference relaxation, and phase coherence.
- Tensor-array tests: component-wise evolution and conservation.
- Engine tests: shared topology, detached snapshots, explicit cross-domain influence, and validation of incompatible graphs.

Passing software tests validates only the tested implementation behavior, not a physical interpretation.

## 10. Future GENESIS interoperability

Do not couple research code directly to private simulator internals. If integration becomes useful, define a versioned interchange format and adapter with explicit units and metadata, stable identifiers, declared sampling interval, missing-data behavior, and round-trip compatibility tests.

The first adapter should be read-only and offline. Any simulator modifications require separate review and regression testing.

## 11. Development stages

- Stage A: formal scalar network baseline.
- Stage B: stronger numerical validation and time-dependent forcing.
- Stage C: phase oscillator and harmonic extensions.
- Stage D: tensor-array generalizations and, later, proper geometric tensor definitions.
- Stage E: shared-topology dimensional composition and explicit cross-domain couplings.
- Stage F: physical mapping and comparison to established theories.
- Stage G: optional GENESIS data adapter and visualization.
