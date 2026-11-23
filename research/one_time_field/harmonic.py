"""Phase-coupled oscillator model for exploratory harmonic experiments."""
from __future__ import annotations
from dataclasses import dataclass
from math import cos, isfinite, pi, sin
from typing import Sequence

@dataclass
class PhaseOscillatorNetwork:
    """Kuramoto-style phases: theta_dot_i = omega_i + K*sum(W_ij*sin(theta_j-theta_i))/degree_i."""
    adjacency: Sequence[Sequence[float]]
    phases: Sequence[float]
    natural_frequencies: Sequence[float]
    coupling: float = 1.0

    def __post_init__(self):
        self.adjacency = tuple(tuple(float(x) for x in row) for row in self.adjacency)
        self.phases = [float(x) for x in self.phases]
        self.natural_frequencies = [float(x) for x in self.natural_frequencies]
        n = len(self.phases)
        if n == 0:
            raise ValueError("network must contain at least one oscillator")
        if len(self.adjacency) != n or any(len(row) != n for row in self.adjacency):
            raise ValueError("adjacency matrix must be square and match phase length")
        if len(self.natural_frequencies) != n:
            raise ValueError("one natural frequency is required per oscillator")
        values = self.phases + self.natural_frequencies + [x for row in self.adjacency for x in row]
        if not all(isfinite(x) for x in values):
            raise ValueError("phases, frequencies, and weights must be finite")
        if any(x < 0 for row in self.adjacency for x in row):
            raise ValueError("edge weights must be nonnegative")
        if any(abs(self.adjacency[i][i]) > 1e-12 for i in range(n)):
            raise ValueError("self-edges are not supported")
        for i in range(n):
            for j in range(n):
                if abs(self.adjacency[i][j] - self.adjacency[j][i]) > 1e-12:
                    raise ValueError("adjacency matrix must be symmetric")
        if not isfinite(self.coupling) or self.coupling < 0:
            raise ValueError("coupling must be finite and nonnegative")
        self.coupling = float(self.coupling)

    @property
    def node_count(self):
        return len(self.phases)

    def derivative(self):
        result = []
        for i in range(self.node_count):
            degree = sum(self.adjacency[i])
            interaction = 0.0 if degree == 0 else sum(
                self.adjacency[i][j] * sin(self.phases[j] - self.phases[i])
                for j in range(self.node_count)
            ) / degree
            result.append(self.natural_frequencies[i] + self.coupling * interaction)
        return result

    def step(self, dt):
        if not isfinite(dt) or dt <= 0:
            raise ValueError("dt must be finite and positive")
        velocities = self.derivative()
        self.phases = [(p + dt * v) % (2 * pi) for p, v in zip(self.phases, velocities)]
        return list(self.phases)

    def run(self, steps, dt):
        if not isinstance(steps, int) or steps < 0:
            raise ValueError("steps must be a nonnegative integer")
        history = [list(self.phases)]
        for _ in range(steps):
            history.append(self.step(dt))
        return history

    def order_parameter(self):
        x = sum(cos(p) for p in self.phases) / self.node_count
        y = sum(sin(p) for p in self.phases) / self.node_count
        return (x*x + y*y) ** 0.5
