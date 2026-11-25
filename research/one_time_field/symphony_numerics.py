"""Numerical integrators and convergence probes for phase-oscillator networks."""
from __future__ import annotations
from math import cos, sin, pi, isfinite


def phase_rhs(phases, adjacency, frequencies, coupling):
    n = len(phases)
    out = []
    for i in range(n):
        degree = sum(adjacency[i])
        interaction = 0.0 if degree == 0 else sum(
            adjacency[i][j] * sin(phases[j] - phases[i]) for j in range(n)
        ) / degree
        out.append(frequencies[i] + coupling * interaction)
    return out


def integrate(phases, adjacency, frequencies, coupling, dt, steps, method="rk4"):
    """Integrate phases; intermediate phases may remain unwrapped."""
    if not isfinite(dt) or dt <= 0:
        raise ValueError("dt must be finite and positive")
    if not isinstance(steps, int) or steps < 0:
        raise ValueError("steps must be a nonnegative integer")
    if method not in ("euler", "rk4"):
        raise ValueError("method must be euler or rk4")
    y = [float(x) for x in phases]
    n = len(y)
    if n == 0 or len(adjacency) != n or len(frequencies) != n:
        raise ValueError("phase, adjacency, and frequency dimensions must agree")
    if any(len(row) != n for row in adjacency):
        raise ValueError("adjacency must be square")
    for _ in range(steps):
        k1 = phase_rhs(y, adjacency, frequencies, coupling)
        if method == "euler":
            y = [a + dt * b for a, b in zip(y, k1)]
            continue
        y2 = [a + 0.5 * dt * b for a, b in zip(y, k1)]
        k2 = phase_rhs(y2, adjacency, frequencies, coupling)
        y3 = [a + 0.5 * dt * b for a, b in zip(y, k2)]
        k3 = phase_rhs(y3, adjacency, frequencies, coupling)
        y4 = [a + dt * b for a, b in zip(y, k3)]
        k4 = phase_rhs(y4, adjacency, frequencies, coupling)
        y = [a + dt * (b + 2*c + 2*d + e) / 6.0
             for a, b, c, d, e in zip(y, k1, k2, k3, k4)]
    return [x % (2.0 * pi) for x in y]


def order_parameter(phases):
    n = len(phases)
    if n == 0:
        raise ValueError("at least one phase is required")
    x = sum(cos(p) for p in phases) / n
    y = sum(sin(p) for p in phases) / n
    return (x*x + y*y) ** 0.5


def circular_distance(a, b):
    """Absolute shortest angular distance in radians."""
    return abs((a - b + pi) % (2.0 * pi) - pi)


def phase_error(reference, candidate):
    if len(reference) != len(candidate) or not reference:
        raise ValueError("phase vectors must be nonempty and equal length")
    # Remove the arbitrary common phase by anchoring both vectors to node zero.
    ref0, got0 = reference[0], candidate[0]
    errors = [circular_distance((r-ref0) % (2*pi), (g-got0) % (2*pi))
              for r, g in zip(reference, candidate)]
    return (sum(e*e for e in errors) / len(errors)) ** 0.5
