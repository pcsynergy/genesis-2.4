import unittest

from research.one_time_field.lorentz_covariant import CovariantParameters
from research.one_time_field.stress_energy import (
    divergence_from_field_equations,
    on_shell_second_time_derivatives,
    stress_energy_tensor,
)


class StressEnergyTests(unittest.TestCase):
    def setUp(self):
        self.p = CovariantParameters(0.4, 1.3, 0.8, 0.07)

    def test_tensor_is_symmetric(self):
        tensor = stress_energy_tensor(0.31, -0.17, (0.7, -0.2),
                                      (-0.11, 0.53), self.p)
        self.assertEqual(tensor[0][1], tensor[1][0])

    def test_energy_density_matches_hamiltonian_density(self):
        phi, clock = 0.31, -0.17
        phi_d, clock_d = (0.7, -0.2), (-0.11, 0.53)
        t00 = stress_energy_tensor(phi, clock, phi_d, clock_d, self.p)[0][0]
        expected = (
            0.5 * phi_d[0]**2 + 0.5 * phi_d[1]**2
            + 0.5 * self.p.field_mass**2 * phi**2
            + 0.5 * self.p.clock_kinetic * clock_d[0]**2
            + 0.5 * self.p.clock_kinetic * clock_d[1]**2
            + 0.5 * self.p.clock_mass_squared * clock**2
            - self.p.coupling * clock * (0.5 * phi**2 / (1 + phi**2))
        )
        self.assertAlmostEqual(t00, expected, places=13)

    def test_on_shell_divergence_vanishes(self):
        phi, clock = 0.42, 0.13
        phi_d, clock_d = (0.21, -0.32), (-0.14, 0.27)
        phi_dxx, clock_dxx = 0.18, -0.09
        phi_tt, clock_tt = on_shell_second_time_derivatives(
            phi, clock, phi_d, clock_d, phi_dxx, clock_dxx, self.p
        )
        divergence = divergence_from_field_equations(
            phi, clock, phi_d, clock_d,
            (phi_tt, 0.06, phi_dxx),
            (clock_tt, -0.03, clock_dxx), self.p
        )
        self.assertAlmostEqual(divergence[0], 0.0, places=13)
        self.assertAlmostEqual(divergence[1], 0.0, places=13)

    def test_off_shell_divergence_equals_equation_residual_identity(self):
        phi, clock = -0.23, 0.19
        phi_d, clock_d = (0.4, -0.7), (0.2, 0.5)
        phi_second, clock_second = (0.3, -0.1, 0.8), (-0.2, 0.07, 0.4)
        div = divergence_from_field_equations(
            phi, clock, phi_d, clock_d, phi_second, clock_second, self.p
        )
        from research.one_time_field.lorentz_covariant import euler_lagrange_residuals
        rphi = -phi_second[0] + phi_second[2] - self.p.field_mass**2 * phi
        from research.one_time_field.lorentz_covariant import coupling_derivative, coupling_function
        rphi += self.p.coupling * clock * coupling_derivative(phi)
        rclock = self.p.clock_kinetic * (-clock_second[0] + clock_second[2])
        rclock += -self.p.clock_mass_squared * clock + self.p.coupling * coupling_function(phi)
        self.assertAlmostEqual(div[0], -rphi * phi_d[0] - rclock * clock_d[0], places=13)
        self.assertAlmostEqual(div[1], rphi * phi_d[1] + rclock * clock_d[1], places=13)


if __name__ == "__main__":
    unittest.main()
