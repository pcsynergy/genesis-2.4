import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.damped import DampedHamiltonianFieldSystem
from one_time_field.variational import VariationalFieldSystem


class DampedHamiltonianFieldSystemTests(unittest.TestCase):
    def oscillator(self, damping=0.4):
        potential = VariationalFieldSystem(
            adjacency=[[0.0]], scalar=[1.0], scalar_mass=1.0
        )
        return DampedHamiltonianFieldSystem(
            potential,
            scalar_inertia=1.0,
            momenta={"scalar": [0.0]},
            scalar_damping=damping,
        )

    def test_zero_damping_matches_hamiltonian_reference(self):
        from one_time_field.hamiltonian import HamiltonianFieldSystem

        damped = self.oscillator(damping=0.0)
        reference = HamiltonianFieldSystem(
            VariationalFieldSystem(adjacency=[[0.0]], scalar=[1.0], scalar_mass=1.0),
            scalar_inertia=1.0,
            momenta={"scalar": [0.0]},
        )
        for _ in range(100):
            damped.step(0.01)
            reference.step(0.01)
        self.assertAlmostEqual(damped.energy(), reference.energy(), places=13)
        self.assertAlmostEqual(
            damped.potential_system.scalar[0],
            reference.potential_system.scalar[0],
            places=13,
        )

    def test_damping_reduces_energy_over_a_resolved_trajectory(self):
        model = self.oscillator()
        initial = model.energy()
        for _ in range(2000):
            model.step(0.01)
        self.assertLess(model.energy(), initial * 0.2)
        self.assertTrue(math.isfinite(model.energy()))

    def test_zero_and_positive_damping_are_valid_but_negative_is_not(self):
        self.oscillator(damping=0.0)
        with self.assertRaises(ValueError):
            self.oscillator(damping=-0.1)

    def test_rejects_nonpositive_step(self):
        model = self.oscillator()
        with self.assertRaises(ValueError):
            model.step(0.0)


if __name__ == "__main__":
    unittest.main()
