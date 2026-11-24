import unittest

from research.one_time_field.upt11_continuum_limit import (
    UPTContinuumLimit, continuum_refinement,
)


class UPTContinuumLimitTests(unittest.TestCase):
    def setUp(self):
        self.model = UPTContinuumLimit(node_count=16)

    def test_energy_gradient_matches_finite_difference(self):
        grad, grad_m = self.model.gradient()
        eps = 1e-6
        original = self.model.field
        for i in range(self.model.node_count):
            plus, minus = list(original), list(original)
            plus[i] += eps
            minus[i] -= eps
            self.model.field = tuple(plus)
            e_plus = self.model.energy()
            self.model.field = tuple(minus)
            e_minus = self.model.energy()
            self.assertAlmostEqual(grad[i], (e_plus-e_minus)/(2*eps*self.model.dx), places=6)
        self.model.field = original
        memory = self.model.memory
        self.model.memory = memory + eps
        e_plus = self.model.energy()
        self.model.memory = memory - eps
        e_minus = self.model.energy()
        self.model.memory = memory
        self.assertAlmostEqual(grad_m, (e_plus-e_minus)/(2*eps), places=7)

    def test_energy_rate_is_negative_dissipation(self):
        rate = self.model.energy_rate()
        self.assertLessEqual(rate, 0.0)

    def test_small_step_decreases_energy(self):
        before = self.model.energy()
        self.model.step(1e-4)
        self.assertLessEqual(self.model.energy(), before + 1e-13)

    def test_periodic_constant_field_has_zero_spatial_gradient(self):
        model = UPTContinuumLimit(node_count=16, memory_strength=0,
                                  bistable_strength=0, field=(0.3,)*16)
        grad, _ = model.gradient()
        self.assertTrue(all(abs(v) < 1e-12 for v in grad))

    def test_observables_are_finite(self):
        obs = self.model.observable()
        self.assertAlmostEqual(obs["mean_field"], 0.25, places=2)
        self.assertGreaterEqual(obs["field_variance"], 0.0)

    def test_refinement_errors_decrease_for_smooth_initial_data(self):
        rows, reference = continuum_refinement(final_time=0.002, counts=(16, 32, 64), cfl=0.08)
        errors = [row["field_rms_error"] for row in rows]
        self.assertTrue(all(a > b for a, b in zip(errors, errors[1:])), errors)
        self.assertEqual(reference["nodes"], 64)

    def test_invalid_parameters_rejected(self):
        with self.assertRaises(ValueError):
            UPTContinuumLimit(node_count=4)
        with self.assertRaises(ValueError):
            self.model.evolve(0.1, cfl=0)


if __name__ == "__main__":
    unittest.main()
