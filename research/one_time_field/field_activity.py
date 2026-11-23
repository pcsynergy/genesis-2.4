"""Field-derived activity observables for the OTFT temporal experiments.

Activity is a model observable built from squared state derivatives. Its
weights must be dimensionally calibrated before physical interpretation.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any


@dataclass(frozen=True)
class FieldActivity:
    """Per-domain mean-square rates and their weighted aggregate."""

    scalar: float
    phase: float
    tensor: float
    total: float

    @classmethod
    def from_engine(
        cls,
        engine: Any,
        *,
        scalar_weight: float = 1.0,
        phase_weight: float = 1.0,
        tensor_weight: float = 1.0,
        scalar_source: list[float] | None = None,
    ) -> "FieldActivity":
        """Calculate derivative activity; scalar_source is the total scalar forcing."""
        weights = {
            "scalar": scalar_weight,
            "phase": phase_weight,
            "tensor": tensor_weight,
        }
        for name, weight in weights.items():
            if not isfinite(weight) or weight < 0.0:
                raise ValueError(f"{name}_weight must be finite and nonnegative")

        contributions = {"scalar": 0.0, "phase": 0.0, "tensor": 0.0}
        if engine.scalar is not None:
            rates = engine.scalar.derivative(source=scalar_source)
            contributions["scalar"] = sum(v * v for v in rates) / len(rates)
        if engine.harmonic is not None:
            rates = engine.harmonic.derivative()
            contributions["phase"] = sum(v * v for v in rates) / len(rates)
        if engine.tensor is not None:
            rates = engine.tensor.derivative()
            count = sum(len(row) for row in rates)
            contributions["tensor"] = (
                sum(v * v for row in rates for v in row) / count
            )

        for name, value in contributions.items():
            if not isfinite(value):
                raise ValueError(f"{name} activity is not finite")
        total = sum(weights[name] * contributions[name] for name in contributions)
        if not isfinite(total):
            raise ValueError("total activity is not finite")
        return cls(
            scalar=contributions["scalar"],
            phase=contributions["phase"],
            tensor=contributions["tensor"],
            total=total,
        )

    def relational_rate(self, gain: float = 1.0, baseline: float = 1.0) -> float:
        """Return baseline + gain*activity, requiring a positive finite rate.

        gain and baseline carry the units needed to make this expression
        dimensionally consistent; defaults are dimensionless toy settings.
        """
        if not isfinite(gain) or gain < 0.0:
            raise ValueError("gain must be finite and nonnegative")
        if not isfinite(baseline) or baseline <= 0.0:
            raise ValueError("baseline must be finite and positive")
        rate = baseline + gain * self.total
        if not isfinite(rate) or rate <= 0.0:
            raise ValueError("relational rate must be finite and positive")
        return rate
