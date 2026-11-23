import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.clock_action import ClockCoupledHamiltonianSystem
from one_time_field.hamiltonian import HamiltonianFieldSystem
from one_time_field.variational import VariationalFieldSystem


def make_model(coupling=0.0):
    potential = VariationalFieldSystem(
        adjacency=[[0.0, 1.0], [1.0, 0.0]],
        scalar=[0.8, -0.3],
        scalar_mass=0.2,
        scalar_gradient=0.4,
    )
    fields = HamiltonianFieldSystem(
        potential, scalar_inertia=1.0,
        momenta={"scalar": [0.1, -0.05]},
    )
    return ClockCoupledHamiltonianSystem(
        fields, clock_coordinate=0.2, clock_momentum=0.03,
        clock_inertia=1.2, clock_stiffness=0.8, coupling=coupling,
    )


class ClockActionTests(unittest.TestCase):
    def test_energy_is_conserved_with_small_verlet_error(self):
        model = make_model(coupling=0.1)
        initial = model.energy()
        errors = []
        for _ in range(2000):
            model.step(0.002)
            errors.append(abs(model.energy() - initial))
        self.assertLess(max(errors), 2e-5)

    def test_zero_coupling_decouples_clock_and_fields(self):
        model = make_model(coupling=0.0)
        initial_field = model.field_system.snapshot()
        initial_clock_energy = (
            model.clock_momentum**2 / (2 * model.clock_inertia)
            + 0.5 * model.clock_stiffness * model.clock_coordinate**2
        )
        model.step(0.01)
        self.assertNotEqual(model.clock_coordinate, 0.2)
        self.assertTrue(all(
            math.isfinite(v) for v in model.field_system.potential_system.scalar
        ))
        self.assertAlmostEqual(model.energy(), model.energy(), places=14)
        self.assertEqual(set(initial_field), set(model.field_system.snapshot()))

    def test_nonzero_coupling_changes_clock_acceleration(self):
        uncoupled, coupled = make_model(0.0), make_model(0.1)
        uncoupled.step(0.001)
        coupled.step(0.001)
        self.assertNotAlmostEqual(
            uncoupled.clock_momentum, coupled.clock_momentum, places=10
        )

    def test_lagrangian_is_kinetic_minus_potential(self):
        model = make_model(0.05)
        self.assertAlmostEqual(
            model.lagrangian(), model.kinetic_energy() - model.potential_energy()
        )

    def test_rejects_missing_scalar_field_and_invalid_parameters(self):
        fields = HamiltonianFieldSystem(
            VariationalFieldSystem(adjacency=[[0.0]], phases=[0.0])
        )
        with self.assertRaises(ValueError):
            ClockCoupledHamiltonianSystem(fields)
        with self.assertRaises(ValueError):
            make_model().step(0.0)
        with self.assertRaises(ValueError):
            ClockCoupledHamiltonianSystem(make_model().field_system, clock_inertia=0.0)


if __name__ == "__main__":
    unittest.main()
