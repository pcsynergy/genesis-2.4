"""Demonstrate the shared variational potential prototype."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from one_time_field import VariationalFieldSystem


def main() -> None:
    model = VariationalFieldSystem(
        adjacency=[[0.0, 1.0], [1.0, 0.0]],
        scalar=[0.2, 1.0],
        phases=[0.1, 1.2],
        tensor=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        scalar_gradient=0.8,
        phase_gradient=0.6,
        tensor_gradient=0.5,
        scalar_phase_coupling=0.25,
        tensor_phase_coupling=0.2,
    )
    print("step,potential")
    for step in range(11):
        print(f"{step},{model.potential():.8f}")
        if step < 10:
            model.step(0.001)


if __name__ == "__main__":
    main()
