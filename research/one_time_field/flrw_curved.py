"""Experiment 12: two scalar fields on a prescribed spatially-flat FLRW background.

Metric signature (-,+,+,+), natural units c=1.  The scale factor is prescribed;
this module does not solve Einstein's equations or include metric backreaction.
"""
from __future__ import annotations

from math import isfinite
from .lorentz_covariant import CovariantParameters, coupling_function, coupling_derivative


def _finite(*values: float) -> None:
    if not all(isfinite(value) for value in values):
        raise ValueError("all inputs must be finite")


def flrw_metric(scale_factor: float) -> tuple[tuple[float, ...], ...]:
    """Return g_mu_nu=diag(-1,a^2,a^2,a^2) for a positive scale factor."""
    _finite(scale_factor)
    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    a2 = scale_factor * scale_factor
    return ((-1.0, 0.0, 0.0, 0.0),
            (0.0, a2, 0.0, 0.0),
            (0.0, 0.0, a2, 0.0),
            (0.0, 0.0, 0.0, a2))


def flrw_inverse_metric(scale_factor: float) -> tuple[tuple[float, ...], ...]:
    _finite(scale_factor)
    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    inv = 1.0 / (scale_factor * scale_factor)
    return ((-1.0, 0.0, 0.0, 0.0),
            (0.0, inv, 0.0, 0.0),
            (0.0, 0.0, inv, 0.0),
            (0.0, 0.0, 0.0, inv))


def metric_determinant(scale_factor: float) -> float:
    _finite(scale_factor)
    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    return -(scale_factor ** 6)


def volume_factor(scale_factor: float) -> float:
    """Return sqrt(-g)=a^3."""
    _finite(scale_factor)
    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    return scale_factor ** 3


def hubble_parameter(scale_factor: float, scale_factor_dot: float) -> float:
    _finite(scale_factor, scale_factor_dot)
    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    return scale_factor_dot / scale_factor


def scalar_dalembertian_homogeneous(
    field_dot: float, field_ddot: float, hubble: float
) -> float:
    """For a homogeneous scalar X(t), Box_g X=-(X_ddot+3 H X_dot)."""
    _finite(field_dot, field_ddot, hubble)
    return -(field_ddot + 3.0 * hubble * field_dot)


def lagrangian_density_flrw(
    phi: float, clock: float, phi_dot: float, clock_dot: float,
    parameters: CovariantParameters = CovariantParameters(),
) -> float:
    """Covariant scalar L density evaluated for homogeneous fields."""
    _finite(phi, clock, phi_dot, clock_dot)
    p = parameters
    return (
        0.5 * phi_dot**2 - 0.5 * p.field_mass**2 * phi**2
        + 0.5 * p.clock_kinetic * clock_dot**2
        - 0.5 * p.clock_mass_squared * clock**2
        + p.coupling * clock * coupling_function(phi)
    )


def euler_lagrange_residuals_flrw(
    phi: float, clock: float, phi_dot: float, clock_dot: float,
    phi_ddot: float, clock_ddot: float, hubble: float,
    parameters: CovariantParameters = CovariantParameters(),
) -> tuple[float, float]:
    """Return covariant E-L residuals (R_phi,R_T), zero on shell."""
    _finite(phi, clock, phi_dot, clock_dot, phi_ddot, clock_ddot, hubble)
    p = parameters
    phi_box = scalar_dalembertian_homogeneous(phi_dot, phi_ddot, hubble)
    clock_box = scalar_dalembertian_homogeneous(clock_dot, clock_ddot, hubble)
    return (
        phi_box - p.field_mass**2 * phi
        + p.coupling * clock * coupling_derivative(phi),
        p.clock_kinetic * clock_box - p.clock_mass_squared * clock
        + p.coupling * coupling_function(phi),
    )


def on_shell_accelerations_flrw(
    phi: float, clock: float, phi_dot: float, clock_dot: float, hubble: float,
    parameters: CovariantParameters = CovariantParameters(),
) -> tuple[float, float]:
    """Return (phi_ddot,T_ddot) from the homogeneous field equations."""
    _finite(phi, clock, phi_dot, clock_dot, hubble)
    p = parameters
    if p.clock_kinetic <= 0.0:
        raise ValueError("clock_kinetic must be positive")
    phi_ddot = (
        -3.0 * hubble * phi_dot - p.field_mass**2 * phi
        + p.coupling * clock * coupling_derivative(phi)
    )
    clock_ddot = (
        -3.0 * hubble * clock_dot
        - (p.clock_mass_squared * clock
           - p.coupling * coupling_function(phi)) / p.clock_kinetic
    )
    return phi_ddot, clock_ddot


def energy_density_pressure_flrw(
    phi: float, clock: float, phi_dot: float, clock_dot: float,
    parameters: CovariantParameters = CovariantParameters(),
) -> tuple[float, float]:
    """Return homogeneous energy density rho and isotropic pressure p."""
    _finite(phi, clock, phi_dot, clock_dot)
    q = parameters
    kinetic = 0.5 * phi_dot**2 + 0.5 * q.clock_kinetic * clock_dot**2
    potential = (
        0.5 * q.field_mass**2 * phi**2
        + 0.5 * q.clock_mass_squared * clock**2
        - q.coupling * clock * coupling_function(phi)
    )
    return kinetic + potential, kinetic - potential


def stress_energy_tensor_flrw(
    phi: float, clock: float, phi_dot: float, clock_dot: float,
    scale_factor: float,
    parameters: CovariantParameters = CovariantParameters(),
) -> tuple[tuple[float, ...], ...]:
    """Return covariant T_mu_nu for homogeneous fields in comoving coordinates."""
    rho, pressure = energy_density_pressure_flrw(
        phi, clock, phi_dot, clock_dot, parameters
    )
    metric = flrw_metric(scale_factor)
    return tuple(tuple(
        (rho if mu == nu == 0 else
         pressure * metric[mu][nu] if mu == nu and mu > 0 else 0.0)
        for nu in range(4)) for mu in range(4))


def continuity_residual_flrw(
    phi_dot: float, clock_dot: float,
    phi_residual: float, clock_residual: float,
) -> float:
    """Return dot(rho)+3H(rho+p) from the off-shell E-L identity.

    With the residual convention used here this equals
    -phi_dot*R_phi-clock_dot*R_T.
    """
    _finite(phi_dot, clock_dot, phi_residual, clock_residual)
    return -phi_dot * phi_residual - clock_dot * clock_residual
