"""Run Experiment 5: action-derived dynamical clock-field coupling."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from one_time_field.clock_action import ClockCoupledHamiltonianSystem
from one_time_field.hamiltonian import HamiltonianFieldSystem
from one_time_field.variational import VariationalFieldSystem


def build(coupling):
    potential = VariationalFieldSystem(
        adjacency=[[0.0, 1.0], [1.0, 0.0]],
        scalar=[0.8, -0.3], scalar_mass=0.2, scalar_gradient=0.4,
    )
    fields = HamiltonianFieldSystem(
        potential, scalar_inertia=1.0,
        momenta={"scalar": [0.1, -0.05]},
    )
    return ClockCoupledHamiltonianSystem(
        fields, clock_coordinate=0.2, clock_momentum=0.03,
        clock_inertia=1.2, clock_stiffness=0.8, coupling=coupling,
    )


def main():
    control, coupled = build(0.0), build(0.1)
    e0 = coupled.energy()
    print("step,lambda,control_clock,coupled_clock,control_energy,coupled_energy,field_distance")
    for step in range(2001):
        if step % 200 == 0:
            a = control.field_system.potential_system.scalar
            b = coupled.field_system.potential_system.scalar
            distance = sum((x-y)**2 for x, y in zip(a, b))**0.5
            print(f"{step},{step*0.002:.6f},{control.clock_coordinate:.12g},"
                  f"{coupled.clock_coordinate:.12g},{control.energy():.12g},"
                  f"{coupled.energy():.12g},{distance:.12g}")
        if step < 2000:
            control.step(0.002)
            coupled.step(0.002)
    print(f"coupled_energy_drift={coupled.energy()-e0:.12g}")


if __name__ == "__main__":
    main()
