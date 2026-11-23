"""Comparative clock models for One Time Field Theory research.

These are transparent mathematical prototypes, not claims that any clock
definition is the uniquely correct physical time.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


def _positive(value: float, name: str) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _nonnegative(value: float, name: str) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


@dataclass
class ExternalClock:
    """A clock identified with the chosen external evolution parameter."""
    reading: float = 0.0

    def advance(self, d_lambda: float) -> float:
        _positive(d_lambda, "d_lambda")
        self.reading += d_lambda
        return self.reading


@dataclass
class RelationalClock:
    """Internal clock with d(tau)/d(lambda) = rate(state) > 0."""
    reading: float = 0.0

    def advance(self, d_lambda: float, rate: float) -> float:
        _positive(d_lambda, "d_lambda")
        _positive(rate, "rate")
        self.reading += rate * d_lambda
        return self.reading

    @staticmethod
    def reparameterized_rhs(rhs_lambda: float, rate: float) -> float:
        """Chain rule: dq/dtau = (dq/dlambda)/(dtau/dlambda)."""
        _positive(rate, "rate")
        if not isfinite(rhs_lambda):
            raise ValueError("rhs_lambda must be finite")
        return rhs_lambda / rate


@dataclass
class EntropyProductionClock:
    """Accumulates nonnegative entropy production, not raw system entropy."""
    reading: float = 0.0

    def advance(self, d_lambda: float, production_rate: float) -> float:
        _positive(d_lambda, "d_lambda")
        _nonnegative(production_rate, "production_rate")
        self.reading += production_rate * d_lambda
        return self.reading


@dataclass
class EventClock:
    """Counts discrete events; count is not duration without calibration."""
    count: int = 0

    def advance(self, events: int) -> int:
        if not isinstance(events, int) or isinstance(events, bool) or events < 0:
            raise ValueError("events must be a nonnegative integer")
        self.count += events
        return self.count


@dataclass
class ObserverClock:
    """Phenomenological duration proxy kept separate from physical clocks."""
    reading: float = 0.0
    minimum_rate: float = 0.05

    def __post_init__(self) -> None:
        _positive(self.minimum_rate, "minimum_rate")

    def advance(self, d_lambda: float, activity: float,
                sensitivity: float = 0.0, reference: float = 0.0) -> float:
        _positive(d_lambda, "d_lambda")
        _nonnegative(activity, "activity")
        _nonnegative(reference, "reference")
        if not isfinite(sensitivity):
            raise ValueError("sensitivity must be finite")
        rate = max(self.minimum_rate, 1.0 + sensitivity * (activity - reference))
        self.reading += rate * d_lambda
        return self.reading


@dataclass
class HybridClock:
    """Tracks several clock hypotheses without collapsing them into one."""
    external: ExternalClock | None = None
    relational: RelationalClock | None = None
    entropy: EntropyProductionClock | None = None
    events: EventClock | None = None
    observer: ObserverClock | None = None

    def snapshot(self) -> dict[str, float | int]:
        result: dict[str, float | int] = {}
        for name in ("external", "relational", "entropy", "events", "observer"):
            clock = getattr(self, name)
            if clock is not None:
                result[name] = clock.count if isinstance(clock, EventClock) else clock.reading
        return result
