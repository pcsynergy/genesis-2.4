"""Demonstrate three clocks responding to activity in a coupled field model."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.engine import DimensionalFieldEngine
from one_time_field.harmonic import PhaseOscillatorNetwork
from one_time_field.network import GraphFieldNetwork
from one_time_field.temporal import TemporalLayer
from one_time_field.tensor import TensorFieldNetwork


def main() -> None:
    graph = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    engine = DimensionalFieldEngine(
        scalar=GraphFieldNetwork(graph, [0.9, -0.35, 0.55], coupling=0.4),
        harmonic=PhaseOscillatorNetwork(graph, [0.15, 1.25, 2.35],
                                        [0.2, 0.0, -0.1], coupling=0.6),
        tensor=TensorFieldNetwork(graph, [[0.8, -0.2], [-0.1, 0.65],
                                          [0.45, 0.9]], (2,), coupling=0.3),
        temporal=TemporalLayer(relational_gain=0.15, observer_gain=0.08,
                               reference_activity=0.25),
    )
    print("step,parameter_time,relational_time,observer_time,event_activity")
    for step in range(101):
        if step:
            engine.step(0.01)
        clock = engine.temporal.snapshot()
        activity = (clock["accumulated_activity"] / clock["parameter_time"]
                    if clock["parameter_time"] else 0.0)
        print(f'{step},{clock["parameter_time"]:.6f},'
              f'{clock["relational_time"]:.6f},{clock["observer_time"]:.6f},'
              f'{activity:.6f}')


if __name__ == "__main__":
    main()
