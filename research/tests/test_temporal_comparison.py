import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.temporal_comparison import run_comparison


class TemporalComparisonTests(unittest.TestCase):
    def test_same_initial_state_and_reparameterized_dynamics_match(self):
        rows = run_comparison(steps=100, d_lambda=0.01, gain=0.25)
        self.assertEqual(len(rows), 101)
        self.assertLessEqual(max(row["max_state_error"] for row in rows), 1e-12)

    def test_relational_clock_is_monotonic_and_distinct(self):
        rows = run_comparison(steps=100, d_lambda=0.01, gain=0.25)
        taus = [row["tau"] for row in rows]
        lambdas = [row["lambda"] for row in rows]
        self.assertTrue(all(b > a for a, b in zip(taus, taus[1:])))
        self.assertTrue(all(b > a for a, b in zip(lambdas, lambdas[1:])))
        self.assertGreater(taus[-1], lambdas[-1])

    def test_zero_gain_reduces_to_baseline_clock(self):
        rows = run_comparison(steps=20, d_lambda=0.02, gain=0.0, baseline=1.0)
        self.assertAlmostEqual(rows[-1]["tau"], rows[-1]["lambda"])
        self.assertLessEqual(rows[-1]["max_state_error"], 1e-12)

    def test_invalid_inputs_are_rejected(self):
        for kwargs in (
            {"steps": -1}, {"d_lambda": 0.0}, {"gain": -0.1},
            {"baseline": 0.0},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                run_comparison(**kwargs)


if __name__ == "__main__":
    unittest.main()
