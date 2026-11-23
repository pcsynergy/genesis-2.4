"""Exact two-node relational coupling model for the UPT-3 toy experiment.

This is a mathematical consensus model, not a claim about fundamental physics.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite


@dataclass(frozen=True)
class TwoNodeRelationalModel:
    """Two distinguishable scalar states coupled by a symmetric relation.

    Equations:
        dx1/dt = coupling * (x2 - x1)
        dx2/dt = coupling * (x1 - x2)

    The common mode is conserved; the difference mode decays exponentially.
    """

    initial: tuple[float, float]
    coupling: float

    def __post_init__(self) -> None:
        if len(self.initial) != 2 or not all(isfinite(float(x)) for x in self.initial):
            raise ValueError("initial must contain exactly two finite states")
        if not isfinite(self.coupling) or self.coupling < 0.0:
            raise ValueError("coupling must be finite and nonnegative")

    @property
    def initial_mean(self) -> float:
        return 0.5 * (self.initial[0] + self.initial[1])

    @property
    def initial_difference(self) -> float:
        return self.initial[0] - self.initial[1]

    def state(self, time: float) -> tuple[float, float]:
        """Return the exact state at nonnegative model time."""
        if not isfinite(time) or time < 0.0:
            raise ValueError("time must be finite and nonnegative")
        mean = self.initial_mean
        difference = self.initial_difference * exp(-2.0 * self.coupling * time)
        return (mean + 0.5 * difference, mean - 0.5 * difference)

    def relational_energy(self, time: float) -> float:
        """Return E = coupling/2 * (x1 - x2)^2."""
        x1, x2 = self.state(time)
        return 0.5 * self.coupling * (x1 - x2) ** 2

    def consensus_error(self, time: float) -> float:
        """Absolute distance between the two components."""
        x1, x2 = self.state(time)
        return abs(x1 - x2)

    def common_mode(self, time: float) -> float:
        """Return the mean mode, invariant under this symmetric coupling."""
        x1, x2 = self.state(time)
        return 0.5 * (x1 + x2)
