import math
import unittest

from research.one_time_field.lorentz_covariant import CovariantParameters
from research.one_time_field.minkowski_3plus1 import (
    divergence_identity_3plus1, euler_lagrange_residuals_3plus1,
    lagrangian_density_3plus1, lorentz_transform_gradient,
    minkowski_gradient_norm, on_shell_second_time_derivatives_3plus1,
    stress_energy_tensor_3plus1,
)


class Minkowski3Plus1Tests(unittest.TestCase):
    def setUp(self):
        self.p = CovariantParameters(0.4, 1.3, 0.8, 0.07)

    def test_gradient_contraction_invariant_under_arbitrary_direction_boosts(self):
        gradient = (0.71, -0.22, 0.31, 0.14)
        for velocity in ((0.3, 0.0, 0.0), (0.0, -0.6, 0.0),
                         (0.2, -0.3, 0.4), (-0.55, 0.25, 0.1)):
            transformed = lorentz_transform_gradient(gradient, velocity)
            self.assertAlmostEqual(minkowski_gradient_norm(gradient),
                                   minkowski_gradient_norm(transformed), places=12)

    def test_lagrangian_density_is_boost_invariant(self):
        phi, clock = 0.31, -0.17
        dphi = (0.7, -0.2, 0.4, 0.1)
        dt = (-0.11, 0.53, -0.27, 0.33)
        base = lagrangian_density_3plus1(phi, clock, dphi, dt, self.p)
        for velocity in ((0.4, 0.0, 0.0), (0.0, 0.5, 0.0),
                         (0.2, -0.3, 0.4)):
            got = lagrangian_density_3plus1(
                phi, clock, lorentz_transform_gradient(dphi, velocity),
                lorentz_transform_gradient(dt, velocity), self.p)
            self.assertAlmostEqual(base, got, places=12)

    def test_stress_energy_is_symmetric_and_has_hamiltonian_density(self):
        phi, clock = 0.31, -0.17
        dphi, dt = (0.7, -0.2, 0.4, 0.1), (-0.11, 0.53, -0.27, 0.33)
        tensor = stress_energy_tensor_3plus1(phi, clock, dphi, dt, self.p)
        for mu in range(4):
            for nu in range(4):
                self.assertAlmostEqual(tensor[mu][nu], tensor[nu][mu], places=14)
        expected = (
            0.5 * (dphi[0]**2 + sum(v*v for v in dphi[1:]))
            + 0.5 * self.p.field_mass**2 * phi**2
            + 0.5 * self.p.clock_kinetic * (dt[0]**2 + sum(v*v for v in dt[1:]))
            + 0.5 * self.p.clock_mass_squared * clock**2
            - self.p.coupling * clock * (0.5 * phi**2 / (1 + phi**2))
        )
        self.assertAlmostEqual(tensor[0][0], expected, places=13)

    def test_on_shell_residuals_and_divergence_identity(self):
        phi, clock = 0.42, 0.13
        lap_phi, lap_clock = 0.18, -0.09
        phi_tt, clock_tt = on_shell_second_time_derivatives_3plus1(
            phi, clock, lap_phi, lap_clock, self.p)
        residuals = euler_lagrange_residuals_3plus1(
            phi, clock, -phi_tt + lap_phi, -clock_tt + lap_clock, self.p)
        self.assertAlmostEqual(residuals[0], 0.0, places=13)
        self.assertAlmostEqual(residuals[1], 0.0, places=13)
        div = divergence_identity_3plus1(
            residuals[0], residuals[1], (0.21, -0.32, 0.17, 0.09),
            (-0.14, 0.27, -0.08, 0.12))
        for component in div:
            self.assertAlmostEqual(component, 0.0, places=13)

    def test_off_shell_divergence_identity(self):
        div = divergence_identity_3plus1(
            0.37, -0.21, (0.4, -0.7, 0.2, 0.1), (0.2, 0.5, -0.3, 0.6))
        expected = (-0.37*0.4 - (-0.21)*0.2,
                    0.37*(-0.7) + (-0.21)*0.5,
                    0.37*0.2 + (-0.21)*(-0.3),
                    0.37*0.1 + (-0.21)*0.6)
        for got, want in zip(div, expected):
            self.assertAlmostEqual(got, want, places=14)

    def test_invalid_boost_rejected(self):
        with self.assertRaises(ValueError):
            lorentz_transform_gradient((1.0, 0.0, 0.0, 0.0), (1.0, 0.0, 0.0))
        with self.assertRaises(ValueError):
            lorentz_transform_gradient((1.0, 0.0, 0.0, 0.0), (math.nan, 0.0, 0.0))


if __name__ == "__main__":
    unittest.main()
