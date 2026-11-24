import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.upt8_renewed_potential import UPTAdaptivePotentialSpace


CYCLE4 = (
    (0, 1, 0, 1),
    (1, 0, 1, 0),
    (0, 1, 0, 1),
    (1, 0, 1, 0),
)


class UPT8RenewedPotentialTests(unittest.TestCase):
    def setUp(self):
        self.model = UPTAdaptivePotentialSpace(CYCLE4, initial_active_count=2)

    def test_initial_domain_matches_upt7_six_states(self):
        self.assertEqual(len(self.model.initial_domain), 6)
        self.assertTrue(all(sum(q) == 2 for q in self.model.initial_domain))

    def test_first_renewal_admits_four_three_active_states(self):
        history = self.model.domain_history(1)
        self.assertEqual([len(domain) for domain in history], [6, 10])
        self.assertEqual(sum(sum(q) == 3 for q in history[-1]), 4)

    def test_second_renewal_admits_fully_active_state(self):
        history = self.model.domain_history(2)
        self.assertEqual([len(domain) for domain in history], [6, 10, 11])
        self.assertIn((1, 1, 1, 1), history[-1])

    def test_domain_is_monotone_and_finite_closure_is_reached(self):
        history = self.model.domain_history(8)
        for previous, current in zip(history, history[1:]):
            self.assertTrue(set(previous).issubset(set(current)))
        self.assertEqual(len(history[-1]), 11)
        self.assertEqual(self.model.renewal_step(history[-1]), history[-1])

    def test_zero_edge_graph_does_not_renew(self):
        empty = ((0, 0, 0, 0),) * 4
        model = UPTAdaptivePotentialSpace(empty, initial_active_count=2)
        history = model.domain_history(4)
        self.assertEqual([len(domain) for domain in history], [6, 6])

    def test_activation_requires_threshold_support(self):
        model = UPTAdaptivePotentialSpace(
            CYCLE4, initial_active_count=2, activation_threshold=2.1
        )
        self.assertEqual(len(model.domain_history(1)[-1]), 6)

    def test_distribution_normalizes_on_each_domain(self):
        for domain in self.model.domain_history(2):
            self.assertAlmostEqual(
                sum(p for _, p in self.model.distribution(domain)), 1.0, places=14
            )

    def test_zero_coupling_is_uniform_on_each_domain(self):
        model = UPTAdaptivePotentialSpace(
            CYCLE4, initial_active_count=2, coupling=0.0
        )
        domain = model.domain_history(2)[-1]
        probabilities = [p for _, p in model.distribution(domain)]
        self.assertTrue(all(abs(p - 1.0 / len(domain)) < 1e-14 for p in probabilities))

    def test_rejects_invalid_threshold_and_asymmetric_graph(self):
        with self.assertRaises(ValueError):
            UPTAdaptivePotentialSpace(CYCLE4, 2, activation_threshold=0.0)
        with self.assertRaises(ValueError):
            UPTAdaptivePotentialSpace(((0, 1), (0, 0)), 1)

    def test_rejects_empty_domain_and_invalid_state(self):
        with self.assertRaises(ValueError):
            self.model.renewal_step(())
        with self.assertRaises(ValueError):
            self.model.renewal_step(((1, 0),))


if __name__ == "__main__":
    unittest.main()
