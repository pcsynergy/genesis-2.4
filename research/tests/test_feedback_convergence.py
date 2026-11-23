import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.feedback_convergence import (
    run_convergence_study, run_feedback_pair, run_strength_sweep,
)


class FeedbackConvergenceTests(unittest.TestCase):
    def test_zero_feedback_matches_control(self):
        result = run_feedback_pair(0.01, final_lambda=0.2, feedback_gain=0.0)
        self.assertLessEqual(result["state_distance"], 1e-14)

    def test_refinement_results_are_finite_and_same_horizon(self):
        rows = run_convergence_study((0.02, 0.01, 0.005), final_lambda=0.2)
        self.assertEqual([row["steps"] for row in rows], [10.0, 20.0, 40.0])
        self.assertTrue(all(row["state_distance"] >= 0 for row in rows))
        self.assertTrue(all(row["final_lambda"] == 0.2 for row in rows))

    def test_strength_sweep_has_zero_and_nonzero_response(self):
        rows = run_strength_sweep((0.0, 0.05), dt=0.01, final_lambda=0.2)
        self.assertLessEqual(rows[0]["state_distance"], 1e-14)
        self.assertGreater(rows[1]["state_distance"], 0.0)

    def test_invalid_step_schedule_rejected(self):
        with self.assertRaises(ValueError):
            run_convergence_study((0.01, 0.02), final_lambda=0.1)


if __name__ == "__main__":
    unittest.main()
