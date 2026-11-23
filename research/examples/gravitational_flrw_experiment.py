"""Run Experiment 13: metric variation and dynamical FLRW gravity."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import unittest
from research.tests.test_gravitational_flrw import TestDynamicalGravityFLRW
if __name__ == "__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(TestDynamicalGravityFLRW)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful(): raise SystemExit(1)
    print("Experiment 13 passed: FLRW Einstein-equation consistency checks.")
