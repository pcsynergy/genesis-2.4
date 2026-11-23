import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.temporal_models import (
    EntropyProductionClock, EventClock, ExternalClock, HybridClock,
    ObserverClock, RelationalClock,
)


class ComparativeClockTests(unittest.TestCase):
    def test_external_clock_tracks_parameter(self):
        clock = ExternalClock()
        self.assertAlmostEqual(clock.advance(0.25), 0.25)

    def test_relational_clock_and_chain_rule(self):
        clock = RelationalClock()
        self.assertAlmostEqual(clock.advance(0.5, 2.0), 1.0)
        self.assertAlmostEqual(RelationalClock.reparameterized_rhs(6.0, 2.0), 3.0)

    def test_relational_rate_must_be_positive(self):
        with self.assertRaises(ValueError):
            RelationalClock().advance(1.0, 0.0)

    def test_entropy_production_clock_is_monotonic(self):
        clock = EntropyProductionClock()
        self.assertAlmostEqual(clock.advance(2.0, 0.4), 0.8)
        with self.assertRaises(ValueError):
            clock.advance(1.0, -0.1)

    def test_event_clock_counts_discrete_events(self):
        clock = EventClock()
        self.assertEqual(clock.advance(3), 3)
        with self.assertRaises(ValueError):
            clock.advance(-1)

    def test_observer_clock_is_separate_proxy(self):
        physical = ExternalClock()
        observer = ObserverClock(minimum_rate=0.1)
        physical.advance(1.0)
        observer.advance(1.0, activity=3.0, sensitivity=0.5, reference=1.0)
        self.assertAlmostEqual(physical.reading, 1.0)
        self.assertAlmostEqual(observer.reading, 2.0)

    def test_hybrid_preserves_distinct_readings(self):
        clocks = HybridClock(
            external=ExternalClock(1.0),
            relational=RelationalClock(1.5),
            entropy=EntropyProductionClock(0.2),
            events=EventClock(4),
            observer=ObserverClock(0.8),
        )
        self.assertEqual(clocks.snapshot(), {
            "external": 1.0, "relational": 1.5, "entropy": 0.2,
            "events": 4, "observer": 0.8,
        })


if __name__ == "__main__":
    unittest.main()
