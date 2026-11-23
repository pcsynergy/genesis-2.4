"""Run Experiment 9: Lorentz-covariant scalar/clock field checks."""
from pathlib import Path
import sys
import unittest

# When invoked as a script, Python places research/examples on sys.path.
# Add the repository root so the research namespace package is importable.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from research.tests.test_lorentz_covariant import LorentzCovarianceTests


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(LorentzCovarianceTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("Experiment 9 passed: action density and field equations are boost invariant.")
