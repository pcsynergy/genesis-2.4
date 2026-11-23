import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.damped import DampedHamiltonianFieldSystem
from one_time_field.hamiltonian import HamiltonianFieldSystem
from one_time_field.variational import VariationalFieldSystem


def make_potential():
    return VariationalFieldSystem(adjacency=[[0.0]], scalar=[1.0], scalar_mass=1.0)


class DynamicsConvergenceTests(unittest.TestCase):
    def test_hamiltonian_state_error_decreases_quadratically(self):
        errors = []
        for dt in (0.08, 0.04, 0.02):
            model = HamiltonianFieldSystem(
                make_potential(), scalar_inertia=1.0, momenta={"scalar": [0.0]}
            )
            for _ in range(round(4.0 / dt)):
                model.step(dt)
            errors.append(abs(model.potential_system.scalar[0] - __import__("math").cos(4.0)))
        self.assertGreater(errors[0], errors[1])
        self.assertGreater(errors[1], errors[2])
        self.assertGreater(errors[0] / errors[1], 3.5)

    def test_damped_energy_balance_residual_decreases_with_timestep(self):
        residuals = []
        gamma = 0.4
        for dt in (0.08, 0.04, 0.02):
            model = DampedHamiltonianFieldSystem(
                make_potential(), scalar_inertia=1.0,
                momenta={"scalar": [0.0]}, scalar_damping=gamma,
            )
            initial = model.energy()
            loss = 0.0
            for _ in range(round(4.0 / dt)):
                p0 = model.momenta["scalar"][0]
                model.step(dt)
                p1 = model.momenta["scalar"][0]
                loss += 0.5 * dt * gamma * (p0*p0 + p1*p1)
            residuals.append(abs(model.energy() + loss - initial))
        self.assertGreater(residuals[0], residuals[1])
        self.assertGreater(residuals[1], residuals[2])

    def test_gradient_flow_euler_error_decreases_with_timestep(self):
        errors = []
        for dt in (0.08, 0.04, 0.02):
            model = make_potential()
            for _ in range(round(4.0 / dt)):
                model.step(dt)
            errors.append(abs(model.scalar[0] - __import__("math").exp(-4.0)))
        self.assertGreater(errors[0], errors[1])
        self.assertGreater(errors[1], errors[2])


if __name__ == "__main__":
    unittest.main()
