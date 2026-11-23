"""Run with: python research/examples/dimensional_engine_demo.py

Demonstrates shared graph topology and the two explicit exploratory
cross-domain couplings. The parameter values are illustrative, not physical.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from one_time_field import (
    DimensionalFieldEngine,
    GraphFieldNetwork,
    PhaseOscillatorNetwork,
    TensorFieldNetwork,
)


def main() -> None:
    graph = [[0.0, 1.0], [1.0, 0.0]]
    engine = DimensionalFieldEngine(
        scalar=GraphFieldNetwork(graph, [1.0, 0.0], coupling=0.2),
        harmonic=PhaseOscillatorNetwork(
            graph, [0.0, 0.8], [1.0, 1.05], coupling=0.4
        ),
        tensor=TensorFieldNetwork(
            graph, [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], (3,), coupling=0.1
        ),
        scalar_to_phase_gain=0.05,
        coherence_to_scalar_gain=0.02,
    )

    print("step,scalar,phase,tensor")
    for step in range(6):
        state = engine.snapshot()
        print(
            f"{step},"
            f"{[round(x, 5) for x in state['scalar']]},"
            f"{[round(x, 5) for x in state['harmonic']]},"
            f"{[[round(x, 5) for x in row] for row in state['tensor']]}"
        )
        if step < 5:
            engine.step(0.05)


if __name__ == "__main__":
    main()
