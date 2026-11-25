"""Milestone E: multi-start synchronization and local/global coherence sweep.

Run from the repository root:
    python research/examples/symphony_harmonic_thresholds.py

This is a finite Kuramoto-style numerical probe, not a physical field model.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field import PhaseOscillatorNetwork

N = 10
PHASE_SETS = (
    (0.0, 0.2, 0.8, 1.7, 2.1, 3.4, 4.8, 5.5, 5.9, 3.0),
    (0.1, 1.1, 2.2, 3.3, 4.4, 5.5, 0.6, 1.7, 2.8, 3.9),
    (0.0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6),
    (5.8, 0.1, 1.9, 4.2, 2.7, 0.7, 3.6, 5.0, 1.2, 2.3),
)
COUPLINGS = tuple(i / 4 for i in range(1, 9))
DISPERSIONS = (0.0, 0.05, 0.10, 0.15)
TOPOLOGIES = ("complete", "path", "ring")


def graph(kind, n=N):
    a = [[0.0] * n for _ in range(n)]
    if kind == "complete":
        for i in range(n):
            for j in range(i + 1, n):
                a[i][j] = a[j][i] = 1.0
    elif kind == "path":
        for i in range(n - 1):
            a[i][i + 1] = a[i + 1][i] = 1.0
    elif kind == "ring":
        for i in range(n):
            j = (i + 1) % n
            a[i][j] = a[j][i] = 1.0
    else:
        raise ValueError("unknown topology")
    return a


def local_edge_alignment(phases, adjacency):
    """Map mean edge cosine from [-1, 1] to a local alignment score [0, 1]."""
    values = [
        __import__("math").cos(phases[j] - phases[i])
        for i in range(len(phases))
        for j in range(i + 1, len(phases))
        if adjacency[i][j] > 0
    ]
    if not values:
        return 1.0
    return (1.0 + sum(values) / len(values)) / 2.0


def run_case(topology, dispersion, coupling, phases, steps=3000, dt=0.01):
    frequencies = [1.0 + dispersion * (i - (N - 1) / 2.0) for i in range(N)]
    adjacency = graph(topology)
    model = PhaseOscillatorNetwork(adjacency, phases, frequencies, coupling)
    model.run(steps, dt)
    return model.order_parameter(), local_edge_alignment(model.phases, adjacency)


def sweep():
    for topology in TOPOLOGIES:
        for dispersion in DISPERSIONS:
            for coupling in COUPLINGS:
                for start_id, phases in enumerate(PHASE_SETS):
                    global_r, local_q = run_case(topology, dispersion, coupling, phases)
                    yield topology, dispersion, coupling, start_id, global_r, local_q


def main():
    print("topology,dispersion,coupling,initial_set,global_R,local_edge_alignment")
    for row in sweep():
        print(f"{row[0]},{row[1]:.2f},{row[2]:.2f},{row[3]},{row[4]:.6f},{row[5]:.6f}")


if __name__ == "__main__":
    main()
