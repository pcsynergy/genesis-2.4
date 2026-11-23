import unittest
from one_time_field.continuum_action import ContinuumClockFieldSystem, refinement_experiment


class ContinuumActionTests(unittest.TestCase):
    def test_energy_drift_is_bounded(self):
        s = ContinuumClockFieldSystem(node_count=32)
        e0 = s.energy()
        for _ in range(300):
            s.step(0.002)
        self.assertLess(abs(s.energy()-e0), 2e-4)

    def test_uncoupled_clock_is_harmonic(self):
        s = ContinuumClockFieldSystem(node_count=16, coupling=0.0, clock=0.2,
                                      clock_velocity=0.03, clock_stiffness=1.0)
        e0 = s.energy()
        for _ in range(1000):
            s.step(0.001)
        self.assertLess(abs(s.energy()-e0), 1e-6)

    def test_invalid_step_rejected(self):
        s = ContinuumClockFieldSystem()
        with self.assertRaises(ValueError):
            s.step(0.0)

    def test_refinement_returns_finite_errors(self):
        rows, ref = refinement_experiment(final_time=0.1, counts=(16, 32, 64))
        self.assertEqual(len(rows), 2)
        self.assertEqual(ref["nodes"], 64)
        for row in rows:
            self.assertGreaterEqual(row["field_rms_error"], 0.0)
            self.assertTrue(row["energy_drift"] >= 0.0)


if __name__ == "__main__":
    unittest.main()
