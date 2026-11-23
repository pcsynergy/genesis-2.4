"""Timestep-convergence study for the three one-mode dynamics regimes.

Outputs one CSV row per timestep and regime. Exact reference solutions are
available for the unit quadratic potential V(q)=q^2/2, unit inertia, and
Rayleigh coefficient gamma=0.4.
"""
from math import cos, exp, sin, sqrt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from one_time_field.damped import DampedHamiltonianFieldSystem
from one_time_field.hamiltonian import HamiltonianFieldSystem
from one_time_field.variational import VariationalFieldSystem


FINAL_TIME = 4.0
DAMPING = 0.4
TIME_STEPS = (0.08, 0.04, 0.02, 0.01, 0.005)


def potential():
    return VariationalFieldSystem(adjacency=[[0.0]], scalar=[1.0], scalar_mass=1.0)


def exact_values(t):
    """Return exact q,p for gradient, conservative, and damped references."""
    q_gradient = exp(-t)
    q_hamiltonian, p_hamiltonian = cos(t), -sin(t)
    a = DAMPING / 2.0
    omega_d = sqrt(1.0 - a*a)
    decay = exp(-a*t)
    q_damped = decay * (cos(omega_d*t) + (a/omega_d)*sin(omega_d*t))
    p_damped = -decay * sin(omega_d*t) / omega_d
    return q_gradient, q_hamiltonian, p_hamiltonian, q_damped, p_damped


def run_one(dt):
    steps = round(FINAL_TIME / dt)
    dt = FINAL_TIME / steps
    gradient = potential()
    conservative = HamiltonianFieldSystem(
        potential(), scalar_inertia=1.0, momenta={"scalar": [0.0]}
    )
    damped = DampedHamiltonianFieldSystem(
        potential(), scalar_inertia=1.0, momenta={"scalar": [0.0]},
        scalar_damping=DAMPING,
    )
    initial_h = conservative.energy()
    initial_damped_h = damped.energy()
    dissipated = 0.0
    max_hamiltonian_drift = 0.0
    for _ in range(steps):
        p_before = damped.momenta["scalar"][0]
        rate_before = DAMPING * p_before*p_before
        gradient.step(dt)
        conservative.step(dt)
        damped.step(dt)
        p_after = damped.momenta["scalar"][0]
        rate_after = DAMPING * p_after*p_after
        dissipated += 0.5 * dt * (rate_before + rate_after)
        max_hamiltonian_drift = max(
            max_hamiltonian_drift, abs(conservative.energy() - initial_h)
        )

    qg, qh, ph, qd, pd = exact_values(FINAL_TIME)
    gradient_error = abs(gradient.scalar[0] - qg)
    hamiltonian_error = sqrt(
        (conservative.potential_system.scalar[0] - qh)**2
        + (conservative.momenta["scalar"][0] - ph)**2
    )
    damped_error = sqrt(
        (damped.potential_system.scalar[0] - qd)**2
        + (damped.momenta["scalar"][0] - pd)**2
    )
    balance_residual = abs(damped.energy() + dissipated - initial_damped_h)
    return {
        "dt": dt,
        "gradient_endpoint_error": gradient_error,
        "hamiltonian_state_error": hamiltonian_error,
        "hamiltonian_max_energy_drift": max_hamiltonian_drift,
        "damped_state_error": damped_error,
        "damped_energy_balance_residual": balance_residual,
        "damped_final_energy": damped.energy(),
    }


def main():
    print(
        "dt,gradient_endpoint_error,hamiltonian_state_error,"
        "hamiltonian_max_energy_drift,damped_state_error,"
        "damped_energy_balance_residual,damped_final_energy"
    )
    for dt in TIME_STEPS:
        row = run_one(dt)
        print(",".join(f"{row[key]:.12e}" for key in (
            "dt", "gradient_endpoint_error", "hamiltonian_state_error",
            "hamiltonian_max_energy_drift", "damped_state_error",
            "damped_energy_balance_residual", "damped_final_energy",
        )))


if __name__ == "__main__":
    main()
