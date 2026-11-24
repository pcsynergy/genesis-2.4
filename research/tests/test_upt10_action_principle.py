import unittest

from research.one_time_field.upt10_action_principle import UPTActionPrinciple


class UPTActionPrincipleTests(unittest.TestCase):
    def setUp(self):
        self.model = UPTActionPrinciple(
            adjacency=((0, 1, 0), (1, 0, 1), (0, 1, 0)),
            relational_strength=0.8,
            memory_strength=0.6,
            bistable_strength=0.4,
        )

    def test_energy_is_finite_and_nonnegative(self):
        self.assertGreaterEqual(self.model.energy((0.2, 0.7, 0.4), 1.1), 0.0)

    def test_gradient_matches_centered_finite_difference(self):
        phi, memory, eps = (0.2, 0.7, 0.4), 1.1, 1e-6
        analytic_phi, analytic_m = self.model.gradient(phi, memory)
        for i in range(len(phi)):
            plus, minus = list(phi), list(phi)
            plus[i] += eps
            minus[i] -= eps
            numeric = (self.model.energy(plus, memory) -
                       self.model.energy(minus, memory)) / (2 * eps)
            self.assertAlmostEqual(analytic_phi[i], numeric, places=7)
        numeric_m = (self.model.energy(phi, memory + eps) -
                     self.model.energy(phi, memory - eps)) / (2 * eps)
        self.assertAlmostEqual(analytic_m, numeric_m, places=7)

    def test_onsager_flow_has_nonpositive_energy_rate(self):
        rate = self.model.energy_rate((0.2, 0.7, 0.4), 1.1)
        dissipation = self.model.dissipation_rate((0.2, 0.7, 0.4), 1.1)
        self.assertAlmostEqual(rate, -dissipation, places=12)
        self.assertLessEqual(rate, 0.0)

    def test_energy_decreases_under_backtracked_step(self):
        phi, memory = (0.2, 0.7, 0.4), 1.1
        before = self.model.energy(phi, memory)
        next_phi, next_memory, used_dt = self.model.step(phi, memory, 10.0)
        self.assertGreater(used_dt, 0.0)
        self.assertLessEqual(self.model.energy(next_phi, next_memory), before + 1e-13)

    def test_relational_gradient_vanishes_for_uniform_field_when_other_terms_off(self):
        model = UPTActionPrinciple(
            adjacency=((0, 1), (1, 0)), relational_strength=2,
            memory_strength=0, bistable_strength=0)
        grad, memory_grad = model.gradient((0.3, 0.3), 0.0)
        self.assertEqual(grad, (0.0, 0.0))
        self.assertEqual(memory_grad, 0.0)

    def test_zero_field_mobility_freezes_field(self):
        model = UPTActionPrinciple(
            adjacency=((0, 1), (1, 0)), field_mobility=0,
            memory_mobility=1)
        dphi, dm = model.rhs((0.2, 0.8), 0.5)
        self.assertEqual(dphi, (0.0, 0.0))
        self.assertNotEqual(dm, 0.0)

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            self.model.energy((1.0,), 0.0)
        with self.assertRaises(ValueError):
            self.model.step((0.1, 0.2, 0.3), 0.5, 0.0)


if __name__ == "__main__":
    unittest.main()
