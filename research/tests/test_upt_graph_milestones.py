import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field import GraphFieldNetwork


def disagreement(values):
    mean = sum(values) / len(values)
    return sum((value - mean) ** 2 for value in values)


def run_network(adjacency, initial, coupling=1.0, dt=0.01, steps=5000):
    model = GraphFieldNetwork(adjacency, initial, coupling=coupling)
    model.run(steps, dt)
    return list(model.state)


class UPTGraphMilestoneTests(unittest.TestCase):
    def test_connected_path_converges_to_global_mean(self):
        adjacency = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        final = run_network(adjacency, [0.0, 2.0, 7.0], dt=0.01, steps=5000)
        self.assertTrue(all(abs(x - 3.0) < 1e-8 for x in final))

    def test_disconnected_graph_converges_within_each_component(self):
        adjacency = [
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
        ]
        final = run_network(adjacency, [0.0, 2.0, 4.0, 10.0], dt=0.01, steps=3000)
        self.assertAlmostEqual(final[0], 1.0, places=8)
        self.assertAlmostEqual(final[1], 1.0, places=8)
        self.assertAlmostEqual(final[2], 7.0, places=8)
        self.assertAlmostEqual(final[3], 7.0, places=8)

    def test_arithmetic_mean_is_conserved_on_symmetric_weighted_graph(self):
        adjacency = [[0, 2, 1], [2, 0, 3], [1, 3, 0]]
        initial = [-2.0, 1.0, 8.0]
        final = run_network(adjacency, initial, coupling=0.2, dt=0.01, steps=100)
        self.assertAlmostEqual(sum(final) / 3, sum(initial) / 3, places=12)

    def test_disagreement_is_nonincreasing_under_stable_step(self):
        adjacency = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        model = GraphFieldNetwork(adjacency, [0.0, 2.0, 9.0], coupling=0.4)
        previous = disagreement(model.state)
        for _ in range(100):
            model.step(0.01)
            current = disagreement(model.state)
            self.assertLessEqual(current, previous + 1e-12)
            previous = current

    def test_coupled_and_uncoupled_observable_predictions_differ(self):
        adjacency = [[0, 1], [1, 0]]
        initial = [0.0, 2.0]
        coupled = run_network(adjacency, initial, coupling=0.5, dt=0.01, steps=1000)
        uncoupled = run_network(adjacency, initial, coupling=0.0, dt=0.01, steps=1000)
        self.assertLess(disagreement(coupled), 1e-6)
        self.assertAlmostEqual(disagreement(uncoupled), disagreement(initial), places=12)

    def test_zero_coupling_preserves_every_node_state(self):
        adjacency = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        initial = [3.0, -1.0, 8.0]
        self.assertEqual(run_network(adjacency, initial, coupling=0.0), initial)

    def test_stability_bound_is_satisfied_by_experiment_step(self):
        # For a symmetric nonnegative graph, lambda_max(L) <= 2*d_max.
        adjacency = [[0, 2, 1], [2, 0, 3], [1, 3, 0]]
        max_degree = max(sum(row) for row in adjacency)
        coupling, dt = 0.2, 0.01
        self.assertLessEqual(dt * coupling * max_degree, 1.0)


if __name__ == "__main__":
    unittest.main()
