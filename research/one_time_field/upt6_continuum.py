"""UPT-6: Noether shift symmetry and continuum field-equation probes.

These routines are small numerical/theoretical probes, not a new physical
theory. The massless wave model is the standard shift-symmetric scalar field;
the diffusion model is a dissipative gradient-flow equation.
"""
from __future__ import annotations
from math import isfinite
from typing import Sequence

def _validate_periodic(values: Sequence[float], dx: float) -> list[float]:
    data = [float(value) for value in values]
    if len(data) < 3 or not all(isfinite(x) for x in data):
        raise ValueError("periodic field requires at least three finite values")
    if not isfinite(dx) or dx <= 0.0:
        raise ValueError("dx must be finite and positive")
    return data

def periodic_laplacian(values: Sequence[float], dx: float) -> list[float]:
    """Second-order centered periodic approximation to d²phi/dx²."""
    data = _validate_periodic(values, dx)
    n, scale = len(data), dx * dx
    return [(data[(i + 1) % n] - 2.0 * data[i] + data[(i - 1) % n]) / scale for i in range(n)]

def massless_wave_acceleration(values: Sequence[float], dx: float, wave_speed: float = 1.0) -> list[float]:
    """Semi-discrete massless wave equation: phi_tt = c² phi_xx."""
    if not isfinite(wave_speed) or wave_speed <= 0.0:
        raise ValueError("wave_speed must be finite and positive")
    return [wave_speed**2 * x for x in periodic_laplacian(values, dx)]

def diffusion_rate(values: Sequence[float], dx: float, diffusivity: float = 1.0) -> list[float]:
    """Semi-discrete diffusion equation: phi_t = D phi_xx."""
    if not isfinite(diffusivity) or diffusivity < 0.0:
        raise ValueError("diffusivity must be finite and nonnegative")
    return [diffusivity * x for x in periodic_laplacian(values, dx)]

def shift_noether_charge(velocities: Sequence[float], dx: float) -> float:
    """Spatial integral of pi=phi_t for a shift-symmetric scalar.

    For L = 1/2 (partial_t phi)^2 - 1/2 c² (partial_x phi)^2,
    invariance under phi -> phi + epsilon gives Q = integral dx phi_t.
    """
    return dx * sum(_validate_periodic(velocities, dx))

def periodic_wave_energy(values: Sequence[float], velocities: Sequence[float], dx: float, wave_speed: float = 1.0) -> float:
    """Discrete standard massless-wave energy on a periodic lattice."""
    field = _validate_periodic(values, dx)
    speed = float(wave_speed)
    if len(field) != len(velocities):
        raise ValueError("field and velocity arrays must have equal length")
    vel = [float(x) for x in velocities]
    if not all(isfinite(x) for x in vel):
        raise ValueError("velocities must be finite")
    if not isfinite(speed) or speed <= 0.0:
        raise ValueError("wave_speed must be finite and positive")
    gradient = [(field[(i + 1) % len(field)] - field[i]) / dx for i in range(len(field))]
    return 0.5 * dx * sum(vel[i]**2 + speed**2 * gradient[i]**2 for i in range(len(field)))

def shift_symmetry_status(potential_is_constant: bool) -> str:
    """Classify invariance under constant field shifts for V(phi)."""
    return "shift_symmetric" if potential_is_constant else "explicitly_broken"
