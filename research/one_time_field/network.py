"""Graph-coupled scalar-field toy model, independent of legacy GENESIS."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence


@dataclass
class GraphFieldNetwork:
    """Evolve scalar node states on a weighted, undirected graph.

    d(phi_i)/dt = -decay*phi_i
                  + coupling*sum_j W[i][j]*(phi_j - phi_i)
                  + source_i

    This is a generic diffusion-with-decay model, not a validated physical
    field theory. Explicit forward-Euler integration is used.
    """

    adjacency: Sequence[Sequence[float]]
    state: Sequence[float]
    coupling: float = 1.0
    decay: float = 0.0

    def __post_init__(self) -> None:
        self.adjacency = tuple(tuple(float(x) for x in row) for row in self.adjacency)
        self.state = [float(x) for x in self.state]
        n = len(self.state)
        if n == 0:
            raise ValueError("network must contain at least one node")
        if len(self.adjacency) != n or any(len(row) != n for row in self.adjacency):
            raise ValueError("adjacency matrix must be square and match state length")
        if not self._finite(self.state) or not all(
            isfinite(x) for row in self.adjacency for x in row
        ):
            raise ValueError("state and adjacency values must be finite")
        if any(x < 0.0 for row in self.adjacency for x in row):
            raise ValueError("edge weights must be nonnegative")
        if any(abs(self.adjacency[i][i]) > 1e-12 for i in range(n)):
            raise ValueError("self-edges are not supported")
        for i in range(n):
            for j in range(n):
                if abs(self.adjacency[i][j] - self.adjacency[j][i]) > 1e-12:
                    raise ValueError("adjacency matrix must be symmetric")
        self._validate_parameter("coupling", self.coupling)
        self._validate_parameter("decay", self.decay)
        self.coupling = float(self.coupling)
        self.decay = float(self.decay)

    @staticmethod
    def _finite(values: Sequence[float]) -> bool:
        return all(isfinite(x) for x in values)

    @staticmethod
    def _validate_parameter(name: str, value: float) -> None:
        if not isfinite(value) or value < 0.0:
            raise ValueError(f"{name} must be finite and nonnegative")

    @property
    def node_count(self) -> int:
        return len(self.state)

    def derivative(self, source: Sequence[float] | None = None) -> list[float]:
        """Return d(state)/dt; source defaults to zero at every node."""
        n = self.node_count
        forcing = [0.0] * n if source is None else [float(x) for x in source]
        if len(forcing) != n or not self._finite(forcing):
            raise ValueError("source must contain one finite value per node")
        result = []
        for i in range(n):
            interaction = sum(
                self.adjacency[i][j] * (self.state[j] - self.state[i])
                for j in range(n)
            )
            result.append(
                -self.decay * self.state[i] + self.coupling * interaction + forcing[i]
            )
        return result

    def step(self, dt: float, source: Sequence[float] | None = None) -> list[float]:
        """Advance one explicit-Euler step and return a copy of the new state."""
        if not isfinite(dt) or dt <= 0.0:
            raise ValueError("dt must be finite and positive")
        slope = self.derivative(source)
        self.state = [x + dt * dx for x, dx in zip(self.state, slope)]
        return list(self.state)

    def run(
        self, steps: int, dt: float, source: Sequence[float] | None = None
    ) -> list[list[float]]:
        """Run a fixed source for steps and return the complete state history."""
        if not isinstance(steps, int) or steps < 0:
            raise ValueError("steps must be a nonnegative integer")
        history = [list(self.state)]
        for _ in range(steps):
            history.append(self.step(dt, source))
        return history

    def mean_state(self) -> float:
        """Return the arithmetic mean of node states."""
        return sum(self.state) / self.node_count
