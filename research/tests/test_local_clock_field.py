import unittest
from one_time_field.local_clock_field import LocalClockFieldSystem, refinement_experiment


class LocalClockFieldTests(unittest.TestCase):
    def test_energy_drift_bounded(self):
        s=LocalClockFieldSystem(node_count=32)
        e0=s.energy()
        for _ in range(250):
            s.step(0.001)
        self.assertLess(abs(s.energy()-e0),1e-5)

    def test_uncoupled_domains_evolve_without_cross_source(self):
        s=LocalClockFieldSystem(node_count=16,coupling=0.0)
        a0=s.accelerations()
        self.assertEqual(len(a0[0]),16)
        self.assertEqual(len(a0[1]),16)

    def test_invalid_dt_rejected(self):
        with self.assertRaises(ValueError):
            LocalClockFieldSystem().step(0.0)

    def test_refinement_outputs_finite(self):
        rows,ref=refinement_experiment(final_time=0.08,counts=(16,32,64))
        self.assertEqual(len(rows),2)
        self.assertEqual(ref["nodes"],64)
        for row in rows:
            for key in ("field_rms_error","clock_rms_error","energy_drift"):
                self.assertTrue(row[key]>=0.0)


if __name__=="__main__":
    unittest.main()
