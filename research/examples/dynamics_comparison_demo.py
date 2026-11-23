"""Compare gradient flow, conservative Hamiltonian, and Rayleigh damping."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from one_time_field.damped import DampedHamiltonianFieldSystem
from one_time_field.hamiltonian import HamiltonianFieldSystem
from one_time_field.variational import VariationalFieldSystem


def make_potential():
    return VariationalFieldSystem(
        adjacency=[[0.0]], scalar=[1.0], scalar_mass=1.0
    )


def main():
    gradient = make_potential()
    conservative = HamiltonianFieldSystem(
        make_potential(), scalar_inertia=1.0, momenta={"scalar": [0.0]}
    )
    damped = DampedHamiltonianFieldSystem(
        make_potential(),
        scalar_inertia=1.0,
        momenta={"scalar": [0.0]},
        scalar_damping=0.4,
    )

    print("step,time,gradient_q,gradient_V,hamiltonian_q,hamiltonian_H,damped_q,damped_H")
    dt = 0.01
    steps = 1000
    for step in range(steps + 1):
        if step % 10 == 0:
            print(
                f"{step},{step*dt:.4f},"
                f"{gradient.scalar[0]:.9f},{gradient.potential():.9f},"
                f"{conservative.potential_system.scalar[0]:.9f},{conservative.energy():.9f},"
                f"{damped.potential_system.scalar[0]:.9f},{damped.energy():.9f}"
            )
        if step < steps:
            gradient.step(dt)
            conservative.step(dt)
            damped.step(dt)


if __name__ == "__main__":
    main()
