"""Experiment 5: an action-derived dynamical clock coupled to field states.

The model is a finite-dimensional, dimensionless Hamiltonian prototype.
It introduces a clock coordinate T with inertia and a harmonic restoring
potential, coupled to the scalar-field amplitude observable C(x)=1/2 sum x_i^2/(1+x_i^2).

U_aug(q,T) = V(q) + 1/2*kappa*T^2 - g*T*C(x)
The coupling is part of the potential, not an externally injected source.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, pi
from typing import Mapping, Sequence

from .hamiltonian import HamiltonianFieldSystem


@dataclass
class ClockCoupledHamiltonianSystem:
    """Canonical system derived from an augmented Lagrangian.

    L = K_fields + 1/2*I_clock*T_dot^2 - V(q)
        - 1/2*kappa*T^2 + g*T*C(x)

    with C(x)=1/2 sum_i x_i^2. The clock is a dynamical coordinate, not an
    externally prescribed time parameter. The selected coupling is a model
    ansatz; its parameters are dimensionless until scales are supplied.
    """

    field_system: HamiltonianFieldSystem
    clock_coordinate: float = 0.0
    clock_momentum: float = 0.0
    clock_inertia: float = 1.0
    clock_stiffness: float = 1.0
    coupling: float = 0.0

    def __post_init__(self) -> None:
        if self.field_system.potential_system.scalar is None:
            raise ValueError("clock coupling currently requires a scalar field")
        for name in ("clock_coordinate", "clock_momentum"):
            value = float(getattr(self, name))
            if not isfinite(value):
                raise ValueError(f"{name} must be finite")
            setattr(self, name, value)
        for name in ("clock_inertia", "clock_stiffness"):
            value = float(getattr(self, name))
            if not isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
            setattr(self, name, value)
        self.coupling = float(self.coupling)
        if not isfinite(self.coupling):
            raise ValueError("coupling must be finite")

    def clock_observable(self) -> float:
        """Return C(x)=1/2 ||x||^2, the scalar-field amplitude observable."""
        return 0.5 * sum((x*x)/(1.0 + x*x) for x in self.field_system.potential_system.scalar)

    def potential_energy(self) -> float:
        return (
            self.field_system.potential_system.potential()
            + 0.5 * self.clock_stiffness * self.clock_coordinate**2
            - self.coupling * self.clock_coordinate * self.clock_observable()
        )

    def kinetic_energy(self) -> float:
        return (
            self.field_system.kinetic_energy()
            + self.clock_momentum**2 / (2.0 * self.clock_inertia)
        )

    def energy(self) -> float:
        """Conserved autonomous Hamiltonian H=K+U_aug (up to integrator error)."""
        return self.kinetic_energy() + self.potential_energy()

    def lagrangian(self) -> float:
        """Evaluate L=K-U_aug for the current canonical state."""
        return self.kinetic_energy() - self.potential_energy()

    def _gradients(self) -> tuple[dict[str, list], float]:
        gradients = self.field_system.potential_system.gradients()
        scalar = self.field_system.potential_system.scalar
        gradients["scalar"] = [
            grad - self.coupling * self.clock_coordinate * x / ((1.0 + x*x) ** 2)
            for grad, x in zip(gradients["scalar"], scalar)
        ]
        clock_gradient = (
            self.clock_stiffness * self.clock_coordinate
            - self.coupling * self.clock_observable()
        )
        return gradients, clock_gradient

    def snapshot(self) -> dict:
        return {
            "fields": self.field_system.snapshot(),
            "field_momenta": self.field_system.snapshot()["momenta"],
            "clock_coordinate": self.clock_coordinate,
            "clock_momentum": self.clock_momentum,
            "energy": self.energy(),
        }

    def step(self, dt: float) -> dict:
        """Advance augmented canonical equations with velocity-Verlet."""
        if not isfinite(dt) or dt <= 0.0:
            raise ValueError("dt must be finite and positive")
        system = self.field_system
        gradients0, clock_grad0 = self._gradients()
        half_momenta = {}
        for domain, momenta in system.momenta.items():
            inertia = system._inertia(domain)
            if domain == "tensor":
                half_momenta[domain] = [
                    [p - 0.5*dt*g for p, g in zip(prow, grow)]
                    for prow, grow in zip(momenta, gradients0[domain])
                ]
                system.potential_system.tensor = [
                    [q + dt*p/inertia for q, p in zip(qrow, prow)]
                    for qrow, prow in zip(system.potential_system.tensor, half_momenta[domain])
                ]
            else:
                half_momenta[domain] = [
                    p - 0.5*dt*g for p, g in zip(momenta, gradients0[domain])
                ]
                values = [
                    q + dt*p/inertia
                    for q, p in zip(getattr(system.potential_system, domain), half_momenta[domain])
                ]
                if domain == "phases":
                    values = [q % (2.0*pi) for q in values]
                setattr(system.potential_system, domain, values)

        clock_half = self.clock_momentum - 0.5*dt*clock_grad0
        self.clock_coordinate += dt * clock_half / self.clock_inertia

        gradients1, clock_grad1 = self._gradients()
        for domain, momenta in half_momenta.items():
            if domain == "tensor":
                system.momenta[domain] = [
                    [p - 0.5*dt*g for p, g in zip(prow, grow)]
                    for prow, grow in zip(momenta, gradients1[domain])
                ]
            else:
                system.momenta[domain] = [
                    p - 0.5*dt*g for p, g in zip(momenta, gradients1[domain])
                ]
        self.clock_momentum = clock_half - 0.5*dt*clock_grad1
        if not isfinite(self.energy()):
            raise RuntimeError("non-finite state in clock-coupled Hamiltonian system")
        return self.snapshot()
