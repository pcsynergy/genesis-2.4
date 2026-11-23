"""Experiment 8: spatially local clock field coupled to a scalar field.

Periodic one-dimensional classical toy model. The local clock T(x,t) has its
own inertia, propagation stiffness, and restoring potential. This is not yet
a Lorentz-covariant spacetime theory.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite, pi, sin, cos


@dataclass
class LocalClockFieldSystem:
    node_count: int = 64
    length: float = 2*pi
    field_speed: float = 1.0
    field_mass: float = 0.4
    clock_speed: float = 0.7
    clock_inertia: float = 1.0
    clock_stiffness: float = 0.8
    coupling: float = 0.05
    field: list[float] | None = None
    field_velocity: list[float] | None = None
    clock: list[float] | None = None
    clock_velocity: list[float] | None = None

    def __post_init__(self):
        if self.node_count < 8 or self.length <= 0:
            raise ValueError("need at least 8 nodes and positive domain length")
        if self.field_speed <= 0 or self.clock_speed <= 0 or self.clock_inertia <= 0:
            raise ValueError("propagation speeds and clock inertia must be positive")
        if self.field_mass < 0 or self.clock_stiffness <= 0:
            raise ValueError("field mass must be nonnegative and clock stiffness positive")
        params=(self.length,self.field_speed,self.field_mass,self.clock_speed,
                self.clock_inertia,self.clock_stiffness,self.coupling)
        if not all(isfinite(float(x)) for x in params):
            raise ValueError("parameters must be finite")
        n=self.node_count
        if self.field is None:
            self.field=[0.30*cos(2*pi*i/n)+0.08*sin(3*2*pi*i/n) for i in range(n)]
        if self.field_velocity is None:
            self.field_velocity=[0.03*sin(2*pi*i/n) for i in range(n)]
        if self.clock is None:
            self.clock=[0.12+0.025*cos(2*pi*i/n+0.3) for i in range(n)]
        if self.clock_velocity is None:
            self.clock_velocity=[0.01*sin(2*pi*i/n+0.2) for i in range(n)]
        arrays=(self.field,self.field_velocity,self.clock,self.clock_velocity)
        if any(len(a)!=n for a in arrays):
            raise ValueError("all state arrays must match node_count")
        if not all(isfinite(float(x)) for a in arrays for x in a):
            raise ValueError("state values must be finite")
        self.dx=self.length/n
        self.time=0.0

    def observable_density(self, x):
        return 0.5*x*x/(1.0+x*x)

    def laplacian(self, values):
        n=self.node_count
        return [(values[(i+1)%n]-2*values[i]+values[(i-1)%n])/(self.dx*self.dx)
                for i in range(n)]

    def energy(self):
        grad_f=[(self.field[(i+1)%self.node_count]-self.field[i])/self.dx
                for i in range(self.node_count)]
        grad_t=[(self.clock[(i+1)%self.node_count]-self.clock[i])/self.dx
                for i in range(self.node_count)]
        density=[]
        for i in range(self.node_count):
            phi=self.field[i]
            density.append(
                0.5*self.field_velocity[i]**2
                +0.5*self.field_speed**2*grad_f[i]**2
                +0.5*self.field_mass**2*phi**2
                +0.5*self.clock_inertia*self.clock_velocity[i]**2
                +0.5*self.clock_speed**2*grad_t[i]**2
                +0.5*self.clock_stiffness*self.clock[i]**2
                -self.coupling*self.clock[i]*self.observable_density(phi)
            )
        return self.dx*sum(density)

    def accelerations(self):
        lap_f=self.laplacian(self.field)
        lap_t=self.laplacian(self.clock)
        af=[]
        at=[]
        for i,phi in enumerate(self.field):
            fprime=phi/(1.0+phi*phi)**2
            af.append(self.field_speed**2*lap_f[i]-self.field_mass**2*phi
                      +self.coupling*self.clock[i]*fprime)
            at.append((self.clock_speed**2*lap_t[i]
                       -self.clock_stiffness*self.clock[i]
                       +self.coupling*self.observable_density(phi))/self.clock_inertia)
        return af,at

    def step(self, dt):
        if not isfinite(dt) or dt<=0:
            raise ValueError("dt must be finite and positive")
        af0,at0=self.accelerations()
        vh=[v+0.5*dt*a for v,a in zip(self.field_velocity,af0)]
        wh=[v+0.5*dt*a for v,a in zip(self.clock_velocity,at0)]
        self.field=[x+dt*v for x,v in zip(self.field,vh)]
        self.clock=[x+dt*v for x,v in zip(self.clock,wh)]
        af1,at1=self.accelerations()
        self.field_velocity=[v+0.5*dt*a for v,a in zip(vh,af1)]
        self.clock_velocity=[v+0.5*dt*a for v,a in zip(wh,at1)]
        self.time+=dt
        if not isfinite(self.energy()):
            raise RuntimeError("non-finite local clock-field state")
        return self.energy()


def _periodic_interpolate(values, x):
    n=len(values)
    u=(x%1.0)*n
    i=int(u)
    f=u-i
    return values[i]*(1-f)+values[(i+1)%n]*f


def refinement_experiment(final_time=0.4, counts=(32,64,128,256)):
    runs=[]
    for n in counts:
        dx=2*pi/n
        vmax=max(1.0,0.7/(1.0**0.5))
        limit=0.16*dx/vmax
        steps=int(__import__("math").ceil(final_time/limit))
        dt=final_time/steps
        s=LocalClockFieldSystem(node_count=n)
        e0=s.energy()
        for _ in range(steps):
            s.step(dt)
        runs.append((n,dt,s,abs(s.energy()-e0)))
    ref=runs[-1][2]
    rows=[]
    for n,dt,s,drift in runs[:-1]:
        ef=[s.field[i]-_periodic_interpolate(ref.field,i/n) for i in range(n)]
        et=[s.clock[i]-_periodic_interpolate(ref.clock,i/n) for i in range(n)]
        rows.append({"nodes":n,"dt":dt,
                     "field_rms_error":(sum(x*x for x in ef)/n)**0.5,
                     "clock_rms_error":(sum(x*x for x in et)/n)**0.5,
                     "energy_drift":drift})
    return rows,{"nodes":ref.node_count,"dt":runs[-1][1],
                 "energy":ref.energy(),"clock_mean":sum(ref.clock)/ref.node_count}


if __name__=="__main__":
    rows,ref=refinement_experiment()
    print("nodes,dt,field_rms_error,clock_rms_error,energy_drift")
    for r in rows:
        print("{nodes},{dt:.8g},{field_rms_error:.8g},{clock_rms_error:.8g},{energy_drift:.8g}".format(**r))
    print("reference",ref)
