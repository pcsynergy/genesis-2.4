import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.temporal_coupling import run_coupling_experiment


class TemporalCouplingTests(unittest.TestCase):
    def test_zero_feedback_matches_control(self):
        rows = run_coupling_experiment(steps=30, feedback_gain=0.0)
        self.assertTrue(all(row["state_distance"] <= 1e-14 for row in rows))

    def test_nonzero_feedback_changes_field_trajectory(self):
        rows = run_coupling_experiment(
            steps=100, dt=0.01, clock_gain=0.25, feedback_gain=0.05
        )
        self.assertGreater(rows[-1]["state_distance"], 1e-8)
        self.assertGreater(rows[-1]["feedback_source"], 0.0)

    def test_zero_clock_gain_produces_no_clock_excess_feedback(self):
        rows = run_coupling_experiment(
            steps=30, clock_gain=0.0, feedback_gain=0.5
        )
        self.assertTrue(all(abs(row["feedback_source"]) <= 1e-14 for row in rows))
        self.assertTrue(all(row["state_distance"] <= 1e-14 for row in rows))

    def test_all_reported_values_remain_finite(self):
        rows = run_coupling_experiment(steps=100)
        self.assertTrue(all(
            value == value and abs(value) < float("inf")
            for row in rows for value in row.values()
        ))

    def test_invalid_parameters_are_rejected(self):
        for kwargs in (
            {"steps": -1}, {"dt": 0.0}, {"clock_gain": -1.0},
            {"clock_baseline": 0.0}, {"feedback_gain": -0.1},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                run_coupling_experiment(**kwargs)


if __name__ == "__main__":
    unittest.main()
