"""UPT-10: finite-dimensional Onsager gradient flow for relational fields and memory.

This is a dissipative variational prototype, not a conservative Euler-Lagrange
model and not a derivation of the UPT-9 Metropolis jump rates.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence


@dataclass(frozen=True)
class UPTActionPrinciple:
    adjacency: Sequence[Sequence[float]]
    relational_strength: float = 1.0
    memory_strength: float = 1.0
    bistable_strength: float = 1.0
    field_mobility: float = 1.0
    memory_mobility: float = 1.0

    def __post_init__(self):
        w = tuple(tuple(float(v) for v in row) for row in self.adjacency)
        n = len(w)
        if n < 2 or any(len(row) != n for row in w):
            raise ValueError("adjacency must be square with at least two sites")
        if any(not isfinite(v) or v < 0 for row in w for v in row):
            raise ValueError("weights must be finite and nonnegative")
        for i in range(n):
            if abs(w[i][i]) > 1e-12:
                raise ValueError("self-edges are not supported")
            for j in range(n):
                if abs(w[i][j] - w[j][i]) > 1e-12:
                    raise ValueError("adjacency must be symmetric")
        for name in ("relational_strength", "memory_strength",
                     "bistable_strength", "field_mobility", "memory_mobility"):
            value = getattr(self, name)
            if not isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if self.field_mobility == 0 and self.memory_mobility == 0:
            raise ValueError("at least one mobility must be positive")
        object.__setattr__(self, "adjacency", w)

    @property
    def size(self):
        return len(self.adjacency)

    def _state(self, field, memory):
        phi = tuple(float(v) for v in field)
        m = float(memory)
        if len(phi) != self.size or any(not isfinite(v) for v in phi) or not isfinite(m):
            raise ValueError("field must be finite and match lattice size; memory must be finite")
        return phi, m

    def energy(self, field, memory):
        phi, m = self._state(field, memory)
        graph = sum(self.adjacency[i][j] * (phi[i] - phi[j]) ** 2
                    for i in range(self.size) for j in range(i + 1, self.size))
        mismatch = sum(phi) - m
        wells = sum(v * v * (1.0 - v) ** 2 for v in phi)
        return (0.5 * self.relational_strength * graph
                + 0.5 * self.memory_strength * mismatch ** 2
                + 0.25 * self.bistable_strength * wells)

    def gradient(self, field, memory):
        phi, m = self._state(field, memory)
        mismatch = sum(phi) - m
        grad = []
        for i, value in enumerate(phi):
            graph_grad = self.relational_strength * sum(
                self.adjacency[i][j] * (value - phi[j])
                for j in range(self.size) if j != i)
            well_grad = 0.5 * self.bistable_strength * value * (1.0 - value) * (1.0 - 2.0 * value)
            grad.append(graph_grad + self.memory_strength * mismatch + well_grad)
        memory_grad = -self.memory_strength * mismatch
        return tuple(grad), memory_grad

    def rhs(self, field, memory):
        grad_phi, grad_m = self.gradient(field, memory)
        return (tuple(-self.field_mobility * v for v in grad_phi),
                -self.memory_mobility * grad_m)

    def dissipation_rate(self, field, memory):
        grad_phi, grad_m = self.gradient(field, memory)
        return (self.field_mobility * sum(v * v for v in grad_phi)
                + self.memory_mobility * grad_m * grad_m)

    def energy_rate(self, field, memory):
        dphi, dm = self.rhs(field, memory)
        grad_phi, grad_m = self.gradient(field, memory)
        return sum(a * b for a, b in zip(grad_phi, dphi)) + grad_m * dm

    def step(self, field, memory, dt, max_backtracks=30):
        """Energy-decreasing explicit step with backtracking line search."""
        phi, m = self._state(field, memory)
        if not isfinite(dt) or dt <= 0:
            raise ValueError("dt must be finite and positive")
        dphi, dm = self.rhs(phi, m)
        old_energy = self.energy(phi, m)
        trial_dt = dt
        for _ in range(max_backtracks + 1):
            candidate_phi = tuple(x + trial_dt * dx for x, dx in zip(phi, dphi))
            candidate_m = m + trial_dt * dm
            candidate_energy = self.energy(candidate_phi, candidate_m)
            if candidate_energy <= old_energy + 1e-13:
                return candidate_phi, candidate_m, trial_dt
            trial_dt *= 0.5
        raise RuntimeError("line search failed to find a non-increasing energy step")
