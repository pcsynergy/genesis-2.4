"""UPT-9 reversible adaptive-potential dynamics with explicit memory."""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from math import exp, isfinite
from typing import Sequence


@dataclass(frozen=True)
class UPTMemoryDynamics:
    adjacency: Sequence[Sequence[float]]
    coupling: float = 1.0
    memory_strength: float = 1.0
    beta: float = 1.0
    attempt_rate: float = 1.0

    def __post_init__(self):
        matrix = tuple(tuple(float(v) for v in row) for row in self.adjacency)
        n = len(matrix)
        if n < 2 or any(len(row) != n for row in matrix):
            raise ValueError("adjacency must be square with at least two nodes")
        if not all(isfinite(v) and v >= 0 for row in matrix for v in row):
            raise ValueError("edge weights must be finite and nonnegative")
        for i in range(n):
            if abs(matrix[i][i]) > 1e-12:
                raise ValueError("self-edges are not supported")
            for j in range(n):
                if abs(matrix[i][j] - matrix[j][i]) > 1e-12:
                    raise ValueError("adjacency must be symmetric")
        for name, value in (("coupling", self.coupling),
                            ("memory_strength", self.memory_strength),
                            ("beta", self.beta)):
            if not isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if not isfinite(self.attempt_rate) or self.attempt_rate <= 0:
            raise ValueError("attempt_rate must be finite and positive")
        object.__setattr__(self, "adjacency", matrix)

    @property
    def node_count(self):
        return len(self.adjacency)

    @property
    def states(self):
        return tuple((q, m) for q in product((0, 1), repeat=self.node_count)
                     for m in range(self.node_count + 1))

    def _validate_state(self, state):
        try:
            q, memory = state
            q = tuple(q)
        except (TypeError, ValueError):
            raise ValueError("state must be a (configuration, memory) pair")
        if len(q) != self.node_count or any(type(v) is not int or v not in (0, 1) for v in q):
            raise ValueError("configuration must contain binary integers")
        if type(memory) is not int or not 0 <= memory <= self.node_count:
            raise ValueError("memory must be an integer between zero and node count")
        return q, memory

    def energy(self, state):
        q, memory = self._validate_state(state)
        cut = sum(self.adjacency[i][j] * (q[i] - q[j]) ** 2
                  for i in range(self.node_count) for j in range(i + 1, self.node_count))
        return 0.5 * self.coupling * cut + 0.5 * self.memory_strength * (sum(q) - memory) ** 2

    def transition_rate(self, source, target):
        source, target = self._validate_state(source), self._validate_state(target)
        q0, m0 = source
        q1, m1 = target
        distance = sum(a != b for a, b in zip(q0, q1)) + abs(m0 - m1)
        if distance != 1:
            return 0.0
        delta = self.energy(target) - self.energy(source)
        return self.attempt_rate * exp(-self.beta * max(0.0, delta))

    def generator(self):
        states = self.states
        result = []
        for i, source in enumerate(states):
            row = [self.transition_rate(source, target) if i != j else 0.0
                   for j, target in enumerate(states)]
            row[i] = -sum(row)
            result.append(tuple(row))
        return tuple(result)

    def stationary_distribution(self):
        weights = [exp(-self.beta * self.energy(state)) for state in self.states]
        z = sum(weights)
        return tuple(w / z for w in weights)

    def detailed_balance_residual(self):
        states, pi = self.states, self.stationary_distribution()
        return max((abs(pi[i] * self.transition_rate(states[i], states[j])
                        - pi[j] * self.transition_rate(states[j], states[i]))
                    for i in range(len(states)) for j in range(len(states)) if i != j),
                   default=0.0)

    def evolve_uniformized(self, probability, duration, steps):
        """Stable explicit CTMC evolution with stochastic Euler substeps."""
        if not isfinite(duration) or duration < 0:
            raise ValueError("duration must be finite and nonnegative")
        if not isinstance(steps, int) or steps < 1:
            raise ValueError("steps must be a positive integer")
        p = tuple(float(v) for v in probability)
        n = len(self.states)
        if len(p) != n or any(not isfinite(v) or v < 0 for v in p):
            raise ValueError("probability must be a nonnegative vector over all states")
        if abs(sum(p) - 1.0) > 1e-10:
            raise ValueError("initial probability must sum to one")
        if duration == 0:
            return p
        qmat = self.generator()
        exit_bound = max(-qmat[i][i] for i in range(n))
        if exit_bound == 0:
            return p
        substeps = max(1, int(exit_bound * duration / steps) + 1)
        dt = duration / (steps * substeps)
        transition = tuple(tuple((1.0 if i == j else 0.0) + dt * qmat[i][j]
                                 for j in range(n)) for i in range(n))
        for _ in range(steps * substeps):
            p = tuple(sum(p[i] * transition[i][j] for i in range(n))
                      for j in range(n))
        return p

    def active_count_domain(self, memory, tolerance=1):
        if type(memory) is not int or not 0 <= memory <= self.node_count:
            raise ValueError("memory must be between zero and node count")
        if type(tolerance) is not int or tolerance < 0:
            raise ValueError("tolerance must be a nonnegative integer")
        return tuple(q for q in product((0, 1), repeat=self.node_count)
                     if abs(sum(q) - memory) <= tolerance)
