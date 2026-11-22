import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.variational import VariationalFieldSystem


class VariationalFieldSystemTests(unittest.TestCase):
    def make_system(self):
        return VariationalFieldSystem(
            adjacency=[[0, 1], [1, 0]],
            scalar=[0.2, 1.1],
            phases=[0.3, 1.0],
            tensor=[[0.0, 1.0], [1.5, -0.5]],
            scalar_gradient=0.8,
            phase_gradient=0.6,
            tensor_gradient=0.4,
            scalar_mass=0.1,
            tensor_mass=0.2,
            scalar_phase_coupling=0.3,
        )

    def test_gradient_matches_finite_difference(self):
        model = self.make_system()
        analytic = model.gradients()
        eps = 1e-6
        original = model.scalar[0]
        model.scalar[0] = original + eps
        plus = model.potential()
        model.scalar[0] = original - eps
        minus = model.potential()
        model.scalar[0] = original
        numeric = (plus - minus) / (2 * eps)
        self.assertAlmostEqual(analytic["scalar"][0], numeric, places=6)

        original = model.phases[0]
        model.phases[0] = original + eps
        plus = model.potential()
        model.phases[0] = original - eps
        minus = model.potential()
        model.phases[0] = original
        numeric = (plus - minus) / (2 * eps)
        self.assertAlmostEqual(analytic["phases"][0], numeric, places=6)

        original = model.tensor[0][1]
        model.tensor[0][1] = original + eps
        plus = model.potential()
        model.tensor[0][1] = original - eps
        minus = model.potential()
        model.tensor[0][1] = original
        numeric = (plus - minus) / (2 * eps)
        self.assertAlmostEqual(analytic["tensor"][0][1], numeric, places=6)

    def test_gradient_flow_reduces_potential_without_external_drive(self):
        model = self.make_system()
        initial = model.potential()
        for _ in range(100):
            model.step(0.001)
        self.assertLess(model.potential(), initial)

    def test_phase_global_shift_leaves_potential_unchanged(self):
        model = self.make_system()
        initial = model.potential()
        model.phases = [theta + 2.4 for theta in model.phases]
        self.assertAlmostEqual(model.potential(), initial, places=12)

    def test_scalar_phase_cross_term_changes_both_gradients(self):
        model = self.make_system()
        coupled = model.gradients()
        model.scalar_phase_coupling = 0.0
        uncoupled = model.gradients()
        self.assertNotAlmostEqual(coupled["scalar"][0], uncoupled["scalar"][0])
        self.assertNotAlmostEqual(coupled["phases"][0], uncoupled["phases"][0])

    def test_single_domain_is_supported(self):
        model = VariationalFieldSystem(adjacency=[[0]], scalar=[2.0], scalar_mass=0.5)
        self.assertAlmostEqual(model.potential(), 1.0)
        model.step(0.1)
        self.assertAlmostEqual(model.scalar[0], 1.9)

    def test_bad_graph_and_step_are_rejected(self):
        with self.assertRaises(ValueError):
            VariationalFieldSystem(adjacency=[[0, 1], [0, 0]], scalar=[0, 1])
        model = self.make_system()
        with self.assertRaises(ValueError):
            model.step(0.0)

    def test_phase_drive_requires_phase_domain(self):
        with self.assertRaises(ValueError):
            VariationalFieldSystem(adjacency=[[0]], scalar=[1], natural_frequencies=[1])


if __name__ == "__main__":
    unittest.main()
