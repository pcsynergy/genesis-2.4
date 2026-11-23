import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from one_time_field.hamiltonian import HamiltonianFieldSystem
from one_time_field.variational import VariationalFieldSystem
from one_time_field.unified_action import UnifiedClockActionSystem

def build(g=0.,shift=0.):
    p=VariationalFieldSystem(adjacency=[[0.,1.],[1.,0.]],scalar=[.6,-.2],
        phases=[.3+shift,1.1+shift],tensor=[[.2,.4],[-.1,.3]],
        scalar_mass=.15,tensor_mass=.1,scalar_gradient=.3,tensor_gradient=.2,
        phase_gradient=.4,scalar_phase_coupling=.05,tensor_phase_coupling=.04)
    f=HamiltonianFieldSystem(p,scalar_inertia=1.1,phase_inertia=.9,tensor_inertia=1.2,
        momenta={"scalar":[.03,-.02],"phases":[.1,-.1],"tensor":[[.02,.01],[-.01,.03]]})
    return UnifiedClockActionSystem(f,.15,.02,1.3,.7,g)

class UnifiedActionTests(unittest.TestCase):
    def test_all_domains_couple(self):
        m=build(.12); g,_=m._gradients()
        self.assertGreater(m.clock_observable(),0)
        for d in ("scalar","phases","tensor"):
            self.assertTrue(any(abs(x)>0 for r in g[d] for x in (r if isinstance(r,list) else [r])))
    def test_energy_error_bounded(self):
        m=build(.08); e=m.energy(); err=[]
        for _ in range(1500): m.step(.0015); err.append(abs(m.energy()-e))
        self.assertLess(max(err),2e-5)
    def test_phase_shift_symmetry_and_noether_charge(self):
        a,b=build(.1),build(.1,2.4)
        self.assertAlmostEqual(a.energy(),b.energy(),places=12)
        p=sum(a.field_system.momenta["phases"])
        for _ in range(300): a.step(.001)
        self.assertAlmostEqual(sum(a.field_system.momenta["phases"]),p,places=11)
    def test_zero_coupling_field_energy_limit(self):
        m=build(0); e=m.field_system.energy()
        for _ in range(20): m.step(.001)
        self.assertAlmostEqual(m.field_system.energy(),e,delta=2e-5)
    def test_lagrangian_and_validation(self):
        m=build(.05); self.assertAlmostEqual(m.lagrangian(),m.kinetic_energy()-m.potential_energy())
        with self.assertRaises(ValueError): m.step(0)
if __name__=="__main__": unittest.main()
