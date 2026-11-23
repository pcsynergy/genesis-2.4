"""Temporal layer: computational, relational, and observer clocks.

The relational and observer clocks are phenomenological model variables. They
do not replace the computational parameter or claim to derive physical time.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass
class TemporalLayer:
    """Accumulate three clocks from a nonnegative field-activity signal.

    parameter_time is the simulation parameter. relational_time runs at
    1 + relational_gain * activity. observer_time runs at
    max(min_observer_rate, 1 + observer_gain * (activity-reference_activity)).

    Gains and rates are model parameters. observer_time is a phenomenological
    perception proxy, not a universal law of consciousness.
    """

    relational_gain: float = 0.0
    observer_gain: float = 0.0
    reference_activity: float = 0.0
    min_observer_rate: float = 0.05
    parameter_time: float = 0.0
    relational_time: float = 0.0
    observer_time: float = 0.0
    accumulated_activity: float = 0.0
    steps: int = 0

    def __post_init__(self) -> None:
        for name in ("relational_gain", "observer_gain", "reference_activity",
                     "min_observer_rate", "parameter_time", "relational_time",
                     "observer_time", "accumulated_activity"):
            value = getattr(self, name)
            if not isfinite(value):
                raise ValueError(f"{name} must be finite")
        if self.reference_activity < 0.0:
            raise ValueError("reference_activity must be nonnegative")
        if self.min_observer_rate <= 0.0:
            raise ValueError("min_observer_rate must be positive")
        if min(self.parameter_time, self.relational_time,
               self.observer_time, self.accumulated_activity) < 0.0:
            raise ValueError("clock values and accumulated_activity must be nonnegative")
        if not isinstance(self.steps, int) or self.steps < 0:
            raise ValueError("steps must be a nonnegative integer")

    def advance(self, parameter_step: float, event_activity: float) -> dict[str, float | int]:
        """Advance clocks by one step using a supplied field-activity rate."""
        if not isfinite(parameter_step) or parameter_step <= 0.0:
            raise ValueError("parameter_step must be finite and positive")
        if not isfinite(event_activity) or event_activity < 0.0:
            raise ValueError("event_activity must be finite and nonnegative")

        relational_rate = 1.0 + self.relational_gain * event_activity
        observer_rate = max(
            self.min_observer_rate,
            1.0 + self.observer_gain * (event_activity - self.reference_activity),
        )
        if relational_rate <= 0.0 or not isfinite(relational_rate):
            raise ValueError("relational clock rate must remain finite and positive")

        self.parameter_time += parameter_step
        self.relational_time += parameter_step * relational_rate
        self.observer_time += parameter_step * observer_rate
        self.accumulated_activity += parameter_step * event_activity
        self.steps += 1
        return self.snapshot()

    def snapshot(self) -> dict[str, float | int]:
        return {
            "parameter_time": self.parameter_time,
            "relational_time": self.relational_time,
            "observer_time": self.observer_time,
            "accumulated_activity": self.accumulated_activity,
            "steps": self.steps,
        }
