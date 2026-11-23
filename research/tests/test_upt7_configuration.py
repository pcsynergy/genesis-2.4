import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.upt7_configuration import UPTConfigurationEnsemble


CYCLE4 = (
    (0, 1, 0, 1),
    (1, 0, 1, 0),
    (0, 1, 0, 1),
    (1, 0, 1, 0),
)


class UPT7ConfigurationTests(unittest.TestCase):
    def test_fixed_count_defines_six_admissible_states(self):
        model = UPTConfigurationEnsemble(CYCLE4, active_count=2)
        self.assertEqual(len(model.admissible_states), 6)
        self.assertTrue(all(sum(q) == 2 for q in model.admissible_states))

    def test_probability_distribution_is_normalized(self):
        model = UPTConfigurationEnsemble(CYCLE4, active_count=2, coupling=0.8)
        self.assertAlmostEqual(sum(p for _, p in model.distribution()), 1.0, places=14)

    def test_zero_coupling_recovers_uniform_baseline(self):
        model = UPTConfigurationEnsemble(CYCLE4, active_count=2, coupling=0.0)
        self.assertAlmostEqual(model.expected_cut(), 8.0 / 3.0, places=14)
        self.assertAlmostEqual(model.expected_coherence(), 1.0 / 3.0, places=14)

    def test_positive_coupling_favors_relationally_coherent_states(self):
        baseline = UPTConfigurationEnsemble(CYCLE4, active_count=2, coupling=0.0)
        coupled = UPTConfigurationEnsemble(CYCLE4, active_count=2, coupling=1.0)
        self.assertGreater(coupled.expected_coherence(), baseline.expected_coherence())
        self.assertLess(coupled.expected_cut(), baseline.expected_cut())

    def test_fixed_count_constraint_is_preserved_by_admissible_domain(self):
        model = UPTConfigurationEnsemble(CYCLE4, active_count=2)
        self.assertTrue(all(sum(state) == 2 for state in model.admissible_states))

    def test_rejects_non_admissible_state(self):
        model = UPTConfigurationEnsemble(CYCLE4, active_count=2)
        with self.assertRaises(ValueError):
            model.relational_energy((1, 0, 0, 0))

    def test_rejects_asymmetric_relation_matrix(self):
        with self.assertRaises(ValueError):
            UPTConfigurationEnsemble(((0, 1), (0, 0)), active_count=1)

    def test_coupling_zero_makes_all_admissible_states_equiprobable(self):
        model = UPTConfigurationEnsemble(CYCLE4, active_count=2, coupling=0.0)
        probabilities = [p for _, p in model.distribution()]
        self.assertTrue(all(abs(p - 1.0 / 6.0) < 1e-14 for p in probabilities))


if __name__ == "__main__":
    unittest.main()
