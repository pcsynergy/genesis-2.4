"""Experiment 2: compare external and field-derived relational time.

The same coupled-field trajectory is parameterized by lambda and by tau,
where d tau / d lambda = b + eta*A(state). A positive reparameterization
changes the clock label, not the geometric path through state space.
"""
from __future__ import annotations

from copy import deepcopy
from math import sqrt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from one_time_field.engine import DimensionalFieldEngine
from one_time_field.field_activity import FieldActivity
from one_time_field.harmonic import PhaseOscillatorNetwork
from one_time_field.network import GraphFieldNetwork
from one_time_field.tensor import TensorFieldNetwork


ADJACENCY = [
    [0.0, 1.0, 0.0],
    [1.0, 0.0, 1.0],
    [0.0, 1.0, 0.0],
]


def make_engine() -> DimensionalFieldEngine:
    """Create the common initial state used by both clock descriptions."""
    return DimensionalFieldEngine(
        scalar=GraphFieldNetwork(
            ADJACENCY, [0.9, -0.35, 0.55], coupling=0.4, decay=0.05
        ),
        harmonic=PhaseOscillatorNetwork(
            ADJACENCY, [0.15, 1.25, 2.35], [0.7, 1.0, 1.3], coupling=0.6
        ),
        tensor=TensorFieldNetwork(
            ADJACENCY, [[0.8, -0.2], [-0.1, 0.65], [0.45, 0.9]],
            (2,), coupling=0.3, decay=0.02
        ),
        scalar_to_phase_gain=0.1,
        coherence_to_scalar_gain=0.05,
    )


def _observables(engine: DimensionalFieldEngine) -> tuple[float, float, float]:
    scalar_mean = engine.scalar.mean_state() if engine.scalar is not None else 0.0
    coherence = engine.harmonic.order_parameter() if engine.harmonic is not None else 0.0
    tensor_rms = 0.0
    if engine.tensor is not None:
        values = [v for row in engine.tensor.state for v in row]
        tensor_rms = sqrt(sum(v * v for v in values) / len(values))
    return scalar_mean, coherence, tensor_rms


def run_comparison(
    steps: int = 100,
    d_lambda: float = 0.01,
    gain: float = 0.25,
    baseline: float = 1.0,
) -> list[dict[str, float]]:
    """Run the paired comparison and return synchronized diagnostics.

    The relational branch integrates dPsi/dtau = F(Psi)/(d tau/d lambda).
    For each step d_tau = rate*d_lambda, so its state increment is
    d_tau*F/rate = d_lambda*F, matching the external-time branch.
    """
    if not isinstance(steps, int) or isinstance(steps, bool) or steps < 0:
        raise ValueError("steps must be a nonnegative integer")
    if not isinstance(d_lambda, (int, float)) or d_lambda <= 0:
        raise ValueError("d_lambda must be positive")
    if not isinstance(gain, (int, float)) or gain < 0:
        raise ValueError("gain must be nonnegative")
    if not isinstance(baseline, (int, float)) or baseline <= 0:
        raise ValueError("baseline must be positive")

    external = make_engine()
    relational = deepcopy(external)
    tau = 0.0
    rows: list[dict[str, float]] = []

    for step in range(steps + 1):
        activity = FieldActivity.from_engine(external)
        rate = activity.relational_rate(gain=float(gain), baseline=float(baseline))
        state_a = external.snapshot()
        state_b = relational.snapshot()
        max_state_error = 0.0
        for domain in state_a:
            if domain == "tensor":
                errors = [
                    abs(a - b)
                    for row_a, row_b in zip(state_a[domain], state_b[domain])
                    for a, b in zip(row_a, row_b)
                ]
            else:
                errors = [
                    abs(a - b)
                    for a, b in zip(state_a[domain], state_b[domain])
                ]
            max_state_error = max(max_state_error, max(errors, default=0.0))
        scalar_mean, coherence, tensor_rms = _observables(external)
        rows.append({
            "step": float(step),
            "lambda": step * float(d_lambda),
            "tau": tau,
            "clock_rate": rate,
            "activity": activity.total,
            "scalar_mean": scalar_mean,
            "phase_coherence": coherence,
            "tensor_rms": tensor_rms,
            "max_state_error": max_state_error,
        })
        if step == steps:
            break

        d_tau = rate * float(d_lambda)
        # External-clock form: dPsi/dlambda = F(Psi).
        external.step(float(d_lambda))
        # Relational-clock form: dPsi/dtau = F(Psi)/rate.
        # Euler increment d_tau/rate is the same d_lambda.
        relational.step(d_tau / rate)
        tau += d_tau

    return rows


def main() -> None:
    rows = run_comparison()
    print(
        "step,lambda,tau,clock_rate,activity,scalar_mean,"
        "phase_coherence,tensor_rms,max_state_error"
    )
    for row in rows[::10]:
        print(",".join(
            f"{row[key]:.12g}"
            for key in (
                "step", "lambda", "tau", "clock_rate", "activity",
                "scalar_mean", "phase_coherence", "tensor_rms",
                "max_state_error",
            )
        ))
    if rows[-1]["max_state_error"] > 1e-12:
        raise RuntimeError("paired state trajectories diverged beyond tolerance")


if __name__ == "__main__":
    main()
