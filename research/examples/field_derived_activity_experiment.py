"""Experiment 1: derive a candidate clock rate from live field derivatives.

All values are dimensionless illustrative model outputs, not measured physics.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from one_time_field.engine import DimensionalFieldEngine
from one_time_field.field_activity import FieldActivity
from one_time_field.harmonic import PhaseOscillatorNetwork
from one_time_field.network import GraphFieldNetwork
from one_time_field.temporal_models import RelationalClock
from one_time_field.tensor import TensorFieldNetwork

ADJACENCY = [
    [0.0, 1.0, 0.0],
    [1.0, 0.0, 1.0],
    [0.0, 1.0, 0.0],
]


def make_engine():
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


def main():
    engine = make_engine()
    clock = RelationalClock()
    dt, steps, gain = 0.01, 100, 0.25
    print("step,lambda,scalar_activity,phase_activity,tensor_activity,total_activity,clock_rate,tau")
    for step in range(steps + 1):
        activity = FieldActivity.from_engine(engine)
        rate = activity.relational_rate(gain=gain)
        if step % 10 == 0:
            print(
                f"{step},{step*dt:.4f},{activity.scalar:.10f},"
                f"{activity.phase:.10f},{activity.tensor:.10f},"
                f"{activity.total:.10f},{rate:.10f},{clock.reading:.10f}"
            )
        if step < steps:
            clock.advance(dt, rate)
            engine.step(dt)


if __name__ == "__main__":
    main()
