# Symphony 5.5 / UPT — Milestone D: Topology and Robustness

**Status:** implemented as a deterministic parameter sweep  
**Runner:** `research/examples/symphony_harmonic_robustness.py`  
**Tests:** `research/tests/test_symphony_robustness.py`

## Research question

Does the synchronization observed in Milestone C persist when the interaction graph and natural-frequency distribution change?

## Design

The same normalized Kuramoto-style dynamics are tested on three undirected, unweighted graph topologies with ten oscillators:

- **Complete graph:** every oscillator interacts with every other oscillator.
- **Path graph:** each interior oscillator interacts with its two neighbors; endpoints have one neighbor.
- **Ring graph:** each oscillator interacts with its two periodic neighbors.

The initial phase configuration is fixed across all cases:
`[0.0, 0.2, 0.8, 1.7, 2.1, 3.4, 4.8, 5.5, 5.9, 3.0]`.

Natural frequencies are linear across the node index:
[
\omega_i=1+s(i-4.5),
]
with dispersion slope \(s=0\) (equal), \(0.02\) (moderate), or \(0.15\) (high). Coupling strengths are \(K=0.5,1,2\). Each case uses explicit Euler updates with \(\Delta t=0.01\) for 5,000 steps. The observable is the global Kuramoto order parameter \(R\).

## Selected outcomes

The following rounded values are from the specified deterministic run:

| Topology | Dispersion | K=0.5 | K=1.0 | K=2.0 |
|---|---|---:|---:|---:|
| Complete | Equal | 1.0000 | 1.0000 | 1.0000 |
| Complete | Moderate | 0.9946 | 0.9987 | 0.9997 |
| Complete | High | 0.3824 | 0.8966 | 0.9801 |
| Path | Equal | 0.8902 | 0.9944 | 1.0000 |
| Path | Moderate | 0.2377 | 0.5548 | 0.8961 |
| Path | High | 0.2242 | 0.3699 | 0.2617 |
| Ring | Equal | 0.0058 | 0.0001 | 0.0000 |
| Ring | Moderate | 0.3655 | 0.1970 | 0.1015 |
| Ring | High | 0.3053 | 0.1939 | 0.2380 |

These are global coherence values for this initial condition and finite integration time. They are not universal phase diagrams or empirical measurements.

## Findings

1. **Topology matters.** The complete graph synchronizes readily in these cases; the path graph needs stronger coupling under moderate dispersion.
2. **Frequency dispersion matters.** In the complete graph, increasing the dispersion requires stronger coupling to reach high global coherence.
3. **Global coherence is not the same as local coordination.** The ring can retain a twisted phase pattern with low global \(R\), even though each node interacts with neighbors. A low order parameter therefore does not prove that all local relations are incoherent.
4. **Coupling does not guarantee monotonic improvement in every finite run.** The path/high-dispersion row shows that increasing \(K\) from 1 to 2 does not improve the final global order parameter for this setup.

## Scientific interpretation

Milestone C showed synchronization for one complete-graph configuration. Milestone D qualifies that result: coherence depends on topology, heterogeneity, initial phases, and integration duration. The mathematical claim is limited to the stated model and reproducible setup.

The musical analogy remains useful as an interpretation of coordinated parts, but the model does not explain cosmic creation, consciousness, biological development, or a new fundamental field. It is not Lorentz-covariant and contains no spacetime metric or gravitational dynamics.

## Next checks

- Repeat with several initial phase configurations rather than one fixed vector.
- Refine the time step and compare a higher-order integrator.
- Track local edge phase differences alongside global \(R\).
- Estimate synchronization boundaries over a denser grid of \((K,s)\).
