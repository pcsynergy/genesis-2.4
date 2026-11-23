import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.damped import DampedHamiltonianFieldSystem
from one_time_field.hamiltonian import HamiltonianFieldSystem
from one_time_field.variational import VariationalFieldSystem


ADJACENCY = [
    [0.0, 1.0, 0.0],
    [1.0, 0.0, 1.0],
    [0.0, 1.0, 0.0],
]
STATE = {
    "scalar": [0.9, -0.35, 0.55],
    "phases": [0.15, 1.25, 2.35],
    "tensor": [[0.8, -0.2], [-0.1, 0.65], [0.45, 0.9]],
}
MOMENTA = {
    "scalar": [0.08, -0.04, 0.03],
    "phases": [0.02, -0.03, 0.01],
    "tensor": [[0.02, -0.01], [-0.015, 0.025], [0.01, -0.02]],
}


def make_potential(cross_coupling=True):
    return VariationalFieldSystem(
        adjacency=ADJACENCY,
        scalar=STATE["scalar"],
        phases=STATE["phases"],
        tensor=STATE["tensor"],
        scalar_gradient=0.8,
        phase_gradient=0.7,
        tensor_gradient=0.6,
        scalar_mass=0.15,
        tensor_mass=0.1,
        scalar_phase_coupling=0.35 if cross_coupling else 0.0,
        tensor_phase_coupling=0.25 if cross_coupling else 0.0,
        scalar_mobility=0.8,
        phase_mobility=0.7,
        tensor_mobility=0.9,
    )


def flatten(state):
    return (
        list(state["scalar"])
        + list(state["phases"])
        + [v for row in state["tensor"] for v in row]
    )


class CoupledNetworkRegimeTests(unittest.TestCase):
    def test_cross_terms_couple_all_three_domains(self):
        coupled = make_potential(True).gradients()
        uncoupled = make_potential(False).gradients()
        for domain in ("scalar", "phases", "tensor"):
            self.assertTrue(
                any(abs(a - b) > 1.0e-8 for a, b in zip(
                    flatten({domain: coupled[domain]}) if domain != "tensor"
                    else {"tensor": coupled[domain]},
                    flatten({domain: uncoupled[domain]}) if domain != "tensor"
                    else {"tensor": uncoupled[domain]},
                )),
                msg=f"cross coupling did not alter {domain} gradient",
            )

    def test_gradient_flow_reduces_shared_potential(self):
        model = make_potential()
        initial = model.potential()
        for _ in range(100):
            model.step(0.001)
        self.assertLess(model.potential(), initial)
        self.assertTrue(all(math.isfinite(v) for v in flatten(model.snapshot())))

    def test_hamiltonian_energy_drift_is_bounded(self):
        model = HamiltonianFieldSystem(
            make_potential(),
            scalar_inertia=1.0,
            phase_inertia=1.2,
            tensor_inertia=0.9,
            momenta=MOMENTA,
        )
        initial = model.energy()
        max_drift = 0.0
        for _ in range(1000):
            model.step(0.001)
            max_drift = max(max_drift, abs(model.energy() - initial))
        self.assertLess(max_drift, 2.0e-4)
        self.assertTrue(math.isfinite(model.energy()))

    def test_rayleigh_damping_lowers_total_energy(self):
        model = DampedHamiltonianFieldSystem(
            make_potential(),
            scalar_inertia=1.0,
            phase_inertia=1.2,
            tensor_inertia=0.9,
            momenta=MOMENTA,
            scalar_damping=0.25,
            phase_damping=0.2,
            tensor_damping=0.3,
        )
        initial = model.energy()
        for _ in range(2000):
            model.step(0.001)
        self.assertLess(model.energy(), initial)
        self.assertTrue(math.isfinite(model.energy()))

    def test_all_three_regimes_remain_finite_and_share_initial_state(self):
        gradient = make_potential()
        conservative = HamiltonianFieldSystem(make_potential(), momenta=MOMENTA)
        damped = DampedHamiltonianFieldSystem(make_potential(), momenta=MOMENTA)
        self.assertEqual(flatten(gradient.snapshot()), flatten(conservative.potential_system.snapshot()))
        self.assertEqual(flatten(gradient.snapshot()), flatten(damped.potential_system.snapshot()))
        for _ in range(100):
            gradient.step(0.001)
            conservative.step(0.001)
            damped.step(0.001)
        for values in (
            flatten(gradient.snapshot()),
            flatten(conservative.potential_system.snapshot()),
            flatten(damped.potential_system.snapshot()),
        ):
            self.assertTrue(all(math.isfinite(v) for v in values))


if __name__ == "__main__":
    unittest.main()
