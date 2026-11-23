import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.engine import DimensionalFieldEngine
from one_time_field.harmonic import PhaseOscillatorNetwork
from one_time_field.network import GraphFieldNetwork
from one_time_field.tensor import TensorFieldNetwork


class DimensionalFieldEngineTests(unittest.TestCase):
    def make_models(self):
        graph = [[0, 1], [1, 0]]
        scalar = GraphFieldNetwork(graph, [2.0, 2.0], coupling=0.0)
        harmonic = PhaseOscillatorNetwork(graph, [0.0, 0.0], [0.0, 0.0], coupling=0.0)
        tensor = TensorFieldNetwork(graph, [[1.0, 2.0], [3.0, 4.0]], (2,), coupling=1.0)
        return scalar, harmonic, tensor

    def test_shared_topology_and_snapshot(self):
        scalar, harmonic, tensor = self.make_models()
        engine = DimensionalFieldEngine(scalar, harmonic, tensor)
        snapshot = engine.snapshot()
        self.assertEqual(snapshot["scalar"], [2.0, 2.0])
        self.assertEqual(snapshot["harmonic"], [0.0, 0.0])
        self.assertEqual(snapshot["tensor"], [[1.0, 2.0], [3.0, 4.0]])
        snapshot["tensor"][0][0] = 999
        self.assertEqual(tensor.state[0][0], 1.0)

    def test_scalar_mean_modulates_phase_frequency(self):
        scalar, harmonic, _ = self.make_models()
        engine = DimensionalFieldEngine(
            scalar=scalar, harmonic=harmonic, scalar_to_phase_gain=0.5
        )
        engine.step(0.1)
        self.assertAlmostEqual(harmonic.phases[0], 0.1)
        self.assertAlmostEqual(harmonic.phases[1], 0.1)
        self.assertEqual(harmonic.natural_frequencies, [0.0, 0.0])

    def test_phase_coherence_drives_scalar_source(self):
        graph = [[0, 1], [1, 0]]
        scalar = GraphFieldNetwork(graph, [0.0, 0.0], coupling=0.0)
        harmonic = PhaseOscillatorNetwork(graph, [0.2, 0.2], [0.0, 0.0], coupling=0.0)
        engine = DimensionalFieldEngine(
            scalar=scalar, harmonic=harmonic, coherence_to_scalar_gain=2.0
        )
        engine.step(0.1)
        self.assertAlmostEqual(scalar.state[0], 0.2)
        self.assertAlmostEqual(scalar.state[1], 0.2)

    def test_tensor_domain_advances_on_shared_graph(self):
        _, _, tensor = self.make_models()
        engine = DimensionalFieldEngine(tensor=tensor)
        engine.step(0.1)
        self.assertAlmostEqual(tensor.state[0][0], 1.2)
        self.assertAlmostEqual(tensor.state[1][0], 2.8)

    def test_mismatched_topologies_are_rejected(self):
        scalar = GraphFieldNetwork([[0, 1], [1, 0]], [1, 1])
        harmonic = PhaseOscillatorNetwork([[0, 0], [0, 0]], [0, 0], [0, 0])
        with self.assertRaises(ValueError):
            DimensionalFieldEngine(scalar=scalar, harmonic=harmonic)

    def test_cross_coupling_requires_both_domains(self):
        scalar = GraphFieldNetwork([[0]], [1])
        with self.assertRaises(ValueError):
            DimensionalFieldEngine(scalar=scalar, scalar_to_phase_gain=1.0)

    def test_external_scalar_source_is_additive(self):
        graph = [[0, 1], [1, 0]]
        scalar = GraphFieldNetwork(graph, [0.0, 0.0], coupling=0.0)
        harmonic = PhaseOscillatorNetwork(graph, [0.0, 0.0], [0.0, 0.0], coupling=0.0)
        engine = DimensionalFieldEngine(
            scalar=scalar, harmonic=harmonic, coherence_to_scalar_gain=2.0
        )
        engine.step(0.1, scalar_external_source=[1.0, 0.5])
        self.assertAlmostEqual(scalar.state[0], 0.3)
        self.assertAlmostEqual(scalar.state[1], 0.25)

    def test_invalid_external_scalar_source_is_rejected(self):
        engine = DimensionalFieldEngine(scalar=GraphFieldNetwork([[0, 1], [1, 0]], [0, 0]))
        with self.assertRaises(ValueError):
            engine.step(0.1, scalar_external_source=[1.0])

    def test_invalid_time_step_is_rejected(self):
        engine = DimensionalFieldEngine(scalar=GraphFieldNetwork([[0]], [1]))
        with self.assertRaises(ValueError):
            engine.step(0.0)

    def test_run_includes_initial_state(self):
        engine = DimensionalFieldEngine(scalar=GraphFieldNetwork([[0]], [1]))
        history = engine.run(3, 0.1)
        self.assertEqual(len(history), 4)
        self.assertAlmostEqual(history[0]["scalar"][0], 1.0)


if __name__ == "__main__":
    unittest.main()
