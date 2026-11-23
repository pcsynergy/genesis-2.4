import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.hamiltonian import HamiltonianFieldSystem
from one_time_field.variational import VariationalFieldSystem


class HamiltonianFieldSystemTests(unittest.TestCase):
    def oscillator(self):
        potential = VariationalFieldSystem(
            adjacency=[[0.0]], scalar=[1.0], scalar_mass=1.0
        )
        return HamiltonianFieldSystem(potential, scalar_inertia=1.0, momenta={"scalar": [0.0]})

    def test_energy_error_remains_bounded_for_harmonic_oscillator(self):
        model = self.oscillator()
        initial = model.energy()
        errors = []
        for _ in range(1000):
            model.step(0.01)
            errors.append(abs(model.energy() - initial))
        self.assertLess(max(errors), 1.0e-4)

    def test_time_reversal_for_velocity_verlet(self):
        model = self.oscillator()
        for _ in range(100):
            model.step(0.01)
        model.momenta["scalar"] = [-p for p in model.momenta["scalar"]]
        for _ in range(100):
            model.step(0.01)
        model.momenta["scalar"] = [-p for p in model.momenta["scalar"]]
        self.assertAlmostEqual(model.potential_system.scalar[0], 1.0, places=10)
        self.assertAlmostEqual(model.momenta["scalar"][0], 0.0, places=10)

    def test_coupled_domains_have_finite_energy(self):
        potential = VariationalFieldSystem(
            adjacency=[[0.0, 1.0], [1.0, 0.0]],
            scalar=[0.2, 1.0],
            phases=[0.1, 1.2],
            tensor=[[1.0, 0.0], [0.0, 1.0]],
            scalar_phase_coupling=0.2,
            tensor_phase_coupling=0.1,
        )
        model = HamiltonianFieldSystem(potential)
        start = model.energy()
        for _ in range(20):
            model.step(0.001)
        self.assertTrue(math.isfinite(model.energy()))
        self.assertAlmostEqual(model.energy(), start, places=7)

    def test_rejects_external_frequency_drive_and_invalid_inertia(self):
        driven = VariationalFieldSystem(
            adjacency=[[0.0]], phases=[0.0], natural_frequencies=[1.0]
        )
        with self.assertRaises(ValueError):
            HamiltonianFieldSystem(driven)
        with self.assertRaises(ValueError):
            HamiltonianFieldSystem(self.oscillator().potential_system, scalar_inertia=0.0)

    def test_momentum_shape_must_match_coordinates(self):
        potential = VariationalFieldSystem(adjacency=[[0.0]], scalar=[1.0])
        with self.assertRaises(ValueError):
            HamiltonianFieldSystem(potential, momenta={"scalar": [0.0, 1.0]})

    def test_rejects_nonpositive_step(self):
        model = self.oscillator()
        with self.assertRaises(ValueError):
            model.step(0.0)


if __name__ == "__main__":
    unittest.main()
