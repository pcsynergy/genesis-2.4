import unittest

from one_time_field import GraphFieldNetwork


class GraphFieldNetworkTests(unittest.TestCase):
    def test_identical_states_remain_identical(self):
        model = GraphFieldNetwork([[0, 1], [1, 0]], [2, 2], coupling=1.0)
        model.run(10, 0.01)
        self.assertAlmostEqual(model.state[0], 2.0)
        self.assertAlmostEqual(model.state[1], 2.0)

    def test_symmetric_coupling_preserves_mean_without_decay(self):
        model = GraphFieldNetwork([[0, 1], [1, 0]], [0, 2], coupling=0.2)
        initial_mean = model.mean_state()
        model.run(20, 0.01)
        self.assertAlmostEqual(model.mean_state(), initial_mean, places=12)
        self.assertLess(abs(model.state[0] - model.state[1]), 2.0)

    def test_decay_reduces_positive_state(self):
        model = GraphFieldNetwork([[0]], [1], decay=0.5)
        model.run(10, 0.01)
        self.assertLess(model.state[0], 1.0)
        self.assertGreater(model.state[0], 0.0)

    def test_source_changes_state(self):
        model = GraphFieldNetwork([[0]], [0])
        model.step(0.1, source=[2.0])
        self.assertAlmostEqual(model.state[0], 0.2)

    def test_disconnected_nodes_evolve_independently(self):
        model = GraphFieldNetwork([[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                                  [1, 2, 3], decay=0.1)
        model.step(0.1)
        self.assertAlmostEqual(model.state[0], 0.99)
        self.assertAlmostEqual(model.state[1], 1.98)
        self.assertAlmostEqual(model.state[2], 2.97)

    def test_invalid_asymmetric_graph_is_rejected(self):
        with self.assertRaises(ValueError):
            GraphFieldNetwork([[0, 1], [0, 0]], [0, 1])

    def test_invalid_time_step_is_rejected(self):
        model = GraphFieldNetwork([[0]], [1])
        with self.assertRaises(ValueError):
            model.step(0.0)

    def test_source_dimension_is_checked(self):
        model = GraphFieldNetwork([[0, 1], [1, 0]], [0, 1])
        with self.assertRaises(ValueError):
            model.step(0.1, source=[1.0])


if __name__ == "__main__":
    unittest.main()
