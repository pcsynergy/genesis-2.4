"""Milestone H: compare coupled phase dynamics with an uncoupled null model."""
from pathlib import Path
import sys
from math import pi
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.symphony_numerics import integrate, order_parameter

N = 8
DT = 0.01
STEPS = 3000
FREQUENCIES = [1.0 + 0.03 * (i - 3.5) for i in range(N)]
INITIALS = [
    [0.0, 0.2, 0.8, 1.7, 2.1, 3.4, 4.8, 5.5],
    [0.1, 0.7, 1.4, 2.2, 3.0, 3.8, 4.7, 5.6],
    [0.0, 1.1, 2.4, 3.0, 3.9, 4.4, 5.2, 5.9],
    [0.3, 0.5, 1.8, 2.6, 3.1, 4.0, 4.9, 5.7],
]

def complete_graph(n):
    return [[0.0 if i == j else 1.0 for j in range(n)] for i in range(n)]

def run_case(coupling):
    adjacency = complete_graph(N)
    values = []
    for initial in INITIALS:
        final = integrate(initial, adjacency, FREQUENCIES, coupling, DT, STEPS, "rk4")
        values.append(order_parameter(final))
    return values

def main():
    null = run_case(0.0)
    coupled = run_case(1.0)
    print("model,start_1,start_2,start_3,start_4,mean_R")
    for name, values in (("uncoupled_K0", null), ("coupled_K1", coupled)):
        print(name + "," + ",".join(f"{v:.6f}" for v in values) + f",{sum(values)/len(values):.6f}")
    print(f"mean_difference_R={sum(coupled)/len(coupled)-sum(null)/len(null):.6f}")

if __name__ == "__main__":
    main()
