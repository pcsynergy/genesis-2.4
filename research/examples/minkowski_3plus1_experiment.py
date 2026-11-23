"""Run Experiment 11: 3+1 Minkowski covariance and stress-energy checks."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from research.tests.test_minkowski_3plus1 import Minkowski3Plus1Tests


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Minkowski3Plus1Tests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("Experiment 11 passed: 3+1 scalar action, boosts, stress-energy, and conservation identity.")
