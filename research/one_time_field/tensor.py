"""Component-wise tensor-state extension of the graph diffusion baseline.

This prototype diffuses corresponding flattened components independently.
It does not define tensor transformation laws, spacetime indices, covariant
derivatives, or geometry.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite, prod
from typing import Sequence

@dataclass
class TensorFieldNetwork:
    """Evolve same-shaped tensor arrays over a weighted undirected graph."""
    adjacency: Sequence[Sequence[float]]
    state: Sequence[Sequence[float]]
    tensor_shape: Sequence[int]
    coupling: float = 1.0
    decay: float = 0.0

    def __post_init__(self):
        self.adjacency = tuple(tuple(float(x) for x in row) for row in self.adjacency)
        self.state = [[float(x) for x in row] for row in self.state]
        self.tensor_shape = tuple(int(x) for x in self.tensor_shape)
        n = len(self.state)
        if n == 0:
            raise ValueError("network must contain at least one node")
        if not self.tensor_shape or any(d <= 0 for d in self.tensor_shape):
            raise ValueError("tensor_shape must contain positive dimensions")
        if any(len(row) != prod(self.tensor_shape) for row in self.state):
            raise ValueError("each node state must match tensor_shape component count")
        if len(self.adjacency) != n or any(len(row) != n for row in self.adjacency):
            raise ValueError("adjacency matrix must be square and match node count")
        values = [x for row in self.state for x in row] + [x for row in self.adjacency for x in row]
        if not all(isfinite(x) for x in values):
            raise ValueError("state and adjacency values must be finite")
        if any(x < 0 for row in self.adjacency for x in row):
            raise ValueError("edge weights must be nonnegative")
        if any(abs(self.adjacency[i][i]) > 1e-12 for i in range(n)):
            raise ValueError("self-edges are not supported")
        for i in range(n):
            for j in range(n):
                if abs(self.adjacency[i][j] - self.adjacency[j][i]) > 1e-12:
                    raise ValueError("adjacency matrix must be symmetric")
        for name, value in (("coupling", self.coupling), ("decay", self.decay)):
            if not isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and nonnegative")
        self.coupling, self.decay = float(self.coupling), float(self.decay)

    @property
    def node_count(self):
        return len(self.state)

    @property
    def component_count(self):
        return prod(self.tensor_shape)

    def derivative(self):
        result = []
        for i in range(self.node_count):
            rates = []
            for k in range(self.component_count):
                interaction = sum(
                    self.adjacency[i][j] * (self.state[j][k] - self.state[i][k])
                    for j in range(self.node_count)
                )
                rates.append(-self.decay * self.state[i][k] + self.coupling * interaction)
            result.append(rates)
        return result

    def step(self, dt):
        if not isfinite(dt) or dt <= 0:
            raise ValueError("dt must be finite and positive")
        rates = self.derivative()
        self.state = [[x + dt * dx for x, dx in zip(row, rate)]
                      for row, rate in zip(self.state, rates)]
        return [list(row) for row in self.state]

    def run(self, steps, dt):
        if not isinstance(steps, int) or steps < 0:
            raise ValueError("steps must be a nonnegative integer")
        history = [[list(row) for row in self.state]]
        for _ in range(steps):
            history.append(self.step(dt))
        return history
