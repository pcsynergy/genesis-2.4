"""UPT-16: a common hybrid state contract and dynamics compatibility tests.

This module formalizes the interfaces between UPT layers. It deliberately
does not assert that the operators are all consequences of one physical law.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from typing import Sequence


class PotentialEnergyOntology(str, Enum):
    POTENTIAL_FIRST = "potential_first"
    CO_FUNDAMENTAL = "co_fundamental"
    UNDECIDED = "undecided"


@dataclass(frozen=True)
class HybridUPTState:
    """A model state with explicit admissibility, field, memory, and relations."""
    admissible_states: tuple[tuple[int, ...], ...]
    field: tuple[float, ...]
    memory: float
    adjacency: tuple[tuple[float, ...], ...]
    evolution_parameter: float = 0.0

    def __post_init__(self):
        n = len(self.field)
        if n < 1 or len(self.adjacency) != n or any(len(r) != n for r in self.adjacency):
            raise ValueError("field and adjacency dimensions must agree and be nonempty")
        if any(not isfinite(v) for v in self.field) or not isfinite(self.memory):
            raise ValueError("field and memory must be finite")
        if not isfinite(self.evolution_parameter):
            raise ValueError("evolution_parameter must be finite")
        if any(not isfinite(v) or v < 0 for row in self.adjacency for v in row):
            raise ValueError("adjacency weights must be finite and nonnegative")
        if any(abs(self.adjacency[i][j] - self.adjacency[j][i]) > 1e-12
               for i in range(n) for j in range(n)):
            raise ValueError("adjacency must be symmetric")
        normalized = tuple(tuple(int(x) for x in state) for state in self.admissible_states)
        if any(len(state) != n or any(x not in (0, 1) for x in state)
               for state in normalized):
            raise ValueError("admissible configurations must be binary and match field size")
        if len(set(normalized)) != len(normalized):
            raise ValueError("admissible configurations must be unique")
        object.__setattr__(self, "admissible_states", normalized)


def gradient_flow_rhs(gradient: Sequence[float],
                      mobility: Sequence[Sequence[float]]) -> tuple[float, ...]:
    """Return -M grad(H), requiring a symmetric positive-semidefinite mobility."""
    g = tuple(float(v) for v in gradient)
    m = tuple(tuple(float(v) for v in row) for row in mobility)
    n = len(g)
    if n == 0 or len(m) != n or any(len(row) != n for row in m):
        raise ValueError("gradient and mobility dimensions must agree and be nonempty")
    if any(not isfinite(v) for v in g) or any(not isfinite(v) for row in m for v in row):
        raise ValueError("gradient and mobility must be finite")
    if any(abs(m[i][j] - m[j][i]) > 1e-10 for i in range(n) for j in range(n)):
        raise ValueError("mobility must be symmetric")
    # Sylvester/eigenvalue-free PSD check by all principal minors for small research matrices.
    # Use Cholesky-like LDL pivots with a tolerance; reject negative pivots.
    a = [list(row) for row in m]
    tol = 1e-10
    for k in range(n):
        pivot = a[k][k]
        if pivot < -tol:
            raise ValueError("mobility must be positive semidefinite")
        if pivot <= tol:
            if any(abs(a[i][k]) > tol for i in range(k + 1, n)):
                raise ValueError("mobility must be positive semidefinite")
            continue
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] -= a[i][k] * a[k][j] / pivot
    return tuple(-sum(m[i][j] * g[j] for j in range(n)) for i in range(n))


def energy_rate(gradient: Sequence[float], velocity: Sequence[float]) -> float:
    g, v = tuple(gradient), tuple(velocity)
    if len(g) != len(v) or not g:
        raise ValueError("gradient and velocity must have equal nonzero length")
    if any(not isfinite(float(x)) for x in g + v):
        raise ValueError("gradient and velocity must be finite")
    return sum(float(a) * float(b) for a, b in zip(g, v))


def hamiltonian_rhs(gradient: Sequence[float],
                    structure: Sequence[Sequence[float]]) -> tuple[float, ...]:
    """Return J grad(H); caller supplies an antisymmetric structure matrix."""
    g = tuple(float(v) for v in gradient)
    j = tuple(tuple(float(v) for v in row) for row in structure)
    n = len(g)
    if n == 0 or len(j) != n or any(len(row) != n for row in j):
        raise ValueError("gradient and structure dimensions must agree and be nonempty")
    if any(not isfinite(v) for v in g) or any(not isfinite(v) for row in j for v in row):
        raise ValueError("gradient and structure must be finite")
    if any(abs(j[i][k] + j[k][i]) > 1e-10 for i in range(n) for k in range(n)):
        raise ValueError("Hamiltonian structure must be antisymmetric")
    return tuple(sum(j[i][k] * g[k] for k in range(n)) for i in range(n))


def classify_common_energy_compatibility(gradient: Sequence[float],
                                         mobility: Sequence[Sequence[float]],
                                         structure: Sequence[Sequence[float]],
                                         tolerance: float = 1e-10) -> dict:
    """Show whether the same nonstationary velocity can be gradient and Hamiltonian.

    For positive-definite M, -M grad(H) dissipates H strictly away from critical
    points; for antisymmetric J, J grad(H) conserves H. Equality is impossible
    away from critical points. Semidefinite M can have degenerate directions.
    """
    g = tuple(float(v) for v in gradient)
    dissipative = gradient_flow_rhs(g, mobility)
    conservative = hamiltonian_rhs(g, structure)
    d_rate = energy_rate(g, dissipative)
    h_rate = energy_rate(g, conservative)
    same = len(dissipative) == len(conservative) and all(
        abs(a - b) <= tolerance for a, b in zip(dissipative, conservative)
    )
    stationary = all(abs(v) <= tolerance for v in g)
    return {
        "gradient_flow_velocity": dissipative,
        "hamiltonian_velocity": conservative,
        "gradient_flow_energy_rate": d_rate,
        "hamiltonian_energy_rate": h_rate,
        "same_velocity": same,
        "stationary_gradient": stationary,
        "nontrivial_dual_dynamics_compatible": same and not stationary,
        "result": (
            "compatible only at a stationary/degenerate point"
            if same else "distinct vector fields; a coupling or limiting derivation is required"
        ),
    }


def observation_map(field: Sequence[float], weights: Sequence[float] | None = None) -> float:
    """A declared scalar measurement map; not an identity between state and experience."""
    x = tuple(float(v) for v in field)
    if not x or any(not isfinite(v) for v in x):
        raise ValueError("field must be nonempty and finite")
    w = tuple(1.0 for _ in x) if weights is None else tuple(float(v) for v in weights)
    if len(w) != len(x) or any(not isfinite(v) for v in w):
        raise ValueError("weights must be finite and match field size")
    return sum(a * b for a, b in zip(x, w))


def potential_energy_status(ontology: PotentialEnergyOntology) -> dict:
    """Keep ontological Potential distinct from a model's energy functional."""
    return {
        "hypothesis": PotentialEnergyOntology(ontology).value,
        "ontological_potential_equals_energy_functional": False,
        "decision": "unresolved by the current mathematical prototypes",
    }
