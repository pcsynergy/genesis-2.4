import sys
import unittest
from math import pi
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field import PhaseOscillatorNetwork


def complete_graph(n):
    return [[0.0 if i == j else 1.0 for j in range(n)] for i in range(n)]


class PhaseOscillatorNetworkTests(unittest.TestCase):
    def test_order_parameter_is_bounded(self):
        model = PhaseOscillatorNetwork([[0, 1], [1, 0]], [0, pi], [1, 1])
        self.assertGreaterEqual(model.order_parameter(), 0.0)
        self.assertLessEqual(model.order_parameter(), 1.0)

    def test_uncoupled_identical_frequency_network_preserves_coherence(self):
        phases = [0.0, pi / 2, pi, 3 * pi / 2]
        model = PhaseOscillatorNetwork(complete_graph(4), phases, [1, 1, 1, 1], 0.0)
        initial = model.order_parameter()
        model.run(100, 0.01)
        self.assertAlmostEqual(model.order_parameter(), initial, places=12)

    def test_coupling_increases_coherence_for_equal_frequency_spread_state(self):
        n = 8
        phases = [0.0, 0.2, 0.8, 1.7, 2.1, 3.4, 4.8, 5.5]
        frequencies = [1.0] * n
        model = PhaseOscillatorNetwork(complete_graph(n), phases, frequencies, 1.0)
        initial = model.order_parameter()
        model.run(500, 0.01)
        self.assertGreater(model.order_parameter(), initial + 0.5)
        self.assertGreater(model.order_parameter(), 0.95)

    def test_frequency_mismatch_can_be_synchronized_by_coupling(self):
        n = 8
        phases = [2 * pi * i / n for i in range(n)]
        frequencies = [1.0 + 0.03 * (i - (n - 1) / 2.0) for i in range(n)]
        model = PhaseOscillatorNetwork(complete_graph(n), phases, frequencies, 0.5)
        model.run(3000, 0.01)
        self.assertGreater(model.order_parameter(), 0.98)

    def test_invalid_negative_coupling_and_zero_dt_are_rejected(self):
        with self.assertRaises(ValueError):
            PhaseOscillatorNetwork([[0]], [0], [1], -1)
        model = PhaseOscillatorNetwork([[0]], [0], [1])
        with self.assertRaises(ValueError):
            model.step(0.0)


if __name__ == "__main__":
    unittest.main()
