"""Demonstrate conservative Hamiltonian evolution of a one-node field mode."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from one_time_field import HamiltonianFieldSystem, VariationalFieldSystem


def main() -> None:
    potential = VariationalFieldSystem(
        adjacency=[[0.0]],
        scalar=[1.0],
        scalar_mass=1.0,
    )
    model = HamiltonianFieldSystem(
        potential, scalar_inertia=1.0, momenta={"scalar": [0.0]}
    )
    print("step,coordinate,momentum,kinetic,potential,total_energy")
    for step in range(101):
        if step % 10 == 0:
            state = model.snapshot()
            q = state["coordinates"]["scalar"][0]
            p = state["momenta"]["scalar"][0]
            print(
                f"{step},{q:.8f},{p:.8f},"
                f"{model.kinetic_energy():.8f},"
                f"{model.potential_system.potential():.8f},"
                f"{model.energy():.8f}"
            )
        if step < 100:
            model.step(0.01)


if __name__ == "__main__":
    main()
