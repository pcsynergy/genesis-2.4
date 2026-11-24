"""UPT-8 adaptive admissible configuration space prototype.

The model expands an initially constrained binary state space when a
previously inactive node receives sufficient support from active neighbors.
This is a finite graph toy model, not a claim of ontological creation.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import exp, isfinite
from typing import Sequence


@dataclass(frozen=True)
class UPTAdaptivePotentialSpace:
    """Finite binary network with interaction-driven domain renewal.

    Initial admissibility is fixed Hamming weight. A renewal round admits any
    one-bit activation q_i: 0 -> 1 for which the weighted active-neighbor
    support sum_j W_ij q_j reaches activation_threshold.

    The rule is monotone: states are added but never removed. It is
    intentionally explicit and finite, so closure and irreversibility can be
    tested. Coupling and beta govern a Gibbs-like distribution over the
    currently admissible domain; they do not determine the renewal rule.
    """

    adjacency: Sequence[Sequence[float]]
    initial_active_count: int
    activation_threshold: float = 1.0
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
        if (not isinstance(self.initial_active_count, int)
                or not 0 <= self.initial_active_count <= n):
            raise ValueError("initial_active_count must be an integer between zero and node count")
        if not isfinite(self.activation_threshold) or self.activation_threshold <= 0.0:
            raise ValueError("activation_threshold must be finite and positive")
        if not isfinite(self.coupling) or self.coupling < 0.0:
            raise ValueError("coupling must be finite and nonnegative")
        if not isfinite(self.beta) or self.beta < 0.0:
            raise ValueError("beta must be finite and nonnegative")
        object.__setattr__(self, "adjacency", matrix)
        object.__setattr__(self, "activation_threshold", float(self.activation_threshold))
        object.__setattr__(self, "coupling", float(self.coupling))
        object.__setattr__(self, "beta", float(self.beta))

    @property
    def node_count(self) -> int:
        return len(self.adjacency)

    @property
    def ambient_states(self) -> tuple[tuple[int, ...], ...]:
        return tuple(product((0, 1), repeat=self.node_count))

    @property
    def initial_domain(self) -> tuple[tuple[int, ...], ...]:
        return tuple(q for q in self.ambient_states
                     if sum(q) == self.initial_active_count)

    def neighbor_support(self, state: Sequence[int], node: int) -> float:
        q = self._validate_binary_state(state)
        if not isinstance(node, int) or not 0 <= node < self.node_count:
            raise ValueError("node index is outside the network")
        return sum(self.adjacency[node][j] * q[j] for j in range(self.node_count))

    def renewal_step(
        self, domain: Sequence[Sequence[int]]
    ) -> tuple[tuple[int, ...], ...]:
        """Return the domain after one synchronous activation/renewal round."""
        current = {self._validate_binary_state(q) for q in domain}
        if not current:
            raise ValueError("domain must contain at least one state")
        expanded = set(current)
        for q in current:
            for i, value in enumerate(q):
                if value == 0 and self.neighbor_support(q, i) >= self.activation_threshold:
                    candidate = list(q)
                    candidate[i] = 1
                    expanded.add(tuple(candidate))
        return tuple(sorted(expanded))

    def domain_history(self, rounds: int) -> tuple[tuple[tuple[int, ...], ...], ...]:
        if not isinstance(rounds, int) or rounds < 0:
            raise ValueError("rounds must be a nonnegative integer")
        history = [self.initial_domain]
        for _ in range(rounds):
            previous = history[-1]
            next_domain = self.renewal_step(previous)
            history.append(next_domain)
            if next_domain == previous:
                break
        return tuple(history)

    def relational_energy(self, state: Sequence[int]) -> float:
        q = self._validate_binary_state(state)
        cut = sum(
            self.adjacency[i][j] * (q[i] - q[j]) ** 2
            for i in range(self.node_count) for j in range(i + 1, self.node_count)
        )
        return 0.5 * self.coupling * cut

    def distribution(
        self, domain: Sequence[Sequence[int]]
    ) -> tuple[tuple[tuple[int, ...], float], ...]:
        states = tuple(sorted({self._validate_binary_state(q) for q in domain}))
        if not states:
            raise ValueError("domain must contain at least one state")
        weights = [exp(-self.beta * self.relational_energy(q)) for q in states]
        partition = sum(weights)
        return tuple((q, weight / partition) for q, weight in zip(states, weights))

    def expected_coherence(self, domain: Sequence[Sequence[int]]) -> float:
        total_weight = sum(
            self.adjacency[i][j]
            for i in range(self.node_count) for j in range(i + 1, self.node_count)
        )
        if total_weight == 0.0:
            return 1.0
        return sum(
            probability * (
                1.0 - 2.0 * self.relational_energy(q) / self.coupling / total_weight
                if self.coupling > 0.0 else
                1.0 - sum(
                    self.adjacency[i][j] * (q[i] - q[j]) ** 2
                    for i in range(self.node_count) for j in range(i + 1, self.node_count)
                ) / total_weight
            )
            for q, probability in self.distribution(domain)
        )

    def _validate_binary_state(self, state: Sequence[int]) -> tuple[int, ...]:
        q = tuple(state)
        if len(q) != self.node_count or any(type(v) is not int or v not in (0, 1) for v in q):
            raise ValueError("state must contain one binary integer per node")
        return q
