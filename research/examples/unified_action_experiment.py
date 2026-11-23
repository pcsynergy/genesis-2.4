"""Run Experiment 6: unified shared field action."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from one_time_field.hamiltonian import HamiltonianFieldSystem
from one_time_field.variational import VariationalFieldSystem
from one_time_field.unified_action import UnifiedClockActionSystem

def build(g):
    p=VariationalFieldSystem(adjacency=[[0.,1.],[1.,0.]],scalar=[.6,-.2],
        phases=[.3,1.1],tensor=[[.2,.4],[-.1,.3]],scalar_mass=.15,tensor_mass=.1,
        scalar_gradient=.3,tensor_gradient=.2,phase_gradient=.4,
        scalar_phase_coupling=.05,tensor_phase_coupling=.04)
    f=HamiltonianFieldSystem(p,scalar_inertia=1.1,phase_inertia=.9,tensor_inertia=1.2,
        momenta={"scalar":[.03,-.02],"phases":[.1,-.1],"tensor":[[.02,.01],[-.01,.03]]})
    return UnifiedClockActionSystem(f,.15,.02,1.3,.7,g)
def main():
    control,coupled=build(0),build(.08); e=coupled.energy()
    print("lambda,clock,observable,energy,energy_drift")
    for n in range(1001):
        if n%100==0:
            print(f"{n*.0015:.4f},{coupled.clock_coordinate:.9g},{coupled.clock_observable():.9g},{coupled.energy():.12g},{coupled.energy()-e:.3g}")
        if n<1000: control.step(.0015); coupled.step(.0015)
    print("uncoupled_field_energy",control.field_system.energy())
if __name__=="__main__": main()
