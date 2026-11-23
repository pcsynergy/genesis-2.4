"""Experiment 11: two scalar fields on 3+1-dimensional Minkowski spacetime.

Metric signature (-,+,+,+), natural units c=1, fixed flat background.
"""
from __future__ import annotations

from math import isfinite, sqrt
from .lorentz_covariant import (
    CovariantParameters, coupling_function, coupling_derivative,
)


def minkowski_gradient_norm(derivatives: tuple[float, float, float, float]) -> float:
    if len(derivatives) != 4:
        raise ValueError("a 3+1 gradient must contain (dt, dx, dy, dz)")
    return -derivatives[0] ** 2 + sum(v * v for v in derivatives[1:])


def lorentz_transform_gradient(
    derivatives: tuple[float, float, float, float],
    velocity: tuple[float, float, float],
) -> tuple[float, float, float, float]:
    """Transform scalar-field derivative components to a frame boosted by velocity."""
    if len(derivatives) != 4 or len(velocity) != 3:
        raise ValueError("expected four derivatives and three velocity components")
    if not all(isfinite(v) for v in (*derivatives, *velocity)):
        raise ValueError("components must be finite")
    b2 = sum(v * v for v in velocity)
    if b2 >= 1.0:
        raise ValueError("boost speed must be subluminal")
    if b2 == 0.0:
        return tuple(derivatives)
    gamma = 1.0 / sqrt(1.0 - b2)
    spatial = derivatives[1:]
    b_dot_x = sum(b * x for b, x in zip(velocity, spatial))
    time_prime = gamma * (derivatives[0] + b_dot_x)
    factor = (gamma - 1.0) * b_dot_x / b2 + gamma * derivatives[0]
    spatial_prime = tuple(x + factor * b for x, b in zip(spatial, velocity))
    return (time_prime, *spatial_prime)


def lagrangian_density_3plus1(
    phi: float, clock: float,
    phi_derivatives: tuple[float, float, float, float],
    clock_derivatives: tuple[float, float, float, float],
    parameters: CovariantParameters = CovariantParameters(),
) -> float:
    p = parameters
    return (
        -0.5 * minkowski_gradient_norm(phi_derivatives)
        -0.5 * p.field_mass**2 * phi**2
        -0.5 * p.clock_kinetic * minkowski_gradient_norm(clock_derivatives)
        -0.5 * p.clock_mass_squared * clock**2
        + p.coupling * clock * coupling_function(phi)
    )


def stress_energy_tensor_3plus1(
    phi: float, clock: float,
    phi_derivatives: tuple[float, float, float, float],
    clock_derivatives: tuple[float, float, float, float],
    parameters: CovariantParameters = CovariantParameters(),
) -> tuple[tuple[float, ...], ...]:
    """Return contravariant T^{mu nu} as a 4x4 tuple."""
    lag = lagrangian_density_3plus1(
        phi, clock, phi_derivatives, clock_derivatives, parameters
    )
    p = parameters
    raised_phi = (-phi_derivatives[0], *phi_derivatives[1:])
    raised_clock = (-clock_derivatives[0], *clock_derivatives[1:])
    return tuple(tuple(
        raised_phi[mu] * raised_phi[nu]
        + p.clock_kinetic * raised_clock[mu] * raised_clock[nu]
        + ((-1.0 if mu == nu == 0 else 1.0 if mu == nu else 0.0) * lag)
        for nu in range(4)) for mu in range(4))


def euler_lagrange_residuals_3plus1(
    phi: float, clock: float, phi_box: float, clock_box: float,
    parameters: CovariantParameters = CovariantParameters(),
) -> tuple[float, float]:
    p = parameters
    return (
        phi_box - p.field_mass**2 * phi
        + p.coupling * clock * coupling_derivative(phi),
        p.clock_kinetic * clock_box - p.clock_mass_squared * clock
        + p.coupling * coupling_function(phi),
    )


def divergence_identity_3plus1(
    phi_residual: float, clock_residual: float,
    phi_derivatives: tuple[float, float, float, float],
    clock_derivatives: tuple[float, float, float, float],
) -> tuple[float, float, float, float]:
    """Return R_phi*d^nu(phi)+R_T*d^nu(T), the off-shell divergence."""
    return tuple(
        phi_residual * (-phi_derivatives[0] if mu == 0 else phi_derivatives[mu])
        + clock_residual * (-clock_derivatives[0] if mu == 0 else clock_derivatives[mu])
        for mu in range(4)
    )


def on_shell_second_time_derivatives_3plus1(
    phi: float, clock: float,
    phi_laplacian: float, clock_laplacian: float,
    parameters: CovariantParameters = CovariantParameters(),
) -> tuple[float, float]:
    """Return time-time derivatives required by the equations for given spatial Laplacians."""
    p = parameters
    phi_tt = (phi_laplacian - p.field_mass**2 * phi
              + p.coupling * clock * coupling_derivative(phi))
    clock_tt = (clock_laplacian
                - (p.clock_mass_squared * clock
                   - p.coupling * coupling_function(phi)) / p.clock_kinetic)
    return phi_tt, clock_tt
