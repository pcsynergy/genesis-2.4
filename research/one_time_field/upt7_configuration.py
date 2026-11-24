"""UPT-7 finite configuration-space and relational actualization prototype.

The finite binary model is a statistical-mechanics-style toy model, not a
claim that ontological Potential is literally a binary physical field.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import exp, isfinite
from typing import Sequence


@dataclass(frozen=True)
class UPTConfigurationEnsemble:
    """Enumerate admissible binary configurations and relational weights.

    Admissibility is fixed Hamming weight: exactly active_count of n variables
    are 1. The relational energy penalizes disagreement across graph edges:
        E(q) = (J/2) sum_(i<j) W_ij (q_i-q_j)^2.
    A Boltzmann-like actualization distribution is proportional to exp(-beta E).
    This is a finite probability model, not a fundamental law.
    """

    adjacency: Sequence[Sequence[float]]
    active_count: int
    coupling: float = 1.0
    beta: float = 1.0

    def __post_init__(self) -> None:
        matrix = tuple(tuple(float(v) for v in row) for row in self.adjacency)
        n = len(matrix)
        if n < 2 or any(len(row) != n for row in matrix):
            raise ValueError("adjacency must be square with at least two nodes")
        if not all(isfinite(v) and v >= 0.0 for row in matrix for v in row):
            raise ValueError("edge weights must be finite and nonnegative")
        for i in range(n):
            if abs(matrix[i][i]) > 1e-12:
                raise ValueError("self-edges are not supported")
            for j in range(n):
                if abs(matrix[i][j] - matrix[j][i]) > 1e-12:
                    raise ValueError("adjacency must be symmetric")
        if not isinstance(self.active_count, int) or not 0 <= self.active_count <= n:
            raise ValueError("active_count must be an integer between zero and node count")
        if not isfinite(self.coupling) or self.coupling < 0.0:
            raise ValueError("coupling must be finite and nonnegative")
        if not isfinite(self.beta) or self.beta < 0.0:
            raise ValueError("beta must be finite and nonnegative")
        object.__setattr__(self, "adjacency", matrix)
        object.__setattr__(self, "coupling", float(self.coupling))
        object.__setattr__(self, "beta", float(self.beta))

    @property
    def node_count(self) -> int:
        return len(self.adjacency)

    @property
    def admissible_states(self) -> tuple[tuple[int, ...], ...]:
        return tuple(
            state for state in product((0, 1), repeat=self.node_count)
            if sum(state) == self.active_count
        )

    def relational_energy(self, state: Sequence[int]) -> float:
        q = self._validate_state(state)
        cut = sum(
            self.adjacency[i][j] * (q[i] - q[j]) ** 2
            for i in range(self.node_count) for j in range(i + 1, self.node_count)
        )
        return 0.5 * self.coupling * cut

    def _validate_state(self, state: Sequence[int]) -> tuple[int, ...]:
        q = tuple(state)
        if len(q) != self.node_count or any(type(v) is not int or v not in (0, 1) for v in q):
            raise ValueError("state must contain one binary integer per node")
        if sum(q) != self.active_count:
            raise ValueError("state is outside the admissible fixed-count domain")
        return q

    def distribution(self) -> tuple[tuple[tuple[int, ...], float], ...]:
        states = self.admissible_states
        weights = [exp(-self.beta * self.relational_energy(q)) for q in states]
        partition = sum(weights)
        return tuple((q, w / partition) for q, w in zip(states, weights))

    def expected_cut(self) -> float:
        return sum(
            probability * sum(
                self.adjacency[i][j] * (q[i] - q[j]) ** 2
                for i in range(self.node_count) for j in range(i + 1, self.node_count)
            )
            for q, probability in self.distribution()
        )

    def expected_coherence(self) -> float:
        total_weight = sum(
            self.adjacency[i][j]
            for i in range(self.node_count) for j in range(i + 1, self.node_count)
        )
        if total_weight == 0.0:
            return 1.0
        return 1.0 - self.expected_cut() / total_weight

    def observable_summary(self) -> dict[str, float]:
        return {
            "admissible_state_count": float(len(self.admissible_states)),
            "partition_function": sum(
                exp(-self.beta * self.relational_energy(q))
                for q in self.admissible_states
            ),
            "expected_cut": self.expected_cut(),
            "expected_coherence": self.expected_coherence(),
        }
