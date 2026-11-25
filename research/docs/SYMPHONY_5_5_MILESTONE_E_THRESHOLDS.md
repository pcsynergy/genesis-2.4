# Symphony 5.5 / UPT — Milestone E: Multi-start thresholds and local/global coherence

**Status:** implemented; CI validation follows the commit  
**Runner:** `research/examples/symphony_harmonic_thresholds.py`  
**Tests:** `research/tests/test_symphony_thresholds.py`

## Question

How sensitive are apparent synchronization outcomes to initial phase configuration, coupling strength, frequency dispersion, and graph topology? Can a global order parameter conceal local neighbor alignment?

## Protocol

The experiment uses the existing normalized Kuramoto-style network with ten oscillators. It evaluates three graph topologies (complete, path, ring), four linear frequency-dispersion slopes (0, 0.05, 0.10, 0.15), eight coupling strengths (0.25 through 2.00 in increments of 0.25), and four explicitly specified initial phase vectors. Each case is integrated with explicit Euler, step size 0.01, for 3,000 steps. The total grid contains 384 deterministic runs.

Two observables are recorded:

- Global coherence: (R=|N^{-1}\sum_j e^{i\theta_j}|).
- Local edge alignment: (Q_{edge}=(1+\langle\cos(\theta_j-\theta_i)\rangle_{(i,j)\in E})/2), which maps mean neighbor cosine to [0,1].

The second quantity is a local edge statistic, not a substitute for the global order parameter. Neither quantity is a physical measurement.

## Interpretation and reporting discipline

The sweep is a finite parameter grid, not a mathematically exact critical-coupling calculation. Any apparent threshold is conditional on topology, the chosen frequency distribution, initial conditions, integration duration, and numerical method. Report ranges or observed transitions only for the sampled grid; do not extrapolate them into a universal critical value.

The ring test explicitly illustrates why global phase coherence and local neighbor alignment should be reported separately: a spatially twisted phase arrangement can have a small global vector sum while neighboring phases remain similarly offset. Local alignment is not identical to phase locking or long-range synchronization.

## Limitations

This remains a phenomenological phase-oscillator toy model. It does not contain spacetime, gravity, quantum fields, biological neural dynamics, or a derived UPT interaction. The experiment can test internal mathematical behavior and robustness of this model; it cannot validate One Time Field Theory as a physical theory.
