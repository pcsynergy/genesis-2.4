"""Milestone D: topology and frequency-dispersion robustness sweep.

Run from the repository root:
    python research/examples/symphony_harmonic_robustness.py

The experiment probes a Kuramoto-style phase network. It is not a model of
cosmological creation, consciousness, or a new fundamental interaction.
"""
from pathlib import Path
import sys
from math import pi

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field import PhaseOscillatorNetwork


def graph(kind, n):
    matrix = [[0.0] * n for _ in range(n)]
    if kind == "complete":
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j] = matrix[j][i] = 1.0
    elif kind == "ring":
        for i in range(n):
            j = (i + 1) % n
            matrix[i][j] = matrix[j][i] = 1.0
    elif kind == "path":
        for i in range(n - 1):
            matrix[i][i + 1] = matrix[i + 1][i] = 1.0
    else:
        raise ValueError("kind must be complete, ring, or path")
    return matrix


def scenario(topology, dispersion, coupling, steps=5000, dt=0.01):
    n = 10
    phases = [0.0, 0.2, 0.8, 1.7, 2.1, 3.4, 4.8, 5.5, 5.9, 3.0]
    slope = {"equal": 0.0, "moderate": 0.02, "high": 0.15}[dispersion]
    frequencies = [1.0 + slope * (i - (n - 1) / 2.0) for i in range(n)]
    model = PhaseOscillatorNetwork(
        adjacency=graph(topology, n),
        phases=phases,
        natural_frequencies=frequencies,
        coupling=coupling,
    )
    initial = model.order_parameter()
    model.run(steps, dt)
    return initial, model.order_parameter()


def main():
    print("topology,frequency_dispersion,coupling,initial_R,final_R")
    for topology in ("complete", "path", "ring"):
        for dispersion in ("equal", "moderate", "high"):
            for coupling in (0.5, 1.0, 2.0):
                initial, final = scenario(topology, dispersion, coupling)
                print(f"{topology},{dispersion},{coupling:.1f},{initial:.6f},{final:.6f}")


if __name__ == "__main__":
    main()
