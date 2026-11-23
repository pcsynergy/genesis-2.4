"""Experiment 10: stress-energy tensor and on-shell conservation.

Flat 1+1 Minkowski spacetime, signature (-,+), natural units c=1.
"""
from __future__ import annotations

from .lorentz_covariant import (
    CovariantParameters,
    coupling_function,
    euler_lagrange_residuals,
    lagrangian_density,
)


def stress_energy_tensor(
    phi: float,
    clock: float,
    phi_derivatives: tuple[float, float],
    clock_derivatives: tuple[float, float],
    parameters: CovariantParameters = CovariantParameters(),
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Return symmetric contravariant T^{mu nu} as ((T00,T01),(T10,T11))."""
    p = parameters
    phi_t, phi_x = phi_derivatives
    clock_t, clock_x = clock_derivatives
    lag = lagrangian_density(
        phi, clock, phi_derivatives, clock_derivatives, p
    )
    t00 = phi_t**2 + p.clock_kinetic * clock_t**2 - lag
    t01 = -phi_t * phi_x - p.clock_kinetic * clock_t * clock_x
    t11 = phi_x**2 + p.clock_kinetic * clock_x**2 + lag
    return ((t00, t01), (t01, t11))


def divergence_from_field_equations(
    phi: float,
    clock: float,
    phi_derivatives: tuple[float, float],
    clock_derivatives: tuple[float, float],
    phi_second: tuple[float, float, float],
    clock_second: tuple[float, float, float],
    parameters: CovariantParameters = CovariantParameters(),
) -> tuple[float, float]:
    """Compute partial_mu T^{mu nu} using the local Euler-Lagrange identity.

    Hessian tuples are (d_tt, d_tx, d_xx). The result equals
    R_phi * partial^nu(phi) + R_T * partial^nu(T), with
    R_phi,R_T the field-equation residuals.
    """
    phi_box = -phi_second[0] + phi_second[2]
    clock_box = -clock_second[0] + clock_second[2]
    r_phi, r_clock = euler_lagrange_residuals(
        phi, clock, phi_box, clock_box, parameters
    )
    phi_t, phi_x = phi_derivatives
    clock_t, clock_x = clock_derivatives
    # For (-,+), partial^0=-partial_t and partial^1=partial_x.
    return (
        -r_phi * phi_t - r_clock * clock_t,
        r_phi * phi_x + r_clock * clock_x,
    )


def on_shell_second_time_derivatives(
    phi: float,
    clock: float,
    phi_derivatives: tuple[float, float],
    clock_derivatives: tuple[float, float],
    phi_dxx: float,
    clock_dxx: float,
    parameters: CovariantParameters = CovariantParameters(),
) -> tuple[float, float]:
    """Return (phi_tt,T_tt) required by the field equations for supplied d_xx."""
    p = parameters
    from .lorentz_covariant import coupling_derivative
    phi_tt = (phi_dxx - p.field_mass**2 * phi
              + p.coupling * clock * coupling_derivative(phi))
    clock_tt = (clock_dxx - (p.clock_mass_squared * clock
                 - p.coupling * coupling_function(phi)) / p.clock_kinetic)
    return phi_tt, clock_tt
