"""Milestone C: compare phase coherence across coupling strengths.

Run from the repository root:
    python research/examples/symphony_harmonic_creation.py

This is a Kuramoto-style oscillator-network experiment, not a cosmological
creation model or evidence that symbolic sequence maps to physical law.
"""
from pathlib import Path
import sys
from math import pi

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field import PhaseOscillatorNetwork


def complete_graph(n):
    return [[0.0 if i == j else 1.0 for j in range(n)] for i in range(n)]


def run_case(coupling, steps=3000, dt=0.01):
    n = 8
    phases = [2.0 * pi * i / n for i in range(n)]
    frequencies = [1.0 + 0.03 * (i - (n - 1) / 2.0) for i in range(n)]
    model = PhaseOscillatorNetwork(
        adjacency=complete_graph(n),
        phases=phases,
        natural_frequencies=frequencies,
        coupling=coupling,
    )
    initial_order = model.order_parameter()
    history = model.run(steps, dt)
    final_order = model.order_parameter()
    final_rates = model.derivative()
    mean_rate = sum(final_rates) / n
    rate_spread = (sum((x - mean_rate) ** 2 for x in final_rates) / n) ** 0.5
    return initial_order, final_order, rate_spread, history


def main():
    print("coupling,initial_coherence,final_coherence,final_rate_spread")
    for coupling in (0.0, 0.5, 1.0, 2.0):
        initial, final, spread, _ = run_case(coupling)
        print(f"{coupling:.2f},{initial:.6f},{final:.6f},{spread:.6f}")


if __name__ == "__main__":
    main()
