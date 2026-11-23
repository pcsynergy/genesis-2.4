import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.engine import DimensionalFieldEngine
from one_time_field.harmonic import PhaseOscillatorNetwork
from one_time_field.network import GraphFieldNetwork
from one_time_field.tensor import TensorFieldNetwork
from one_time_field.field_activity import FieldActivity


class FieldActivityTests(unittest.TestCase):
    def test_activity_is_derived_from_domain_derivatives(self):
        adjacency = [[0.0, 1.0], [1.0, 0.0]]
        engine = DimensionalFieldEngine(
            scalar=GraphFieldNetwork(adjacency, [1.0, 0.0], coupling=1.0),
            harmonic=PhaseOscillatorNetwork(adjacency, [0.0, 1.0], [1.0, 1.0]),
            tensor=TensorFieldNetwork(adjacency, [[1.0, 0.0], [0.0, 0.0]], (2,)),
        )
        result = FieldActivity.from_engine(engine)
        self.assertAlmostEqual(result.scalar, 1.0)
        self.assertGreater(result.phase, 0.0)
        self.assertAlmostEqual(result.tensor, 0.5)
        self.assertAlmostEqual(result.total, result.scalar + result.phase + result.tensor)

    def test_scalar_activity_includes_explicit_source(self):
        adjacency = [[0.0, 1.0], [1.0, 0.0]]
        engine = DimensionalFieldEngine(
            scalar=GraphFieldNetwork(adjacency, [0.0, 0.0], coupling=0.0)
        )
        result = FieldActivity.from_engine(engine, scalar_source=[2.0, 0.0])
        self.assertAlmostEqual(result.scalar, 2.0)

    def test_weights_select_domains_and_scale_total(self):
        adjacency = [[0.0, 1.0], [1.0, 0.0]]
        engine = DimensionalFieldEngine(
            scalar=GraphFieldNetwork(adjacency, [1.0, 0.0], coupling=1.0),
            harmonic=PhaseOscillatorNetwork(adjacency, [0.0, 0.0], [0.0, 0.0]),
        )
        result = FieldActivity.from_engine(
            engine, scalar_weight=2.0, phase_weight=0.0
        )
        self.assertAlmostEqual(result.total, 2.0)

    def test_relational_rate_uses_derived_activity(self):
        adjacency = [[0.0, 1.0], [1.0, 0.0]]
        engine = DimensionalFieldEngine(
            scalar=GraphFieldNetwork(adjacency, [1.0, 0.0], coupling=1.0)
        )
        activity = FieldActivity.from_engine(engine)
        self.assertAlmostEqual(activity.relational_rate(gain=0.5), 1.5)

    def test_invalid_weights_and_clock_parameters_rejected(self):
        adjacency = [[0.0, 1.0], [1.0, 0.0]]
        engine = DimensionalFieldEngine(
            scalar=GraphFieldNetwork(adjacency, [1.0, 0.0], coupling=1.0)
        )
        with self.assertRaises(ValueError):
            FieldActivity.from_engine(engine, scalar_weight=-1.0)
        activity = FieldActivity.from_engine(engine)
        with self.assertRaises(ValueError):
            activity.relational_rate(gain=-1.0)
        with self.assertRaises(ValueError):
            activity.relational_rate(baseline=0.0)


if __name__ == "__main__":
    unittest.main()
