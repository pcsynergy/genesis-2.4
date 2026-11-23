"""Run Experiment 10: stress-energy and on-shell conservation checks."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from research.tests.test_stress_energy import StressEnergyTests


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(StressEnergyTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("Experiment 10 passed: symmetric stress-energy tensor; divergence vanishes on shell.")
