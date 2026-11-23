"""Run the exact UPT-3 two-node relational-coupling demonstration."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.two_node_relational import TwoNodeRelationalModel


def main() -> None:
    model = TwoNodeRelationalModel((0.0, 2.0), coupling=0.3)
    print("UPT-3: two-node relational coupling")
    print("time    state_1      state_2      mean      difference")
    for time in (0.0, 0.5, 1.0, 2.0, 5.0, 10.0):
        x1, x2 = model.state(time)
        print(f"{time:4.1f}  {x1:11.6f}  {x2:11.6f}  "
              f"{model.common_mode(time):8.6f}  {model.consensus_error(time):11.6f}")
    print(f"initial relational energy: {model.relational_energy(0.0):.8f}")
    print(f"final relational energy:   {model.relational_energy(10.0):.8f}")


if __name__ == "__main__":
    main()
