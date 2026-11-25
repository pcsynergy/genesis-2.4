import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "examples"))
from symphony_harmonic_thresholds import (
    PHASE_SETS, graph, local_edge_alignment, run_case, sweep,
)


class SymphonyThresholdTests(unittest.TestCase):
    def test_sweep_has_full_deterministic_grid(self):
        rows = list(sweep())
        self.assertEqual(len(rows), 3 * 4 * 8 * 4)
        self.assertEqual(len(rows), len(list(sweep())))

    def test_observables_are_bounded(self):
        for topology, dispersion, coupling, start_id, global_r, local_q in sweep():
            self.assertGreaterEqual(global_r, 0.0)
            self.assertLessEqual(global_r, 1.0)
            self.assertGreaterEqual(local_q, 0.0)
            self.assertLessEqual(local_q, 1.0)

    def test_ring_twist_can_have_high_local_but_low_global_coherence(self):
        phases = tuple((2.0 * 3.141592653589793 * i / 10) for i in range(10))
        adjacency = graph("ring")
        global_r, local_q = run_case("ring", 0.0, 1.0, phases, steps=1)
        # At the evenly spaced twist, neighboring edge phase differences are small
        # and similarly directed; the local edge score can exceed the global order.
        self.assertLess(global_r, 0.1)
        self.assertGreater(local_q, global_r)

    def test_initial_phase_sets_are_distinct(self):
        self.assertEqual(len({tuple(x) for x in PHASE_SETS}), len(PHASE_SETS))

    def test_invalid_topology_rejected(self):
        with self.assertRaises(ValueError):
            graph("grid")


if __name__ == "__main__":
    unittest.main()
