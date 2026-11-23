"""Experiment 7: periodic 1-D continuum scalar field coupled to a dynamical clock.

This is a finite-difference discretization of a deliberately simple continuum
action. It is a numerical continuum-limit probe, not a relativistic or
empirically validated theory.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import cos, isfinite, pi, sin


@dataclass
class ContinuumClockFieldSystem:
    """Periodic Klein-Gordon-like scalar field plus one autonomous clock mode.

    S = integral dt [ integral_0^L dx (1/2 phi_t^2 - 1/2 c^2 phi_x^2
        - 1/2 m^2 phi^2) + 1/2 I Tdot^2 - 1/2 k T^2 + g T C[phi] ]

    C[phi] = integral_0^L dx 1/2 phi^2/(1+phi^2).
    The grid is periodic and the spatial derivative is centered second order.
    """
    node_count: int = 64
    length: float = 2.0*pi
    wave_speed: float = 1.0
    mass: float = 0.4
    clock: float = 0.1
    clock_velocity: float = 0.0
    clock_inertia: float = 1.0
    clock_stiffness: float = 0.8
    coupling: float = 0.05
    field: list[float] | None = None
    velocity: list[float] | None = None

    def __post_init__(self):
        if self.node_count < 8 or self.length <= 0 or self.wave_speed <= 0:
            raise ValueError("grid needs at least 8 nodes and positive length/speed")
        if self.clock_inertia <= 0 or self.clock_stiffness <= 0 or self.mass < 0:
            raise ValueError("inertia and stiffness must be positive; mass nonnegative")
        if not all(isfinite(float(x)) for x in (
            self.length, self.wave_speed, self.mass, self.clock,
            self.clock_velocity, self.clock_inertia, self.clock_stiffness, self.coupling
        )):
            raise ValueError("parameters must be finite")
        dx = self.length / self.node_count
        if self.field is None:
            self.field = [0.35*cos(2*pi*i/self.node_count) + 0.12*sin(4*pi*i/self.node_count)
                          for i in range(self.node_count)]
        if self.velocity is None:
            self.velocity = [0.04*sin(2*pi*i/self.node_count) for i in range(self.node_count)]
        if len(self.field) != self.node_count or len(self.velocity) != self.node_count:
            raise ValueError("field and velocity arrays must match node_count")
        if not all(isfinite(float(x)) for x in self.field + self.velocity):
            raise ValueError("field data must be finite")
        self.dx = dx
        self.time = 0.0

    def observable(self) -> float:
        return self.dx * sum(0.5*x*x/(1.0+x*x) for x in self.field)

    def acceleration(self):
        n = self.node_count
        lap = [(self.field[(i+1)%n] - 2*self.field[i] + self.field[(i-1)%n])/(self.dx*self.dx)
               for i in range(n)]
        phi_acc = [self.wave_speed**2*lap[i] - self.mass**2*self.field[i]
                   + self.coupling*self.clock*self.field[i]/(1+self.field[i]**2)**2
                   for i in range(n)]
        clock_acc = (-self.clock_stiffness*self.clock + self.coupling*self.observable())/self.clock_inertia
        return phi_acc, clock_acc

    def energy(self) -> float:
        grad = [(self.field[(i+1)%self.node_count]-self.field[i])/self.dx
                for i in range(self.node_count)]
        field_k = 0.5*self.dx*sum(v*v for v in self.velocity)
        field_u = 0.5*self.dx*sum(self.wave_speed**2*d*d + self.mass**2*x*x
                                  for d, x in zip(grad, self.field))
        clock_k = 0.5*self.clock_inertia*self.clock_velocity**2
        clock_u = 0.5*self.clock_stiffness*self.clock**2 - self.coupling*self.clock*self.observable()
        return field_k + field_u + clock_k + clock_u

    def step(self, dt: float):
        if not isfinite(dt) or dt <= 0:
            raise ValueError("dt must be finite and positive")
        a0, c0 = self.acceleration()
        vh = [v + 0.5*dt*a for v, a in zip(self.velocity, a0)]
        ch = self.clock_velocity + 0.5*dt*c0
        self.field = [x + dt*v for x, v in zip(self.field, vh)]
        self.clock += dt*ch
        a1, c1 = self.acceleration()
        self.velocity = [v + 0.5*dt*a for v, a in zip(vh, a1)]
        self.clock_velocity = ch + 0.5*dt*c1
        self.time += dt
        if not isfinite(self.energy()):
            raise RuntimeError("non-finite continuum state")
        return self.energy()


def _interpolate_periodic(values, x):
    n = len(values)
    u = (x % 1.0)*n
    i = int(u)
    f = u-i
    return values[i % n]*(1-f) + values[(i+1) % n]*f


def refinement_experiment(final_time: float = 0.5, counts=(32, 64, 128, 256)):
    """Run CFL-scaled refinements and compare each grid to the finest solution."""
    runs = []
    for n in counts:
        dx = 2*pi/n
        dt_limit = 0.18*dx
        steps = int(__import__("math").ceil(final_time/dt_limit))
        dt = final_time/steps
        system = ContinuumClockFieldSystem(node_count=n)
        e0 = system.energy()
        for _ in range(steps):
            system.step(dt)
        runs.append((n, dt, system, abs(system.energy()-e0)))
    reference = runs[-1][2]
    rows = []
    for n, dt, system, drift in runs[:-1]:
        errors = []
        for i, value in enumerate(system.field):
            x = i/n
            errors.append(value-_interpolate_periodic(reference.field, x))
        rms = (sum(e*e for e in errors)/len(errors))**0.5
        rows.append({"nodes": n, "dt": dt, "field_rms_error": rms,
                     "clock_error": abs(system.clock-reference.clock),
                     "energy_drift": drift})
    return rows, {"nodes": reference.node_count, "dt": runs[-1][1],
                  "clock": reference.clock, "energy": reference.energy()}


if __name__ == "__main__":
    rows, ref = refinement_experiment()
    print("nodes,dt,field_rms_error,clock_error,energy_drift")
    for r in rows:
        print("{nodes},{dt:.8g},{field_rms_error:.8g},{clock_error:.8g},{energy_drift:.8g}".format(**r))
    print("reference", ref)
