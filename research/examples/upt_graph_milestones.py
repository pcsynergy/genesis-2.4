"""Run UPT-4 graph admissibility and UPT-5 observable comparison."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field import GraphFieldNetwork


def disagreement(values):
    mean = sum(values) / len(values)
    return sum((value - mean) ** 2 for value in values)


def main():
    print("UPT-4: graph topology and component-wise collective modes")
    path = GraphFieldNetwork(
        [[0, 1, 0], [1, 0, 1], [0, 1, 0]], [0.0, 2.0, 7.0], coupling=1.0
    )
    path.run(5000, 0.01)
    print("connected path final states:", [round(x, 10) for x in path.state])
    print("connected path mean:", round(path.mean_state(), 10))

    disconnected = GraphFieldNetwork(
        [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
        [0.0, 2.0, 4.0, 10.0], coupling=1.0,
    )
    disconnected.run(3000, 0.01)
    print("disconnected final states:", [round(x, 10) for x in disconnected.state])
    print("expected component means: [1, 1] and [7, 7]")

    print("\\nUPT-5: coupled versus uncoupled observable")
    adjacency = [[0, 1], [1, 0]]
    initial = [0.0, 2.0]
    coupled = GraphFieldNetwork(adjacency, initial, coupling=0.5)
    uncoupled = GraphFieldNetwork(adjacency, initial, coupling=0.0)
    coupled.run(200, 0.01)
    uncoupled.run(200, 0.01)
    print("observable: disagreement D = sum_i (x_i - mean(x))^2")
    print("initial D:", disagreement(initial))
    print("coupled D:", disagreement(coupled.state))
    print("uncoupled D:", disagreement(uncoupled.state))
    print("coupled states:", [round(x, 10) for x in coupled.state])
    print("uncoupled states:", [round(x, 10) for x in uncoupled.state])


if __name__ == "__main__":
    main()
