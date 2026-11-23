"""Experiment 13: metric variation and FLRW Einstein equations."""
from __future__ import annotations
from math import isfinite
from .flrw_curved import energy_density_pressure_flrw

def _finite(*values: float) -> None:
    if not all(isfinite(v) for v in values):
        raise ValueError("all inputs must be finite")

def ricci_scalar_flrw(hubble: float, hubble_dot: float) -> float:
    """R=6(dot(H)+2H^2), spatially flat FLRW, signature (-,+,+,+)."""
    _finite(hubble, hubble_dot)
    return 6.0 * (hubble_dot + 2.0 * hubble**2)

def einstein_tensor_flrw(scale_factor: float, hubble: float, hubble_dot: float):
    """Return covariant G_mu_nu=diag(3H^2,a^2*(-2Hdot-3H^2),...)."""
    _finite(scale_factor, hubble, hubble_dot)
    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    spatial = scale_factor**2 * (-2.0*hubble_dot - 3.0*hubble**2)
    return ((3.0*hubble**2, 0.0, 0.0, 0.0),
            (0.0, spatial, 0.0, 0.0),
            (0.0, 0.0, spatial, 0.0),
            (0.0, 0.0, 0.0, spatial))

def friedmann_residual(hubble: float, energy_density: float, planck_mass_squared: float) -> float:
    _finite(hubble, energy_density, planck_mass_squared)
    if planck_mass_squared <= 0.0:
        raise ValueError("planck_mass_squared must be positive")
    return 3.0*planck_mass_squared*hubble**2 - energy_density

def acceleration_residual(hubble_dot: float, energy_density: float, pressure: float, planck_mass_squared: float) -> float:
    _finite(hubble_dot, energy_density, pressure, planck_mass_squared)
    if planck_mass_squared <= 0.0:
        raise ValueError("planck_mass_squared must be positive")
    return -2.0*planck_mass_squared*hubble_dot - energy_density - pressure

def einstein_equation_residuals_flrw(
    scale_factor: float, hubble: float, hubble_dot: float,
    phi: float, clock: float, phi_dot: float, clock_dot: float,
    planck_mass_squared: float, parameters=None,
) -> tuple[float, float]:
    """Return 00 and spatial Einstein-equation residuals for scalar matter."""
    from .lorentz_covariant import CovariantParameters
    p = parameters or CovariantParameters()
    rho, pressure = energy_density_pressure_flrw(phi, clock, phi_dot, clock_dot, p)
    return (friedmann_residual(hubble, rho, planck_mass_squared),
            acceleration_residual(hubble_dot, rho, pressure, planck_mass_squared))

def friedmann_constraint_propagation(
    hubble: float, hubble_dot: float, density_dot: float, planck_mass_squared: float,
) -> float:
    """Return d/dt(3 Mpl^2 H^2-rho); zero under acceleration + continuity."""
    _finite(hubble, hubble_dot, density_dot, planck_mass_squared)
    if planck_mass_squared <= 0.0:
        raise ValueError("planck_mass_squared must be positive")
    return 6.0*planck_mass_squared*hubble*hubble_dot - density_dot
