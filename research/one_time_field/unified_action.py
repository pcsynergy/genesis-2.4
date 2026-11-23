"""Experiment 6: unified scalar, phase, tensor, and clock action."""
from __future__ import annotations
from dataclasses import dataclass
from math import cos, isfinite, pi, sin
from .hamiltonian import HamiltonianFieldSystem

@dataclass
class UnifiedClockActionSystem:
    """Autonomous finite-dimensional action with a constant block-diagonal metric."""
    field_system: HamiltonianFieldSystem
    clock_coordinate: float = 0.0
    clock_momentum: float = 0.0
    clock_inertia: float = 1.0
    clock_stiffness: float = 1.0
    coupling: float = 0.0
    scalar_weight: float = 1.0
    phase_weight: float = 1.0
    tensor_weight: float = 1.0

    def __post_init__(self):
        if any(self.field_system.potential_system.natural_frequencies):
            raise ValueError("autonomous action does not accept natural-frequency drive")
        for name in ("clock_coordinate","clock_momentum","clock_inertia","clock_stiffness",
                     "coupling","scalar_weight","phase_weight","tensor_weight"):
            v=float(getattr(self,name))
            if not isfinite(v): raise ValueError(f"{name} must be finite")
            if name in ("clock_inertia","clock_stiffness") and v<=0:
                raise ValueError(f"{name} must be positive")
            if name.endswith("_weight") and v<0:
                raise ValueError(f"{name} must be nonnegative")
            setattr(self,name,v)
        if not any((self.scalar_weight,self.phase_weight,self.tensor_weight)):
            raise ValueError("at least one observable weight must be positive")

    def _observable_and_gradients(self):
        s=self.field_system.potential_system
        grads={k:([[0.0]*len(r) for r in v] if k=="tensor" else [0.0]*len(v))
               for k,v in s.snapshot().items()}
        c=0.0
        if s.scalar is not None:
            for i,x in enumerate(s.scalar):
                c+=.5*self.scalar_weight*x*x/(1+x*x)
                grads["scalar"][i]=self.scalar_weight*x/(1+x*x)**2
        if s.tensor is not None:
            for i,row in enumerate(s.tensor):
                n2=sum(x*x for x in row)
                c+=.5*self.tensor_weight*n2/(1+n2)
                for k,x in enumerate(row):
                    grads["tensor"][i][k]=self.tensor_weight*x/(1+n2)**2
        if s.phases is not None:
            total=sum(s.adjacency[i][j] for i in range(s.node_count)
                      for j in range(i+1,s.node_count))
            if total:
                for i in range(s.node_count):
                    for j in range(i+1,s.node_count):
                        w=s.adjacency[i][j]
                        d=s.phases[i]-s.phases[j]
                        c+=self.phase_weight*w*(1-cos(d))/total
                        z=self.phase_weight*w*sin(d)/total
                        grads["phases"][i]+=z
                        grads["phases"][j]-=z
        return c,grads

    def clock_observable(self): return self._observable_and_gradients()[0]
    def potential_energy(self):
        return (self.field_system.potential_system.potential()
                +.5*self.clock_stiffness*self.clock_coordinate**2
                -self.coupling*self.clock_coordinate*self.clock_observable())
    def kinetic_energy(self):
        return self.field_system.kinetic_energy()+self.clock_momentum**2/(2*self.clock_inertia)
    def energy(self): return self.kinetic_energy()+self.potential_energy()
    def lagrangian(self): return self.kinetic_energy()-self.potential_energy()

    def _gradients(self):
        base=self.field_system.potential_system.gradients()
        c,cg=self._observable_and_gradients()
        factor=self.coupling*self.clock_coordinate
        for domain in base:
            if domain=="tensor":
                for i in range(len(base[domain])):
                    for k in range(len(base[domain][i])):
                        base[domain][i][k]-=factor*cg[domain][i][k]
            else:
                base[domain]=[a-factor*b for a,b in zip(base[domain],cg[domain])]
        return base,self.clock_stiffness*self.clock_coordinate-self.coupling*c

    def step(self,dt):
        if not isfinite(dt) or dt<=0: raise ValueError("dt must be finite and positive")
        fs,ps=self.field_system,self.field_system.potential_system
        g0,cg0=self._gradients()
        half={}
        for d,mom in fs.momenta.items():
            inertia=fs._inertia(d)
            if d=="tensor":
                half[d]=[[p-.5*dt*g for p,g in zip(pr,gr)] for pr,gr in zip(mom,g0[d])]
                ps.tensor=[[q+dt*p/inertia for q,p in zip(qr,pr)]
                           for qr,pr in zip(ps.tensor,half[d])]
            else:
                half[d]=[p-.5*dt*g for p,g in zip(mom,g0[d])]
                q=[x+dt*p/inertia for x,p in zip(getattr(ps,d),half[d])]
                if d=="phases": q=[x%(2*pi) for x in q]
                setattr(ps,d,q)
        ch=self.clock_momentum-.5*dt*cg0
        self.clock_coordinate+=dt*ch/self.clock_inertia
        g1,cg1=self._gradients()
        for d,mom in half.items():
            if d=="tensor":
                fs.momenta[d]=[[p-.5*dt*g for p,g in zip(pr,gr)] for pr,gr in zip(mom,g1[d])]
            else: fs.momenta[d]=[p-.5*dt*g for p,g in zip(mom,g1[d])]
        self.clock_momentum=ch-.5*dt*cg1
        if not isfinite(self.energy()): raise RuntimeError("non-finite unified-action state")
        return self.snapshot()

    def snapshot(self):
        return {"fields":self.field_system.snapshot(),"clock_coordinate":self.clock_coordinate,
                "clock_momentum":self.clock_momentum,"clock_observable":self.clock_observable(),
                "energy":self.energy()}
