"""UPT-12: dimensional scaling and observable identifiability.

The model remains a phenomenological reaction-diffusion/gradient-flow
system. This module supplies unit-consistent parameter bookkeeping and
compares memory-coupled and uncoupled model trajectories.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence

from .upt11_continuum_limit import UPTContinuumLimit


@dataclass(frozen=True)
class PhysicalScales:
    """Reference scales: length [L], time [T], field [Phi], energy [E]."""
    length: float
    time: float
    field: float
    energy: float

    def __post_init__(self):
        for name in ("length", "time", "field", "energy"):
            value = getattr(self, name)
            if not isfinite(value) or value <= 0:
                raise ValueError(f"{name} scale must be finite and positive")


@dataclass(frozen=True)
class DimensionfulParameters:
    """SI-like dimensional parameters for the UPT-11 continuum energy."""
    relational_strength: float  # [E L / Phi^2]
    memory_strength: float      # [E / (L Phi^2)]
    bistable_strength: float    # [E / (L Phi^4)]
    field_mobility: float       # [Phi L / (E T)]
    memory_mobility: float      # [Phi L / (E T)]

    def __post_init__(self):
        for name in self.__dataclass_fields__:
            value = getattr(self, name)
            if not isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and nonnegative")

    def dimensionless(self, scales: PhysicalScales):
        """Return coefficients in coordinates x/L0, t/T0, phi/Phi0, H/E0."""
        L, T, P, E = scales.length, scales.time, scales.field, scales.energy
        return {
            "relational_strength": self.relational_strength * P**2 / (E * L),
            "memory_strength": self.memory_strength * L * P**2 / E,
            "bistable_strength": self.bistable_strength * L * P**4 / E,
            "field_mobility": self.field_mobility * E * T / (P * L),
            "memory_mobility": self.memory_mobility * E * T / (P * L),
        }


def compare_memory_coupling(*, node_count=64, final_time=0.02,
                            memory_strength=0.5, cfl=0.12):
    """Compare matched UPT-11 runs with kappa>0 and kappa=0.

    The initial field and memory are identical. Returned differences are
    model-level effects, not empirical predictions.
    """
    coupled = UPTContinuumLimit(node_count=node_count,
                                 memory_strength=memory_strength)
    uncoupled = UPTContinuumLimit(node_count=node_count,
                                   memory_strength=0.0)
    coupled_result = coupled.evolve(final_time, cfl=cfl)
    uncoupled_result = uncoupled.evolve(final_time, cfl=cfl)
    return {
        "coupled": coupled_result,
        "uncoupled": uncoupled_result,
        "difference": {
            key: coupled_result[key] - uncoupled_result[key]
            for key in ("mean_field", "field_variance", "memory", "energy")
        },
        "memory_strength": memory_strength,
        "interpretation": "synthetic model comparison; no data calibration",
    }


def infer_memory_relaxation_product(times: Sequence[float],
                                    memory_values: Sequence[float],
                                    mismatch_values: Sequence[float]):
    """Estimate gamma_m*kappa from dm/dt = gamma_m*kappa*(mean(phi)-m).

    A least-squares slope through the origin is returned. With only m(t) and
    mismatch(t), gamma_m and kappa are structurally confounded: only their
    product is identifiable. A zero mismatch design has no information.
    """
    if len(times) < 3 or len(times) != len(memory_values) or len(times) != len(mismatch_values):
        raise ValueError("times, memory_values and mismatch_values need equal length >= 3")
    if any(not isfinite(float(v)) for seq in (times, memory_values, mismatch_values) for v in seq):
        raise ValueError("all observations must be finite")
    if any(times[i+1] <= times[i] for i in range(len(times)-1)):
        raise ValueError("times must be strictly increasing")
    slopes = [(memory_values[i+1]-memory_values[i])/(times[i+1]-times[i])
              for i in range(len(times)-1)]
    predictors = [(mismatch_values[i+1]+mismatch_values[i])/2
                  for i in range(len(times)-1)]
    denom = sum(v*v for v in predictors)
    if denom <= 1e-24:
        raise ValueError("mismatch signal is zero; relaxation rate is unidentifiable")
    estimate = sum(x*y for x, y in zip(predictors, slopes))/denom
    return {
        "gamma_m_times_kappa": estimate,
        "separately_identifiable": False,
        "identifiability_note": "Only gamma_m*kappa is identifiable from this observable equation without independent information about either factor.",
    }
