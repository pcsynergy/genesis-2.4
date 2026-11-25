import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from examples.symphony_harmonic_null_comparison import run_case

class SymphonyNullComparisonTests(unittest.TestCase):
    def test_uncoupled_and_coupled_predictions_are_distinct(self):
        null = run_case(0.0)
        coupled = run_case(1.0)
        self.assertEqual(len(null), 4)
        self.assertEqual(len(coupled), 4)
        self.assertTrue(all(0.0 <= x <= 1.0 for x in null + coupled))
        self.assertGreater(sum(coupled) / 4.0, sum(null) / 4.0 + 0.5)

    def test_null_run_is_deterministic(self):
        self.assertEqual(run_case(0.0), run_case(0.0))

if __name__ == "__main__":
    unittest.main()
