"""Experiment 9: Lorentz-covariant scalar/clock fields in 1+1 Minkowski spacetime.

Metric signature (-,+). Both fields are Lorentz scalars and share one
Minkowski light cone. This is a classical field-theory ansatz on fixed flat
spacetime, not a dynamical theory of gravity or a measured theory of time.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt


@dataclass(frozen=True)
class CovariantParameters:
    field_mass: float = 0.4
    clock_kinetic: float = 1.0
    clock_mass_squared: float = 0.8
    coupling: float = 0.05

    def __post_init__(self):
        values = (self.field_mass, self.clock_kinetic,
                  self.clock_mass_squared, self.coupling)
        if not all(isfinite(float(v)) for v in values):
            raise ValueError("parameters must be finite")
        if self.field_mass < 0 or self.clock_kinetic <= 0:
            raise ValueError("field mass must be nonnegative and clock kinetic coefficient positive")
        if self.clock_mass_squared <= 0:
            raise ValueError("clock mass-squared must be positive")


def coupling_function(phi: float) -> float:
    """Bounded smooth scalar coupling f(phi)."""
    return 0.5 * phi * phi / (1.0 + phi * phi)


def coupling_derivative(phi: float) -> float:
    return phi / (1.0 + phi * phi) ** 2


def minkowski_gradient_norm(derivatives: tuple[float, float]) -> float:
    """Return eta^{mu nu} d_mu u d_nu u for signature (-,+)."""
    dt, dx = derivatives
    return -dt * dt + dx * dx


def lorentz_boost_gradient(
    derivatives: tuple[float, float], velocity: float
) -> tuple[float, float]:
    """Transform covector components (d_t u, d_x u) to boosted coordinates."""
    if not isfinite(velocity) or abs(velocity) >= 1.0:
        raise ValueError("boost velocity must be finite and subluminal")
    dt, dx = derivatives
    gamma = 1.0 / sqrt(1.0 - velocity * velocity)
    return gamma * (dt + velocity * dx), gamma * (velocity * dt + dx)


def lagrangian_density(
    phi: float,
    clock: float,
    phi_derivatives: tuple[float, float],
    clock_derivatives: tuple[float, float],
    parameters: CovariantParameters = CovariantParameters(),
) -> float:
    """Lorentz scalar L density for two real scalar fields."""
    p = parameters
    phi_norm = minkowski_gradient_norm(phi_derivatives)
    clock_norm = minkowski_gradient_norm(clock_derivatives)
    return (
        -0.5 * phi_norm
        -0.5 * p.field_mass**2 * phi**2
        -0.5 * p.clock_kinetic * clock_norm
        -0.5 * p.clock_mass_squared * clock**2
        + p.coupling * clock * coupling_function(phi)
    )


def d_alembertian(second_derivatives: tuple[float, float]) -> float:
    """Return box u = -d_tt u + d_xx u in 1+1 dimensions."""
    dtt, dxx = second_derivatives
    return -dtt + dxx


def lorentz_boost_second_derivatives(
    second_derivatives: tuple[float, float], velocity: float
) -> tuple[float, float]:
    """Transform (d_tt u, d_xx u) for a boost when mixed derivative is zero.

    The test helper deliberately accepts the mixed derivative separately in
    lorentz_boost_hessian; this convenience function is for diagonal Hessians.
    """
    return lorentz_boost_hessian(second_derivatives[0], 0.0,
                                 second_derivatives[1], velocity)


def lorentz_boost_hessian(
    dtt: float, dtx: float, dxx: float, velocity: float
) -> tuple[float, float, float]:
    """Transform a symmetric 1+1 Hessian under a Lorentz boost."""
    if not isfinite(velocity) or abs(velocity) >= 1.0:
        raise ValueError("boost velocity must be finite and subluminal")
    gamma = 1.0 / sqrt(1.0 - velocity * velocity)
    # Derivatives in primed coordinates: d_t' = gamma(d_t + v d_x),
    # d_x' = gamma(v d_t + d_x).
    dtt_p = gamma**2 * (dtt + 2.0 * velocity * dtx + velocity**2 * dxx)
    dxx_p = gamma**2 * (velocity**2 * dtt + 2.0 * velocity * dtx + dxx)
    dtx_p = gamma**2 * (velocity * dtt + (1.0 + velocity**2) * dtx
                        + velocity * dxx)
    return dtt_p, dtx_p, dxx_p


def euler_lagrange_residuals(
    phi: float,
    clock: float,
    phi_box: float,
    clock_box: float,
    parameters: CovariantParameters = CovariantParameters(),
) -> tuple[float, float]:
    """Residuals of box(phi)-m²phi+g*T*f'(phi)=0 and
    Z*box(T)-mu_T²*T+g*f(phi)=0.
    """
    p = parameters
    r_phi = (phi_box - p.field_mass**2 * phi
             + p.coupling * clock * coupling_derivative(phi))
    r_clock = (p.clock_kinetic * clock_box
               - p.clock_mass_squared * clock
               + p.coupling * coupling_function(phi))
    return r_phi, r_clock
