import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.temporal import TemporalLayer


class TemporalLayerTests(unittest.TestCase):
    def test_zero_activity_clocks_match_parameter_time(self):
        layer = TemporalLayer(relational_gain=2.0, observer_gain=0.5)
        state = layer.advance(0.25, 0.0)
        self.assertAlmostEqual(state["parameter_time"], 0.25)
        self.assertAlmostEqual(state["relational_time"], 0.25)
        self.assertAlmostEqual(state["observer_time"], 0.25)

    def test_activity_changes_relational_and_observer_rates(self):
        layer = TemporalLayer(relational_gain=0.5, observer_gain=0.2,
                              reference_activity=1.0)
        state = layer.advance(0.5, 3.0)
        self.assertAlmostEqual(state["parameter_time"], 0.5)
        self.assertAlmostEqual(state["relational_time"], 1.25)
        self.assertAlmostEqual(state["observer_time"], 0.7)
        self.assertAlmostEqual(state["accumulated_activity"], 1.5)

    def test_observer_rate_has_positive_floor(self):
        layer = TemporalLayer(observer_gain=-10.0, reference_activity=1.0,
                              min_observer_rate=0.1)
        self.assertAlmostEqual(layer.advance(1.0, 10.0)["observer_time"], 0.1)

    def test_invalid_inputs_are_rejected(self):
        layer = TemporalLayer()
        for dt, activity in ((0.0, 0.0), (1.0, -1.0), (float("nan"), 0.0)):
            with self.assertRaises(ValueError):
                layer.advance(dt, activity)

    def test_snapshot_is_detached(self):
        layer = TemporalLayer()
        state = layer.snapshot()
        state["parameter_time"] = 100
        self.assertEqual(layer.parameter_time, 0.0)


if __name__ == "__main__":
    unittest.main()
