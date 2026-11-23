"""Run Experiment 12: prescribed-FLRW curved-background consistency checks."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import unittest
from research.tests.test_flrw_curved import TestFLRWCurvedBackground


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        TestFLRWCurvedBackground
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("Experiment 12 passed: prescribed-FLRW identities and limits.")
