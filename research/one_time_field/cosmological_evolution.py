"""Experiment 14: self-consistent homogeneous two-field FLRW evolution.

Classical spatially-flat FLRW model in natural units, signature (-,+,+,+).
H is integrated independently from the Friedmann constraint so numerical
constraint drift is measurable rather than hidden by algebraic reconstruction.
"""
from __future__ import annotations

from math import isfinite, sqrt
from .flrw_curved import energy_density_pressure_flrw, on_shell_accelerations_flrw
from .gravitational_flrw import friedmann_residual
from .lorentz_covariant import CovariantParameters


def _validate(*values: float) -> None:
    if not all(isfinite(float(v)) for v in values):
        raise ValueError("all inputs must be finite")


def _observables(state, params, mpl2):
    a, h, phi, phi_dot, clock, clock_dot = state
    if a <= 0:
        raise ValueError("scale factor became nonpositive")
    rho, pressure = energy_density_pressure_flrw(
        phi, clock, phi_dot, clock_dot, params
    )
    if rho < 0:
        raise ValueError("energy density became negative; no real flat-FLRW H constraint")
    return rho, pressure, friedmann_residual(h, rho, mpl2)


def _rhs(state, params, mpl2):
    a, h, phi, phi_dot, clock, clock_dot = state
    rho, pressure, _ = _observables(state, params, mpl2)
    phi_ddot, clock_ddot = on_shell_accelerations_flrw(
        phi, clock, phi_dot, clock_dot, h, params
    )
    h_dot = -(rho + pressure) / (2.0 * mpl2)
    return (a * h, h_dot, phi_dot, phi_ddot, clock_dot, clock_ddot)


def _add_scaled(y, terms, scale):
    return tuple(y[i] + scale * terms[i] for i in range(len(y)))


def _rk4_step(state, dt, params, mpl2):
    k1 = _rhs(state, params, mpl2)
    k2 = _rhs(_add_scaled(state, k1, 0.5 * dt), params, mpl2)
    k3 = _rhs(_add_scaled(state, k2, 0.5 * dt), params, mpl2)
    k4 = _rhs(_add_scaled(state, k3, dt), params, mpl2)
    return tuple(state[i] + dt * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) / 6.0
                 for i in range(len(state)))


def evolve_cosmology(
    parameters: CovariantParameters = CovariantParameters(),
    planck_mass_squared: float = 1.0,
    *,
    scale_factor_0: float = 1.0,
    phi_0: float = 0.2,
    clock_0: float = 0.1,
    phi_dot_0: float = 0.0,
    clock_dot_0: float = 0.0,
    duration: float = 2.0,
    steps: int = 2000,
    expanding: bool = True,
) -> tuple[dict[str, float], ...]:
    """Integrate (a,H,phi,phi_dot,T,T_dot) with fixed-step classical RK4.

    Initial H is selected from the Friedmann constraint, with sign determined
    by expanding. The ODE subsequently evolves H through the acceleration
    equation. Returned rows include rho, p and the Friedmann residual.
    """
    _validate(planck_mass_squared, scale_factor_0, phi_0, clock_0,
              phi_dot_0, clock_dot_0, duration)
    if planck_mass_squared <= 0 or scale_factor_0 <= 0 or duration <= 0:
        raise ValueError("Planck mass squared, scale factor and duration must be positive")
    if not isinstance(steps, int) or steps < 1:
        raise ValueError("steps must be a positive integer")
    rho0, _ = energy_density_pressure_flrw(
        phi_0, clock_0, phi_dot_0, clock_dot_0, parameters
    )
    if rho0 < 0:
        raise ValueError("initial energy density must be nonnegative")
    sign = 1.0 if expanding else -1.0
    h0 = sign * sqrt(rho0 / (3.0 * planck_mass_squared))
    state = (scale_factor_0, h0, phi_0, phi_dot_0, clock_0, clock_dot_0)
    dt = duration / steps
    rows = []

    def record(index, current):
        rho, pressure, constraint = _observables(current, parameters, planck_mass_squared)
        t = index * dt
        rows.append({
            "time": t, "scale_factor": current[0], "hubble": current[1],
            "phi": current[2], "phi_dot": current[3],
            "clock": current[4], "clock_dot": current[5],
            "energy_density": rho, "pressure": pressure,
            "friedmann_residual": constraint,
        })

    record(0, state)
    for i in range(1, steps + 1):
        state = _rk4_step(state, dt, parameters, planck_mass_squared)
        _validate(*state)
        record(i, state)
    return tuple(rows)
