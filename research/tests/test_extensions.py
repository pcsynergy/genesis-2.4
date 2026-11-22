import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.harmonic import PhaseOscillatorNetwork
from one_time_field.tensor import TensorFieldNetwork


class HarmonicNetworkTests(unittest.TestCase):
    def test_identical_phases_remain_identical(self):
        model = PhaseOscillatorNetwork([[0, 1], [1, 0]], [0.5, 0.5], [1, 1], 2)
        model.run(20, 0.01)
        self.assertAlmostEqual(model.phases[0], model.phases[1])
        self.assertAlmostEqual(model.order_parameter(), 1.0)

    def test_coupling_reduces_two_node_phase_difference(self):
        model = PhaseOscillatorNetwork([[0, 1], [1, 0]], [0, 1], [0, 0], 1)
        initial = abs(model.phases[1] - model.phases[0])
        model.run(10, 0.01)
        self.assertLess(abs(model.phases[1] - model.phases[0]), initial)

    def test_phase_wraps_into_canonical_interval(self):
        model = PhaseOscillatorNetwork([[0]], [6.2], [2.0])
        model.step(1.0)
        self.assertGreaterEqual(model.phases[0], 0)
        self.assertLess(model.phases[0], 2 * math.pi)

    def test_bad_frequency_count_is_rejected(self):
        with self.assertRaises(ValueError):
            PhaseOscillatorNetwork([[0, 1], [1, 0]], [0, 1], [0])


class TensorNetworkTests(unittest.TestCase):
    def test_vector_components_evolve_independently_and_conserve_means(self):
        model = TensorFieldNetwork([[0, 1], [1, 0]], [[0, 2, 4], [2, 4, 6]], (3,), 0.1)
        means = [(model.state[0][k] + model.state[1][k]) / 2 for k in range(3)]
        model.run(10, 0.01)
        for k, expected in enumerate(means):
            self.assertAlmostEqual((model.state[0][k] + model.state[1][k]) / 2, expected, places=12)

    def test_rank_two_shape_is_checked(self):
        model = TensorFieldNetwork([[0]], [[1, 2, 3, 4]], (2, 2))
        self.assertEqual(model.component_count, 4)
        with self.assertRaises(ValueError):
            TensorFieldNetwork([[0]], [[1, 2, 3]], (2, 2))

    def test_tensor_decay_reduces_components(self):
        model = TensorFieldNetwork([[0]], [[1, 2]], (2,), decay=0.5)
        model.step(0.1)
        self.assertAlmostEqual(model.state[0][0], 0.95)
        self.assertAlmostEqual(model.state[0][1], 1.9)


if __name__ == "__main__":
    unittest.main()
