import unittest
from research.one_time_field.gravitational_flrw import (
    acceleration_residual, einstein_equation_residuals_flrw,
    einstein_tensor_flrw, friedmann_constraint_propagation,
    friedmann_residual, ricci_scalar_flrw,
)
from research.one_time_field.flrw_curved import energy_density_pressure_flrw
from research.one_time_field.lorentz_covariant import CovariantParameters

class TestDynamicalGravityFLRW(unittest.TestCase):
    def setUp(self):
        self.params = CovariantParameters(field_mass=0.5, clock_kinetic=1.2,
            clock_mass_squared=0.7, coupling=0.04)

    def test_ricci_and_einstein_tensor(self):
        a,h,hd = 2.0,0.1,-0.02
        self.assertAlmostEqual(ricci_scalar_flrw(h,hd),6.0*(hd+2*h*h))
        tensor=einstein_tensor_flrw(a,h,hd)
        self.assertAlmostEqual(tensor[0][0],3*h*h)
        spatial=a*a*(-2*hd-3*h*h)
        for i in range(1,4):
            self.assertAlmostEqual(tensor[i][i],spatial)
            for j in range(4):
                if i != j: self.assertAlmostEqual(tensor[i][j],0.0)

    def test_friedmann_and_acceleration(self):
        mpl2,h,rho,p=2.5,0.2,3*2.5*0.2**2,0.17
        hd=-(rho+p)/(2*mpl2)
        self.assertAlmostEqual(friedmann_residual(h,rho,mpl2),0.0)
        self.assertAlmostEqual(acceleration_residual(hd,rho,p,mpl2),0.0)

    def test_coupled_scalar_matter_equations(self):
        phi,clock,pd,td=0.4,-0.2,0.03,0.02
        rho,p=energy_density_pressure_flrw(phi,clock,pd,td,self.params)
        mpl2=1.7
        h=(rho/(3*mpl2))**0.5
        hd=-(rho+p)/(2*mpl2)
        residuals=einstein_equation_residuals_flrw(
            1.0,h,hd,phi,clock,pd,td,mpl2,self.params)
        self.assertAlmostEqual(residuals[0],0.0)
        self.assertAlmostEqual(residuals[1],0.0)

    def test_constraint_propagation(self):
        mpl2,h,rho,p=1.8,0.14,0.21,0.06
        hd=-(rho+p)/(2*mpl2)
        rho_dot=-3*h*(rho+p)
        self.assertAlmostEqual(
            friedmann_constraint_propagation(h,hd,rho_dot,mpl2),0.0)

    def test_positive_planck_mass_required(self):
        with self.assertRaises(ValueError): friedmann_residual(0.1,0.2,0.0)
        with self.assertRaises(ValueError): acceleration_residual(0.1,0.2,0.3,-1)

if __name__ == "__main__": unittest.main()
