import sys
import unittest
from math import exp
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.two_node_relational import TwoNodeRelationalModel


class TwoNodeRelationalTests(unittest.TestCase):
    def test_exact_solution_matches_closed_form_difference(self):
        model = TwoNodeRelationalModel((0.0, 2.0), coupling=0.3)
        self.assertAlmostEqual(model.consensus_error(1.5), 2.0 * exp(-0.9))

    def test_common_mode_is_invariant(self):
        model = TwoNodeRelationalModel((-2.0, 4.0), coupling=0.7)
        for time in (0.0, 0.1, 1.0, 10.0):
            self.assertAlmostEqual(model.common_mode(time), 1.0, places=14)

    def test_difference_decays_for_positive_coupling(self):
        model = TwoNodeRelationalModel((1.0, 5.0), coupling=0.2)
        self.assertLess(model.consensus_error(5.0), model.consensus_error(0.0))

    def test_relational_energy_is_nonincreasing(self):
        model = TwoNodeRelationalModel((-1.0, 3.0), coupling=0.4)
        energies = [model.relational_energy(t) for t in (0, 0.5, 1, 2, 5)]
        self.assertTrue(all(b <= a for a, b in zip(energies, energies[1:])))

    def test_zero_coupling_preserves_both_distinct_states(self):
        model = TwoNodeRelationalModel((2.0, 8.0), coupling=0.0)
        self.assertEqual(model.state(100.0), (2.0, 8.0))

    def test_invalid_initial_state_is_rejected(self):
        with self.assertRaises(ValueError):
            TwoNodeRelationalModel((1.0,), coupling=0.2)

    def test_negative_coupling_is_rejected(self):
        with self.assertRaises(ValueError):
            TwoNodeRelationalModel((1.0, 2.0), coupling=-0.1)

    def test_negative_time_is_rejected(self):
        model = TwoNodeRelationalModel((1.0, 2.0), coupling=0.2)
        with self.assertRaises(ValueError):
            model.state(-1.0)


if __name__ == "__main__":
    unittest.main()
