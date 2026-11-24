import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.upt9_memory_dynamics import UPTMemoryDynamics

CYCLE4 = ((0,1,0,1),(1,0,1,0),(0,1,0,1),(1,0,1,0))


class UPT9Tests(unittest.TestCase):
    def setUp(self):
        self.model = UPTMemoryDynamics(CYCLE4, coupling=0.7, memory_strength=1.2)

    def test_augmented_state_count(self):
        self.assertEqual(len(self.model.states), 80)

    def test_generator_rows_sum_to_zero(self):
        for row in self.model.generator():
            self.assertAlmostEqual(sum(row), 0.0, places=12)

    def test_off_diagonal_rates_nonnegative(self):
        for i, row in enumerate(self.model.generator()):
            self.assertTrue(all(v >= 0 for j, v in enumerate(row) if i != j))

    def test_single_coordinate_edges_are_bidirectional(self):
        a, b = ((0,0,0,0),0), ((1,0,0,0),0)
        self.assertGreater(self.model.transition_rate(a,b), 0)
        self.assertGreater(self.model.transition_rate(b,a), 0)

    def test_gibbs_distribution_satisfies_detailed_balance(self):
        self.assertLess(self.model.detailed_balance_residual(), 1e-12)

    def test_stationary_distribution_normalizes(self):
        self.assertAlmostEqual(sum(self.model.stationary_distribution()), 1.0, places=13)

    def test_stationary_distribution_is_left_null_vector(self):
        pi, q = self.model.stationary_distribution(), self.model.generator()
        for j in range(len(pi)):
            self.assertAlmostEqual(sum(pi[i]*q[i][j] for i in range(len(pi))), 0, places=11)

    def test_probability_evolution_preserves_mass_and_positivity(self):
        p = [0.0]*len(self.model.states)
        p[0] = 1.0
        evolved = self.model.evolve_uniformized(p, 0.4, 20)
        self.assertAlmostEqual(sum(evolved), 1.0, places=12)
        self.assertTrue(all(v >= 0 for v in evolved))

    def test_memory_changes_configuration_transition_rate(self):
        q = (0,0,0,0)
        a = self.model.transition_rate((q,0),((1,0,0,0),0))
        b = self.model.transition_rate((q,1),((1,0,0,0),1))
        self.assertNotAlmostEqual(a,b,places=12)

    def test_zero_memory_strength_removes_memory_dependence(self):
        model = UPTMemoryDynamics(CYCLE4, coupling=0.7, memory_strength=0)
        q = (0,0,0,0)
        a = model.transition_rate((q,0),((1,0,0,0),0))
        b = model.transition_rate((q,1),((1,0,0,0),1))
        self.assertAlmostEqual(a,b,places=14)

    def test_admissible_domain_can_expand_and_contract(self):
        self.assertEqual(len(self.model.active_count_domain(2)), 11)
        self.assertEqual(len(self.model.active_count_domain(0)), 5)

    def test_adaptive_and_memoryless_baselines_differ(self):
        q = (0,0,0,0)
        adaptive = self.model.transition_rate((q,0),((1,0,0,0),0))
        baseline = UPTMemoryDynamics(CYCLE4, coupling=0.7, memory_strength=0)
        self.assertNotAlmostEqual(adaptive,baseline.transition_rate((q,0),((1,0,0,0),0)))

    def test_rejects_invalid_parameters_and_probabilities(self):
        with self.assertRaises(ValueError):
            UPTMemoryDynamics(CYCLE4,memory_strength=-1)
        with self.assertRaises(ValueError):
            self.model.evolve_uniformized([0.1],1,10)


if __name__ == "__main__":
    unittest.main()
