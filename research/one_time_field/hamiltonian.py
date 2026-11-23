"""Finite-dimensional Hamiltonian dynamics using the shared OTFT potential."""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, pi
from typing import Mapping, Sequence

from .variational import VariationalFieldSystem


@dataclass
class HamiltonianFieldSystem:
    """Canonical conservative dynamics with a separable, diagonal kinetic term.

    The supplied VariationalFieldSystem provides U(q)=V(q) and its gradients.
    This class interprets that dimensionless functional as a potential energy
    in the chosen normalized units. It does not add physical units or prove
    that the functional is a physical energy.

    A velocity-Verlet step is symplectic for this separable Hamiltonian:
        H(q,p) = sum_a p_a**2/(2*m_a) + V(q).

    Natural-frequency forcing from the gradient-flow prototype is deliberately
    excluded: canonical dynamics require all forces to come from the stated
    Hamiltonian (or be represented by an explicit time-dependent Hamiltonian).
    """

    potential_system: VariationalFieldSystem
    scalar_inertia: float = 1.0
    phase_inertia: float = 1.0
    tensor_inertia: float = 1.0
    momenta: Mapping[str, Sequence] | None = None

    def __post_init__(self) -> None:
        if any(self.potential_system.natural_frequencies):
            raise ValueError("Hamiltonian system does not accept natural-frequency drive")
        for name in ("scalar_inertia", "phase_inertia", "tensor_inertia"):
            value = float(getattr(self, name))
            if not isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and strictly positive")
            setattr(self, name, value)
        expected = self.potential_system.snapshot()
        if self.momenta is None:
            self.momenta = {
                key: ([[0.0 for _ in row] for row in value] if key == "tensor" else [0.0] * len(value))
                for key, value in expected.items()
            }
        else:
            self.momenta = {
                key: ([[float(v) for v in row] for row in value] if key == "tensor" else [float(v) for v in value])
                for key, value in self.momenta.items()
            }
            if set(self.momenta) != set(expected):
                raise ValueError("momenta domains must match present state domains")
            for key, value in expected.items():
                p = self.momenta[key]
                if key == "tensor":
                    if len(p) != len(value) or any(len(a) != len(b) for a, b in zip(p, value)):
                        raise ValueError("tensor momenta must match tensor state shape")
                    if not all(isfinite(v) for row in p for v in row):
                        raise ValueError("momenta must be finite")
                else:
                    if len(p) != len(value) or not all(isfinite(v) for v in p):
                        raise ValueError(f"{key} momenta must match state shape and be finite")

    def _inertia(self, domain: str) -> float:
        return {
            "scalar": self.scalar_inertia,
            "phases": self.phase_inertia,
            "tensor": self.tensor_inertia,
        }[domain]

    def kinetic_energy(self) -> float:
        total = 0.0
        for domain, values in self.momenta.items():
            inertia = self._inertia(domain)
            if domain == "tensor":
                total += sum(p*p for row in values for p in row) / (2.0 * inertia)
            else:
                total += sum(p*p for p in values) / (2.0 * inertia)
        return total

    def energy(self) -> float:
        """Return dimensionless total Hamiltonian H=K+V."""
        return self.kinetic_energy() + self.potential_system.potential()

    def snapshot(self) -> dict[str, dict]:
        """Return detached generalized coordinates and canonical momenta."""
        return {
            "coordinates": self.potential_system.snapshot(),
            "momenta": {
                key: ([list(row) for row in value] if key == "tensor" else list(value))
                for key, value in self.momenta.items()
            },
        }

    def step(self, dt: float) -> dict[str, dict]:
        """Advance one symplectic velocity-Verlet step for positive dt."""
        if not isfinite(dt) or dt <= 0.0:
            raise ValueError("dt must be finite and positive")
        system = self.potential_system
        grad0 = system.gradients()
        half = {}
        for domain, p_values in self.momenta.items():
            inertia = self._inertia(domain)
            if domain == "tensor":
                half[domain] = [
                    [p - 0.5*dt*g for p, g in zip(prow, grow)]
                    for prow, grow in zip(p_values, grad0[domain])
                ]
                system.tensor = [
                    [q + dt*p/inertia for q, p in zip(qrow, prow)]
                    for qrow, prow in zip(system.tensor, half[domain])
                ]
            else:
                half[domain] = [p - 0.5*dt*g for p, g in zip(p_values, grad0[domain])]
                updated = [q + dt*p/inertia for q, p in zip(getattr(system, domain), half[domain])]
                if domain == "phases":
                    updated = [q % (2.0*pi) for q in updated]
                setattr(system, domain, updated)
        grad1 = system.gradients()
        for domain, p_half in half.items():
            if domain == "tensor":
                self.momenta[domain] = [
                    [p - 0.5*dt*g for p, g in zip(prow, grow)]
                    for prow, grow in zip(p_half, grad1[domain])
                ]
            else:
                self.momenta[domain] = [
                    p - 0.5*dt*g for p, g in zip(p_half, grad1[domain])
                ]
        return self.snapshot()

