"""UPT-11: periodic 1-D continuum limit of relational-memory gradient flow.

Dimensionless finite-difference model. This is a convergence study, not a
physical calibration or a claim of a new field equation.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import cos, isfinite, pi, sin, sqrt
from typing import Sequence


@dataclass
class UPTContinuumLimit:
    node_count: int = 64
    length: float = 2.0 * pi
    relational_strength: float = 1.0
    memory_strength: float = 0.5
    bistable_strength: float = 0.2
    field_mobility: float = 1.0
    memory_mobility: float = 0.8
    memory: float = 0.25
    field: Sequence[float] | None = None

    def __post_init__(self):
        if not isinstance(self.node_count, int) or self.node_count < 8:
            raise ValueError("node_count must be an integer >= 8")
        if not isfinite(self.length) or self.length <= 0:
            raise ValueError("length must be finite and positive")
        for name in ("relational_strength", "memory_strength", "bistable_strength",
                     "field_mobility", "memory_mobility"):
            value = getattr(self, name)
            if not isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if self.field_mobility == 0 and self.memory_mobility == 0:
            raise ValueError("at least one mobility must be positive")
        if not isfinite(self.memory):
            raise ValueError("memory must be finite")
        self.dx = self.length / self.node_count
        if self.field is None:
            self.field = tuple(0.25 + 0.12*cos(2*pi*i/self.node_count)
                               + 0.04*sin(4*pi*i/self.node_count)
                               for i in range(self.node_count))
        else:
            self.field = tuple(float(v) for v in self.field)
        if len(self.field) != self.node_count or any(not isfinite(v) for v in self.field):
            raise ValueError("field must contain one finite value per grid point")
        self.time = 0.0

    def mean(self):
        return sum(self.field) / self.node_count

    def variance(self):
        mean = self.mean()
        return sum((v-mean)**2 for v in self.field) / self.node_count

    def observable(self):
        """Spatial mean and variance: simple model-level observables."""
        return {"mean_field": self.mean(), "field_variance": self.variance(),
                "memory": self.memory}

    def energy(self):
        phi = self.field
        gradient = sum(((phi[(i+1) % self.node_count] - phi[i]) / self.dx)**2
                       for i in range(self.node_count))
        wells = sum(v*v*(1-v)*(1-v) for v in phi)
        mismatch = self.mean() - self.memory
        return (0.5*self.relational_strength*self.dx*gradient
                + 0.25*self.bistable_strength*self.dx*wells
                + 0.5*self.memory_strength*self.length*mismatch*mismatch)

    def gradient(self):
        phi, n = self.field, self.node_count
        mismatch = self.mean() - self.memory
        result = []
        for i, value in enumerate(phi):
            laplacian = (phi[(i+1) % n] - 2*value + phi[(i-1) % n])/(self.dx*self.dx)
            well = 0.5*self.bistable_strength*value*(1-value)*(1-2*value)
            result.append(-self.relational_strength*laplacian + well
                          + self.memory_strength*mismatch)
        memory_gradient = -self.memory_strength*self.length*mismatch
        return tuple(result), memory_gradient

    def rhs(self):
        grad, grad_memory = self.gradient()
        return (tuple(-self.field_mobility*v for v in grad),
                -self.memory_mobility*grad_memory/self.length)

    def energy_rate(self):
        grad, grad_memory = self.gradient()
        return (-self.field_mobility*self.dx*sum(v*v for v in grad)
                -self.memory_mobility*grad_memory*grad_memory/self.length)

    def step(self, dt):
        if not isfinite(dt) or dt <= 0:
            raise ValueError("dt must be finite and positive")
        old_energy = self.energy()
        dfield, dmemory = self.rhs()
        trial = dt
        for _ in range(32):
            candidate = tuple(v + trial*dv for v, dv in zip(self.field, dfield))
            candidate_memory = self.memory + trial*dmemory
            self.field, self.memory = candidate, candidate_memory
            new_energy = self.energy()
            if new_energy <= old_energy + 1e-13:
                self.time += trial
                return trial
            self.field = tuple(v - trial*dv for v, dv in zip(candidate, dfield))
            self.memory = candidate_memory - trial*dmemory
            trial *= 0.5
        raise RuntimeError("energy-decreasing step not found")

    def evolve(self, final_time, cfl=0.12):
        if not isfinite(final_time) or final_time < self.time:
            raise ValueError("final_time must be finite and >= current time")
        if not isfinite(cfl) or cfl <= 0:
            raise ValueError("cfl must be finite and positive")
        accepted = 0
        rejected_dt = 0
        base_dt = cfl*self.dx*self.dx/max(self.field_mobility*self.relational_strength, 1e-12)
        while self.time < final_time - 1e-15:
            dt = min(base_dt, final_time-self.time)
            used = self.step(dt)
            accepted += 1
            if used < dt*(1-1e-12):
                rejected_dt += 1
        return {"steps": accepted, "backtracked_steps": rejected_dt,
                "final_time": self.time, "energy": self.energy(),
                **self.observable()}


def interpolate_periodic(values, x):
    n = len(values)
    u = (x % 1.0)*n
    i = int(u)
    fraction = u-i
    return values[i % n]*(1-fraction) + values[(i+1) % n]*fraction


def continuum_refinement(final_time=0.02, counts=(16, 32, 64, 128), cfl=0.12):
    runs = []
    for n in counts:
        model = UPTContinuumLimit(node_count=n)
        result = model.evolve(final_time, cfl=cfl)
        runs.append((model, result))
    reference = runs[-1][0]
    rows = []
    for model, result in runs[:-1]:
        errors = [value-interpolate_periodic(reference.field, i/model.node_count)
                  for i, value in enumerate(model.field)]
        rms = sqrt(sum(e*e for e in errors)/len(errors))
        rows.append({"nodes": model.node_count, "dx": model.dx,
                     "field_rms_error": rms,
                     "mean_error": abs(model.mean()-reference.mean()),
                     "memory_error": abs(model.memory-reference.memory),
                     "energy": model.energy(), "steps": result["steps"]})
    return rows, {"nodes": reference.node_count, "dx": reference.dx,
                  "energy": reference.energy(), **reference.observable(),
                  "steps": runs[-1][1]["steps"]}
