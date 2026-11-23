"""Experiment 4: timestep convergence and feedback-strength sensitivity.

This is a numerical verification study of Experiment 3's explicitly
postulated one-step-delayed clock-to-field source. It is not a physical
measurement or evidence for a real clock-field interaction.
"""
from __future__ import annotations

from math import isfinite, sqrt

from one_time_field.temporal_coupling import make_engine, _scalar_total_source
from one_time_field.field_activity import FieldActivity


def _distance(a: dict, b: dict) -> float:
    terms = []
    for domain in a:
        if domain == "tensor":
            terms.extend(
                (x - y) ** 2
                for row_a, row_b in zip(a[domain], b[domain])
                for x, y in zip(row_a, row_b)
            )
        else:
            terms.extend((x - y) ** 2 for x, y in zip(a[domain], b[domain]))
    return sqrt(sum(terms))


def run_feedback_pair(
    dt: float, final_lambda: float = 5.0, feedback_gain: float = 0.05,
    clock_gain: float = 0.25, clock_baseline: float = 1.0,
) -> dict[str, float]:
    """Run control and feedback systems to a common final parameter time."""
    for name, value in (("dt", dt), ("final_lambda", final_lambda),
                        ("feedback_gain", feedback_gain), ("clock_gain", clock_gain),
                        ("clock_baseline", clock_baseline)):
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not isfinite(value):
            raise ValueError(f"{name} must be finite")
    if dt <= 0 or final_lambda < 0 or feedback_gain < 0 or clock_gain < 0 or clock_baseline <= 0:
        raise ValueError("dt and baseline must be positive; final time and gains nonnegative")
    ratio = final_lambda / dt
    steps = round(ratio)
    if abs(steps * dt - final_lambda) > 1e-10:
        raise ValueError("final_lambda must be an integer multiple of dt")

    control, coupled = make_engine(), make_engine()
    previous_rate = float(clock_baseline)
    for _ in range(steps):
        control_source = _scalar_total_source(control, 0.0)
        feedback = feedback_gain * (previous_rate - clock_baseline)
        coupled_source = _scalar_total_source(coupled, feedback)
        activity = FieldActivity.from_engine(coupled, scalar_source=coupled_source)
        rate = activity.relational_rate(clock_gain, clock_baseline)
        control.step(dt)
        coupled.step(dt, scalar_external_source=[feedback] * coupled.node_count)
        previous_rate = rate

    # Evaluate diagnostics on the actual final states, not on the state
    # immediately before the final integration step.
    final_feedback = feedback_gain * (previous_rate - clock_baseline)
    final_source = _scalar_total_source(coupled, final_feedback)
    final_activity = FieldActivity.from_engine(coupled, scalar_source=final_source)
    final_rate = final_activity.relational_rate(clock_gain, clock_baseline)
    distance = _distance(control.snapshot(), coupled.snapshot())
    result = {
        "dt": float(dt), "steps": float(steps), "final_lambda": float(final_lambda),
        "feedback_gain": float(feedback_gain), "state_distance": distance,
        "final_feedback_source": final_feedback,
        "final_clock_rate": final_rate,
    }
    if not all(isfinite(v) for v in result.values()):
        raise RuntimeError("non-finite result in feedback convergence study")
    return result


def run_convergence_study(
    step_sizes: tuple[float, ...] = (0.02, 0.01, 0.005, 0.0025, 0.00125),
    final_lambda: float = 5.0, feedback_gain: float = 0.05,
) -> list[dict[str, float]]:
    """Compare feedback-induced separation across successively finer steps."""
    if len(step_sizes) < 2 or any(b >= a for a, b in zip(step_sizes, step_sizes[1:])):
        raise ValueError("step_sizes must contain at least two strictly decreasing values")
    return [
        run_feedback_pair(dt, final_lambda, feedback_gain)
        for dt in step_sizes
    ]


def run_strength_sweep(
    gains: tuple[float, ...] = (0.0, 0.01, 0.025, 0.05, 0.1),
    dt: float = 0.0025, final_lambda: float = 5.0,
) -> list[dict[str, float]]:
    """Vary feedback amplitude at a fixed timestep and final parameter time."""
    if not gains or any(g < 0 or not isfinite(g) for g in gains):
        raise ValueError("gains must be a nonempty sequence of finite nonnegative values")
    return [run_feedback_pair(dt, final_lambda, gain) for gain in gains]


def main() -> None:
    print("CONVERGENCE: dt,steps,state_distance,final_feedback_source,final_clock_rate")
    for row in run_convergence_study():
        print(",".join(f"{row[k]:.12g}" for k in
                       ("dt", "steps", "state_distance", "final_feedback_source", "final_clock_rate")))
    print("STRENGTH: feedback_gain,dt,state_distance,final_feedback_source,final_clock_rate")
    for row in run_strength_sweep():
        print(",".join(f"{row[k]:.12g}" for k in
                       ("feedback_gain", "dt", "state_distance", "final_feedback_source", "final_clock_rate")))


if __name__ == "__main__":
    main()
