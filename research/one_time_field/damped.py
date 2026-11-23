"""Rayleigh-damped Hamiltonian dynamics via symmetric operator splitting."""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite
from typing import Mapping, Sequence

from .hamiltonian import HamiltonianFieldSystem


@dataclass
class DampedHamiltonianFieldSystem(HamiltonianFieldSystem):
    """Hamiltonian field system with diagonal linear Rayleigh friction.

    For each coordinate block a:
        q_dot = p / m
        p_dot = -dV/dq - gamma_a * p

    The continuous energy balance is dH/dt = -sum_a gamma_a*||p_a||^2/m_a <= 0.
    A symmetric split step applies exact half-step momentum damping, one
    conservative velocity-Verlet step, then exact half-step damping. The
    splitting is second order, but discrete total energy need not decrease
    at every step because the conservative Verlet substep has bounded
    integration error.
    """

    scalar_damping: float = 0.2
    phase_damping: float = 0.2
    tensor_damping: float = 0.2

    def __post_init__(self) -> None:
        super().__post_init__()
        for name in ("scalar_damping", "phase_damping", "tensor_damping"):
            value = float(getattr(self, name))
            if not isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
            setattr(self, name, value)

    def _damping(self, domain: str) -> float:
        return {
            "scalar": self.scalar_damping,
            "phases": self.phase_damping,
            "tensor": self.tensor_damping,
        }[domain]

    def _damp_momenta(self, factor_dt: float) -> None:
        for domain, values in self.momenta.items():
            factor = exp(-self._damping(domain) * factor_dt)
            if domain == "tensor":
                self.momenta[domain] = [
                    [factor * p for p in row] for row in values
                ]
            else:
                self.momenta[domain] = [factor * p for p in values]

    def step(self, dt: float) -> dict[str, dict]:
        """Advance one symmetric damping–Verlet–damping step."""
        if not isfinite(dt) or dt <= 0.0:
            raise ValueError("dt must be finite and positive")
        self._damp_momenta(0.5 * dt)
        super().step(dt)
        self._damp_momenta(0.5 * dt)
        return self.snapshot()
