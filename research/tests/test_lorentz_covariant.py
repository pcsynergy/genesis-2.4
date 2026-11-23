import math
import unittest

from research.one_time_field.lorentz_covariant import (
    CovariantParameters,
    coupling_function,
    d_alembertian,
    euler_lagrange_residuals,
    lagrangian_density,
    lorentz_boost_gradient,
    lorentz_boost_hessian,
    minkowski_gradient_norm,
)


class LorentzCovarianceTests(unittest.TestCase):
    def setUp(self):
        self.p = CovariantParameters(0.4, 1.3, 0.8, 0.07)

    def test_minkowski_gradient_norm_is_boost_invariant(self):
        for v in (-0.8, -0.3, 0.0, 0.45, 0.9):
            grad = (0.71, -0.22)
            boosted = lorentz_boost_gradient(grad, v)
            self.assertAlmostEqual(minkowski_gradient_norm(grad),
                                   minkowski_gradient_norm(boosted), places=12)

    def test_full_lagrangian_density_is_boost_invariant(self):
        phi, clock = 0.31, -0.17
        dphi, dclock = (0.7, -0.2), (-0.11, 0.53)
        original = lagrangian_density(phi, clock, dphi, dclock, self.p)
        for v in (-0.75, -0.2, 0.4, 0.85):
            transformed = lagrangian_density(
                phi, clock,
                lorentz_boost_gradient(dphi, v),
                lorentz_boost_gradient(dclock, v), self.p)
            self.assertAlmostEqual(original, transformed, places=12)

    def test_d_alembertian_is_boost_invariant(self):
        hessian = (0.8, -0.19, 0.37)
        original = d_alembertian((hessian[0], hessian[2]))
        for v in (-0.7, 0.25, 0.82):
            boosted = lorentz_boost_hessian(*hessian, v)
            self.assertAlmostEqual(original,
                                   d_alembertian((boosted[0], boosted[2])),
                                   places=12)

    def test_equations_are_scalar_residuals_under_boost(self):
        # Since both fields and their box operators are scalars, their
        # Euler-Lagrange residuals must have the same value in every frame.
        phi, clock = 0.42, 0.13
        phi_hessian = (0.3, 0.08, -0.2)
        clock_hessian = (-0.1, 0.04, 0.6)
        box_phi = d_alembertian((phi_hessian[0], phi_hessian[2]))
        box_clock = d_alembertian((clock_hessian[0], clock_hessian[2]))
        base = euler_lagrange_residuals(phi, clock, box_phi, box_clock, self.p)
        for v in (-0.6, 0.35, 0.78):
            hp = lorentz_boost_hessian(*phi_hessian, v)
            ht = lorentz_boost_hessian(*clock_hessian, v)
            got = euler_lagrange_residuals(
                phi, clock, d_alembertian((hp[0], hp[2])),
                d_alembertian((ht[0], ht[2])), self.p)
            self.assertAlmostEqual(base[0], got[0], places=12)
            self.assertAlmostEqual(base[1], got[1], places=12)

    def test_invalid_boost_rejected(self):
        with self.assertRaises(ValueError):
            lorentz_boost_gradient((1.0, 0.0), 1.0)

    def test_bounded_coupling_function(self):
        self.assertGreaterEqual(coupling_function(100.0), 0.0)
        self.assertLessEqual(coupling_function(100.0), 0.5)


if __name__ == "__main__":
    unittest.main()
