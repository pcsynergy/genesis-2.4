"""Milestone G: Jacobian spectra for synchronized and twisted states."""
from pathlib import Path
import sys
from math import cos, pi
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.symphony_stability import (
    phase_jacobian, symmetric_eigenvalues, classify_transverse_stability,
)

N = 10
K = 1.0


def complete_graph(n):
    return [[0.0 if i == j else 1.0 for j in range(n)] for i in range(n)]


def ring_graph(n):
    a = [[0.0] * n for _ in range(n)]
    for i in range(n):
        j = (i + 1) % n
        a[i][j] = a[j][i] = 1.0
    return a


def main():
    print("state,largest_eigenvalue,smallest_eigenvalue,transverse_classification")
    cases = [
        ("complete_synchronized", [0.0] * N, complete_graph(N)),
        ("ring_q1_twist", [2*pi*i/N for i in range(N)], ring_graph(N)),
        ("ring_q2_twist", [4*pi*i/N for i in range(N)], ring_graph(N)),
    ]
    for name, phases, adjacency in cases:
        eig = symmetric_eigenvalues(phase_jacobian(phases, adjacency, K))
        print(f"{name},{max(eig):.10f},{min(eig):.10f},{classify_transverse_stability(eig)}")


if __name__ == "__main__":
    main()
