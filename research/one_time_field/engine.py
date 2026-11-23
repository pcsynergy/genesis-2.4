"""Shared-topology engine composing scalar, phase, and tensor state models.

The engine keeps each domain's governing equation intact. Two optional,
explicit cross-domain terms are provided as exploratory couplings:
  * global scalar mean -> uniform phase-frequency offset
  * phase coherence -> uniform scalar source

The gains carry whatever units make each user-defined mapping consistent.
They are modeling parameters, not measured physical constants.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any

from .harmonic import PhaseOscillatorNetwork
from .network import GraphFieldNetwork
from .tensor import TensorFieldNetwork


@dataclass
class DimensionalFieldEngine:
    """Advance heterogeneous field states on one shared weighted graph.

    All present submodels must use exactly the same adjacency matrix. At each
    step, cross-domain signals are computed from the pre-step state, then all
    submodels advance once. This is a simultaneous explicit-Euler update.
    """

    scalar: GraphFieldNetwork | None = None
    harmonic: PhaseOscillatorNetwork | None = None
    tensor: TensorFieldNetwork | None = None
    scalar_to_phase_gain: float = 0.0
    coherence_to_scalar_gain: float = 0.0

    def __post_init__(self) -> None:
        models = [m for m in (self.scalar, self.harmonic, self.tensor) if m is not None]
        if not models:
            raise ValueError("at least one field model is required")
        reference = models[0].adjacency
        if any(model.adjacency != reference for model in models[1:]):
            raise ValueError("all field models must share the same adjacency matrix")
        for name, value in (
            ("scalar_to_phase_gain", self.scalar_to_phase_gain),
            ("coherence_to_scalar_gain", self.coherence_to_scalar_gain),
        ):
            if not isfinite(value):
                raise ValueError(f"{name} must be finite")
        self.scalar_to_phase_gain = float(self.scalar_to_phase_gain)
        self.coherence_to_scalar_gain = float(self.coherence_to_scalar_gain)
        if self.scalar_to_phase_gain and (self.scalar is None or self.harmonic is None):
            raise ValueError("scalar_to_phase_gain requires scalar and harmonic models")
        if self.coherence_to_scalar_gain and (self.scalar is None or self.harmonic is None):
            raise ValueError("coherence_to_scalar_gain requires scalar and harmonic models")

    @property
    def node_count(self) -> int:
        model = self.scalar or self.harmonic or self.tensor
        return model.node_count

    def snapshot(self) -> dict[str, Any]:
        """Return a detached snapshot of all present domain states."""
        result: dict[str, Any] = {}
        if self.scalar is not None:
            result["scalar"] = list(self.scalar.state)
        if self.harmonic is not None:
            result["harmonic"] = list(self.harmonic.phases)
        if self.tensor is not None:
            result["tensor"] = [list(row) for row in self.tensor.state]
        return result

    def step(
        self, dt: float, scalar_external_source: list[float] | None = None
    ) -> dict[str, Any]:
        """Advance all domains; optional scalar forcing is additive to coherence coupling."""
        if not isfinite(dt) or dt <= 0.0:
            raise ValueError("dt must be finite and positive")

        scalar_mean = self.scalar.mean_state() if self.scalar is not None else 0.0
        coherence = self.harmonic.order_parameter() if self.harmonic is not None else 0.0

        # Each coupling is a declared mapping between different state domains.
        if scalar_external_source is not None:
            scalar_external_source = [float(v) for v in scalar_external_source]
            if len(scalar_external_source) != self.node_count or not all(isfinite(v) for v in scalar_external_source):
                raise ValueError("scalar_external_source must contain one finite value per node")
        if self.scalar is not None:
            scalar_source = [self.coherence_to_scalar_gain * coherence] * self.node_count
            if scalar_external_source is not None:
                scalar_source = [a + b for a, b in zip(scalar_source, scalar_external_source)]
            self.scalar.step(dt, source=scalar_source)

        if self.harmonic is not None:
            base_frequencies = list(self.harmonic.natural_frequencies)
            offset = self.scalar_to_phase_gain * scalar_mean
            self.harmonic.natural_frequencies = [w + offset for w in base_frequencies]
            try:
                self.harmonic.step(dt)
            finally:
                self.harmonic.natural_frequencies = base_frequencies

        if self.tensor is not None:
            self.tensor.step(dt)

        return self.snapshot()

    def run(self, steps: int, dt: float) -> list[dict[str, Any]]:
        """Return the initial snapshot and each subsequent coupled state."""
        if not isinstance(steps, int) or steps < 0:
            raise ValueError("steps must be a nonnegative integer")
        history = [self.snapshot()]
        for _ in range(steps):
            history.append(self.step(dt))
        return history
