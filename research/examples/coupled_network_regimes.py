"""Three-node, three-domain comparison of OTFT prototype dynamics.

The graph and dimensionless potential are identical across the three regimes.
The reported values are numerical diagnostics, not calibrated observables.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from one_time_field.damped import DampedHamiltonianFieldSystem
from one_time_field.hamiltonian import HamiltonianFieldSystem
from one_time_field.variational import VariationalFieldSystem


ADJACENCY = [
    [0.0, 1.0, 0.0],
    [1.0, 0.0, 1.0],
    [0.0, 1.0, 0.0],
]
INITIAL = {
    "scalar": [0.9, -0.35, 0.55],
    "phases": [0.15, 1.25, 2.35],
    "tensor": [[0.8, -0.2], [-0.1, 0.65], [0.45, 0.9]],
}
MOMENTA = {
    "scalar": [0.08, -0.04, 0.03],
    "phases": [0.02, -0.03, 0.01],
    "tensor": [[0.02, -0.01], [-0.015, 0.025], [0.01, -0.02]],
}


def make_potential():
    return VariationalFieldSystem(
        adjacency=ADJACENCY,
        scalar=INITIAL["scalar"],
        phases=INITIAL["phases"],
        tensor=INITIAL["tensor"],
        scalar_gradient=0.8,
        phase_gradient=0.7,
        tensor_gradient=0.6,
        scalar_mass=0.15,
        tensor_mass=0.1,
        scalar_phase_coupling=0.35,
        tensor_phase_coupling=0.25,
        scalar_mobility=0.8,
        phase_mobility=0.7,
        tensor_mobility=0.9,
    )


def order_parameter(phases):
    import cmath
    return abs(sum(cmath.exp(1j * value) for value in phases) / len(phases))


def norm(values):
    if values and isinstance(values[0], list):
        return sum(value * value for row in values for value in row) ** 0.5
    return sum(value * value for value in values) ** 0.5


def main():
    gradient = make_potential()
    conservative = HamiltonianFieldSystem(
        make_potential(),
        scalar_inertia=1.0,
        phase_inertia=1.2,
        tensor_inertia=0.9,
        momenta=MOMENTA,
    )
    damped = DampedHamiltonianFieldSystem(
        make_potential(),
        scalar_inertia=1.0,
        phase_inertia=1.2,
        tensor_inertia=0.9,
        momenta=MOMENTA,
        scalar_damping=0.25,
        phase_damping=0.2,
        tensor_damping=0.3,
    )

    print("step,time,gradient_V,hamiltonian_H,damped_H,phase_R,gradient_scalar_norm,hamiltonian_scalar_norm,damped_scalar_norm")
    dt, steps = 0.001, 2000
    for step in range(steps + 1):
        if step % 100 == 0:
            print(
                f"{step},{step*dt:.4f},"
                f"{gradient.potential():.10f},{conservative.energy():.10f},"
                f"{damped.energy():.10f},"
                f"{order_parameter(gradient.phases):.8f},"
                f"{norm(gradient.scalar):.8f},"
                f"{norm(conservative.potential_system.scalar):.8f},"
                f"{norm(damped.potential_system.scalar):.8f}"
            )
        if step < steps:
            gradient.step(dt)
            conservative.step(dt)
            damped.step(dt)


if __name__ == "__main__":
    main()
