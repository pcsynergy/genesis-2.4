import math
import unittest

from research.one_time_field.flrw_curved import (
    continuity_residual_flrw,
    energy_density_pressure_flrw,
    euler_lagrange_residuals_flrw,
    flrw_inverse_metric,
    flrw_metric,
    hubble_parameter,
    lagrangian_density_flrw,
    metric_determinant,
    on_shell_accelerations_flrw,
    scalar_dalembertian_homogeneous,
    stress_energy_tensor_flrw,
    volume_factor,
)
from research.one_time_field.lorentz_covariant import CovariantParameters


class TestFLRWCurvedBackground(unittest.TestCase):
    def setUp(self):
        self.p = CovariantParameters(
            field_mass=0.7, clock_kinetic=1.3,
            clock_mass_squared=0.9, coupling=0.08,
        )

    def test_metric_inverse_and_determinant(self):
        a = 2.5
        g = flrw_metric(a)
        gi = flrw_inverse_metric(a)
        for i in range(4):
            for j in range(4):
                product = sum(g[i][k] * gi[k][j] for k in range(4))
                self.assertAlmostEqual(product, 1.0 if i == j else 0.0)
        self.assertAlmostEqual(metric_determinant(a), -(a ** 6))
        self.assertAlmostEqual(volume_factor(a), a ** 3)

    def test_scale_factor_validation(self):
        for function in (flrw_metric, flrw_inverse_metric,
                         metric_determinant, volume_factor):
            with self.assertRaises(ValueError):
                function(0.0)

    def test_hubble_and_scalar_wave_operator(self):
        self.assertAlmostEqual(hubble_parameter(4.0, 0.8), 0.2)
        self.assertAlmostEqual(
            scalar_dalembertian_homogeneous(0.3, -0.4, 0.2),
            -(-0.4 + 3.0 * 0.2 * 0.3),
        )
        # Static a=1 is the homogeneous Minkowski limit.
        self.assertAlmostEqual(
            scalar_dalembertian_homogeneous(0.3, 0.4, 0.0), -0.4
        )

    def test_lagrangian_flat_limit_matches_minkowski_form(self):
        phi, clock, pd, td = 0.6, -0.2, 0.15, -0.08
        flat = lagrangian_density_flrw(phi, clock, pd, td, self.p)
        expected = (
            0.5 * pd**2 - 0.5 * self.p.field_mass**2 * phi**2
            + 0.5 * self.p.clock_kinetic * td**2
            - 0.5 * self.p.clock_mass_squared * clock**2
            + self.p.coupling * clock
            * (0.5 * phi**2 / (1.0 + phi**2))
        )
        self.assertAlmostEqual(flat, expected)

    def test_on_shell_accelerations_zero_residuals(self):
        phi, clock = 0.45, -0.3
        pd, td, h = 0.12, -0.07, 0.16
        pdd, tdd = on_shell_accelerations_flrw(
            phi, clock, pd, td, h, self.p
        )
        residuals = euler_lagrange_residuals_flrw(
            phi, clock, pd, td, pdd, tdd, h, self.p
        )
        self.assertAlmostEqual(residuals[0], 0.0, places=12)
        self.assertAlmostEqual(residuals[1], 0.0, places=12)

    def test_off_shell_continuity_identity(self):
        residuals = (0.31, -0.22)
        pd, td = 0.4, -0.15
        expected = -pd * residuals[0] - td * residuals[1]
        self.assertAlmostEqual(
            continuity_residual_flrw(pd, td, *residuals), expected
        )

    def test_stress_tensor_isotropic_and_energy_density(self):
        phi, clock, pd, td, a = 0.5, -0.1, 0.2, 0.06, 1.7
        rho, pressure = energy_density_pressure_flrw(
            phi, clock, pd, td, self.p
        )
        tensor = stress_energy_tensor_flrw(
            phi, clock, pd, td, a, self.p
        )
        self.assertAlmostEqual(tensor[0][0], rho)
        for i in range(1, 4):
            self.assertAlmostEqual(tensor[i][i] / a**2, pressure)
            for j in range(4):
                if i != j:
                    self.assertAlmostEqual(tensor[i][j], 0.0)
        self.assertAlmostEqual(tensor[0][1], 0.0)

    def test_de_sitter_and_power_law_backgrounds(self):
        # a=exp(Ht): H is constant.
        h0, t = 0.13, 2.0
        a = math.exp(h0 * t)
        adot = h0 * a
        self.assertAlmostEqual(hubble_parameter(a, adot), h0)
        # a=t^p (t>0): H=p/t.
        p, t = 0.7, 3.0
        a = t**p
        adot = p * t**(p - 1.0)
        self.assertAlmostEqual(hubble_parameter(a, adot), p / t)


if __name__ == "__main__":
    unittest.main()
