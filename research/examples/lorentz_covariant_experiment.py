"""Run Experiment 9: Lorentz-covariant scalar/clock field checks."""
import unittest

from research.tests.test_lorentz_covariant import LorentzCovarianceTests


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(LorentzCovarianceTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("Experiment 9 passed: action density and field equations are boost invariant.")
