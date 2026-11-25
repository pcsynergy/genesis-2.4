import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field import PhaseOscillatorNetwork


def graph(kind, n):
    matrix = [[0.0] * n for _ in range(n)]
    if kind == "complete":
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j] = matrix[j][i] = 1.0
    elif kind == "ring":
        for i in range(n):
            j = (i + 1) % n
            matrix[i][j] = matrix[j][i] = 1.0
    elif kind == "path":
        for i in range(n - 1):
            matrix[i][i + 1] = matrix[i + 1][i] = 1.0
    return matrix


def run_case(topology, slope, coupling, steps=5000, dt=0.01):
    n = 10
    phases = [0.0, 0.2, 0.8, 1.7, 2.1, 3.4, 4.8, 5.5, 5.9, 3.0]
    frequencies = [1.0 + slope * (i - (n - 1) / 2.0) for i in range(n)]
    model = PhaseOscillatorNetwork(graph(topology, n), phases, frequencies, coupling)
    initial = model.order_parameter()
    model.run(steps, dt)
    return initial, model.order_parameter()


class SymphonyRobustnessTests(unittest.TestCase):
    def test_complete_graph_synchronizes_moderate_frequency_dispersion(self):
        initial, final = run_case("complete", 0.02, 0.5)
        self.assertGreater(final, 0.99)
        self.assertGreater(final, initial + 0.8)

    def test_stronger_coupling_overcomes_larger_dispersion_in_complete_graph(self):
        _, weak = run_case("complete", 0.15, 0.5)
        _, strong = run_case("complete", 0.15, 2.0)
        self.assertGreater(strong, weak + 0.4)
        self.assertGreater(strong, 0.95)

    def test_path_graph_reaches_high_coherence_at_strong_coupling(self):
        _, final = run_case("path", 0.02, 2.0)
        self.assertGreater(final, 0.85)

    def test_ring_can_retain_twisted_low_global_coherence_state(self):
        _, final = run_case("ring", 0.0, 1.0)
        self.assertLess(final, 0.05)

    def test_coherence_is_bounded_for_each_topology(self):
        for topology in ("complete", "path", "ring"):
            _, final = run_case(topology, 0.02, 1.0)
            self.assertGreaterEqual(final, 0.0)
            self.assertLessEqual(final, 1.0)


if __name__ == "__main__":
    unittest.main()
