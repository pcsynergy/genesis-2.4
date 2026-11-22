"""Run with: python research/examples/two_node_demo.py"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from one_time_field import GraphFieldNetwork


def main() -> None:
    model = GraphFieldNetwork(
        adjacency=[[0.0, 1.0], [1.0, 0.0]],
        state=[1.0, -1.0],
        coupling=0.5,
        decay=0.0,
    )
    print("step,node_0,node_1,mean")
    for step in range(11):
        print(
            f"{step},{model.state[0]:.6f},"
            f"{model.state[1]:.6f},{model.mean_state():.6f}"
        )
        if step < 10:
            model.step(dt=0.05)


if __name__ == "__main__":
    main()
