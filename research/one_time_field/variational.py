"""Variational prototype: a shared potential for heterogeneous field states.

States are dimensionless, normalized coordinates. The functional is a
mathematical experiment, not a physical energy until scales, units, and
observables are supplied by a specific model.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import cos, isfinite, pi, sin
from typing import Sequence


@dataclass
class VariationalFieldSystem:
    """Gradient-flow system for scalar, phase, and tensor-array states.

    Potential:
      V = 1/2*m_s*sum_i x_i^2
        + 1/2*m_t*sum_i,a T[i,a]^2
        + 1/2*sum_{i<j} W_ij * (
              g_s*(x_i-x_j)^2
            + g_t*||T_i-T_j||^2
            + 2*g_h*(1-cos(theta_i-theta_j))
            + lambda*(x_i-x_j)^2*(1-cos(theta_i-theta_j))
          )

    Each state follows its own gradient flow with its own positive mobility.
    Optional natural phase frequencies are external drives; nonzero drive
    means V need not decrease monotonically.
    """

    adjacency: Sequence[Sequence[float]]
    scalar: Sequence[float] | None = None
    phases: Sequence[float] | None = None
    tensor: Sequence[Sequence[float]] | None = None
    scalar_gradient: float = 1.0
    phase_gradient: float = 1.0
    tensor_gradient: float = 1.0
    scalar_mass: float = 0.0
    tensor_mass: float = 0.0
    scalar_phase_coupling: float = 0.0
    scalar_mobility: float = 1.0
    phase_mobility: float = 1.0
    tensor_mobility: float = 1.0
    natural_frequencies: Sequence[float] | None = None

    def __post_init__(self) -> None:
        self.adjacency = tuple(tuple(float(v) for v in row) for row in self.adjacency)
        n = len(self.adjacency)
        if n == 0 or any(len(row) != n for row in self.adjacency):
            raise ValueError("adjacency must be a nonempty square matrix")
        if not all(isfinite(v) for row in self.adjacency for v in row):
            raise ValueError("adjacency values must be finite")
        if any(v < 0.0 for row in self.adjacency for v in row):
            raise ValueError("edge weights must be nonnegative")
        for i in range(n):
            if abs(self.adjacency[i][i]) > 1e-12:
                raise ValueError("self-edges are not supported")
            for j in range(n):
                if abs(self.adjacency[i][j] - self.adjacency[j][i]) > 1e-12:
                    raise ValueError("adjacency must be symmetric")

        self.scalar = None if self.scalar is None else [float(v) for v in self.scalar]
        self.phases = None if self.phases is None else [float(v) for v in self.phases]
        self.tensor = None if self.tensor is None else [
            [float(v) for v in row] for row in self.tensor
        ]
        if self.scalar is None and self.phases is None and self.tensor is None:
            raise ValueError("at least one state domain is required")
        for name, values in (("scalar", self.scalar), ("phases", self.phases)):
            if values is not None and (len(values) != n or not all(isfinite(v) for v in values)):
                raise ValueError(f"{name} must contain one finite value per graph node")
        if self.tensor is not None:
            if len(self.tensor) != n or not self.tensor:
                raise ValueError("tensor state must contain one row per graph node")
            width = len(self.tensor[0])
            if width == 0 or any(len(row) != width for row in self.tensor):
                raise ValueError("tensor state must have a consistent nonzero component count")
            if not all(isfinite(v) for row in self.tensor for v in row):
                raise ValueError("tensor values must be finite")

        coefficients = (
            "scalar_gradient", "phase_gradient", "tensor_gradient",
            "scalar_mass", "tensor_mass", "scalar_phase_coupling",
            "scalar_mobility", "phase_mobility", "tensor_mobility",
        )
        for name in coefficients:
            value = getattr(self, name)
            if not isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
            setattr(self, name, float(value))
        if min(self.scalar_mobility, self.phase_mobility, self.tensor_mobility) <= 0.0:
            raise ValueError("mobilities must be strictly positive")

        if self.natural_frequencies is None:
            self.natural_frequencies = [0.0] * n
        else:
            self.natural_frequencies = [float(v) for v in self.natural_frequencies]
            if len(self.natural_frequencies) != n or not all(
                isfinite(v) for v in self.natural_frequencies
            ):
                raise ValueError("natural_frequencies must contain one finite value per node")
        if self.phases is None and any(self.natural_frequencies):
            raise ValueError("natural frequencies require a phase state")

    @property
    def node_count(self) -> int:
        return len(self.adjacency)

    def potential(self) -> float:
        """Evaluate the shared dimensionless potential functional."""
        value = 0.0
        if self.scalar is not None:
            value += 0.5 * self.scalar_mass * sum(x*x for x in self.scalar)
        if self.tensor is not None:
            value += 0.5 * self.tensor_mass * sum(
                x*x for row in self.tensor for x in row
            )
        for i in range(self.node_count):
            for j in range(i + 1, self.node_count):
                weight = self.adjacency[i][j]
                if weight == 0.0:
                    continue
                phase_factor = (
                    1.0 - cos(self.phases[i] - self.phases[j])
                    if self.phases is not None else 0.0
                )
                if self.scalar is not None:
                    dx = self.scalar[i] - self.scalar[j]
                    value += 0.5 * weight * self.scalar_gradient * dx*dx
                    if self.phases is not None:
                        value += 0.5 * weight * self.scalar_phase_coupling * dx*dx * phase_factor
                if self.tensor is not None:
                    dt = sum((a-b)**2 for a, b in zip(self.tensor[i], self.tensor[j]))
                    value += 0.5 * weight * self.tensor_gradient * dt
                if self.phases is not None:
                    value += weight * self.phase_gradient * phase_factor
        return value

    def gradients(self) -> dict[str, list]:
        """Return partial derivatives of V with respect to each present state."""
        result: dict[str, list] = {}
        if self.scalar is not None:
            grad = [self.scalar_mass*x for x in self.scalar]
            for i in range(self.node_count):
                for j in range(self.node_count):
                    if i == j:
                        continue
                    phase_factor = (
                        1.0 - cos(self.phases[i] - self.phases[j])
                        if self.phases is not None else 0.0
                    )
                    coefficient = self.scalar_gradient + self.scalar_phase_coupling * phase_factor
                    grad[i] += self.adjacency[i][j] * coefficient * (self.scalar[i] - self.scalar[j])
            result["scalar"] = grad

        if self.tensor is not None:
            grad = [[self.tensor_mass*x for x in row] for row in self.tensor]
            for i in range(self.node_count):
                for j in range(self.node_count):
                    if i == j:
                        continue
                    for k in range(len(self.tensor[i])):
                        grad[i][k] += (
                            self.adjacency[i][j] * self.tensor_gradient
                            * (self.tensor[i][k] - self.tensor[j][k])
                        )
            result["tensor"] = grad

        if self.phases is not None:
            grad = [0.0] * self.node_count
            for i in range(self.node_count):
                for j in range(self.node_count):
                    if i == j:
                        continue
                    delta = self.phases[i] - self.phases[j]
                    coefficient = self.phase_gradient
                    if self.scalar is not None:
                        dx = self.scalar[i] - self.scalar[j]
                        coefficient += 0.5 * self.scalar_phase_coupling * dx*dx
                    grad[i] += self.adjacency[i][j] * coefficient * sin(delta)
            result["phases"] = grad
        return result

    def step(self, dt: float) -> dict[str, list]:
        """Advance all domains with simultaneous explicit gradient-flow updates."""
        if not isfinite(dt) or dt <= 0.0:
            raise ValueError("dt must be finite and positive")
        grad = self.gradients()
        if self.scalar is not None:
            self.scalar = [
                x - dt*self.scalar_mobility*g
                for x, g in zip(self.scalar, grad["scalar"])
            ]
        if self.tensor is not None:
            self.tensor = [
                [x - dt*self.tensor_mobility*g for x, g in zip(row, grow)]
                for row, grow in zip(self.tensor, grad["tensor"])
            ]
        if self.phases is not None:
            self.phases = [
                (theta + dt*(omega - self.phase_mobility*g)) % (2*pi)
                for theta, omega, g in zip(
                    self.phases, self.natural_frequencies, grad["phases"]
                )
            ]
        return self.snapshot()

    def snapshot(self) -> dict[str, list]:
        """Return a detached copy of all present state domains."""
        state = {}
        if self.scalar is not None:
            state["scalar"] = list(self.scalar)
        if self.phases is not None:
            state["phases"] = list(self.phases)
        if self.tensor is not None:
            state["tensor"] = [list(row) for row in self.tensor]
        return state
