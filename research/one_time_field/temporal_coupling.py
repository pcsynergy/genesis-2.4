"""Experiment 3: explicit feedback from field-derived clock to field dynamics.

The scalar field receives a one-step-delayed source proportional to the
previous step's clock-rate excess. This is an explicit phenomenological
interaction, not a consequence of time reparameterization.
"""
from __future__ import annotations

from math import isfinite, sqrt
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
    """Create the shared initial three-domain system."""
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


def _scalar_total_source(engine: DimensionalFieldEngine, feedback: float) -> list[float]:
    coherence = engine.harmonic.order_parameter() if engine.harmonic is not None else 0.0
    source = engine.coherence_to_scalar_gain * coherence + feedback
    return [source] * engine.node_count


def _state_distance(a: dict, b: dict) -> float:
    differences = []
    for domain in a:
        if domain == "tensor":
            differences.extend(
                abs(x - y)
                for row_a, row_b in zip(a[domain], b[domain])
                for x, y in zip(row_a, row_b)
            )
        else:
            differences.extend(abs(x - y) for x, y in zip(a[domain], b[domain]))
    return sqrt(sum(value * value for value in differences))


def run_coupling_experiment(
    steps: int = 500,
    dt: float = 0.01,
    clock_gain: float = 0.25,
    clock_baseline: float = 1.0,
    feedback_gain: float = 0.05,
) -> list[dict[str, float]]:
    """Compare no clock feedback with explicit delayed clock-to-scalar forcing.

    The coupled equation adds
        d(phi_i)/d(lambda) = F_phi_i(Psi) + epsilon*(r_(n-1)-b)
    to the scalar field, uniformly across nodes. The lag makes the update
    explicit and avoids an implicit algebraic loop. All other equations and
    initial conditions are shared with the control system.
    """
    if not isinstance(steps, int) or isinstance(steps, bool) or steps < 0:
        raise ValueError("steps must be a nonnegative integer")
    for name, value, allow_zero in (
        ("dt", dt, False),
        ("clock_gain", clock_gain, True),
        ("clock_baseline", clock_baseline, False),
        ("feedback_gain", feedback_gain, True),
    ):
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not isfinite(value):
            raise ValueError(f"{name} must be finite")
        if value < 0 or (not allow_zero and value == 0):
            raise ValueError(f"{name} must be {'nonnegative' if allow_zero else 'positive'}")

    control = make_engine()
    coupled = make_engine()
    previous_clock_rate = float(clock_baseline)
    rows: list[dict[str, float]] = []

    for step in range(steps + 1):
        control_source = _scalar_total_source(control, 0.0)
        coupled_feedback = feedback_gain * (previous_clock_rate - clock_baseline)
        coupled_source = _scalar_total_source(coupled, coupled_feedback)

        control_activity = FieldActivity.from_engine(control, scalar_source=control_source)
        coupled_activity = FieldActivity.from_engine(coupled, scalar_source=coupled_source)
        control_rate = control_activity.relational_rate(clock_gain, clock_baseline)
        coupled_rate = coupled_activity.relational_rate(clock_gain, clock_baseline)

        distance = _state_distance(control.snapshot(), coupled.snapshot())
        rows.append({
            "step": float(step),
            "lambda": step * float(dt),
            "control_activity": control_activity.total,
            "coupled_activity": coupled_activity.total,
            "control_clock_rate": control_rate,
            "coupled_clock_rate": coupled_rate,
            "feedback_source": coupled_feedback,
            "state_distance": distance,
        })

        if step == steps:
            break
        control.step(float(dt))
        coupled.step(float(dt), scalar_external_source=[coupled_feedback] * coupled.node_count)
        previous_clock_rate = coupled_rate

    if not all(isfinite(value) for row in rows for value in row.values()):
        raise RuntimeError("non-finite value encountered during coupling experiment")
    return rows


def main() -> None:
    rows = run_coupling_experiment()
    print(
        "step,lambda,control_activity,coupled_activity,control_clock_rate,"
        "coupled_clock_rate,feedback_source,state_distance"
    )
    for row in rows[::50]:
        print(",".join(
            f"{row[key]:.12g}"
            for key in (
                "step", "lambda", "control_activity", "coupled_activity",
                "control_clock_rate", "coupled_clock_rate",
                "feedback_source", "state_distance",
            )
        ))
    print(f"final_state_distance={rows[-1]['state_distance']:.12g}")


if __name__ == "__main__":
    main()
