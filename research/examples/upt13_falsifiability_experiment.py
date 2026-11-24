"""Run UPT-13 falsifiability and held-out model comparison."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from one_time_field.upt13_falsifiability import compare_memory_relaxation


def synthetic_series(rate=0.8, count=41, dt=0.1):
    import math
    times = [i * dt for i in range(count)]
    mean_field = [0.2 + 0.15 * math.sin(i * 0.31) for i in range(count)]
    memory = [0.7]
    for i in range(count - 1):
        decay = math.exp(-rate * dt)
        memory.append(mean_field[i] + (memory[-1] - mean_field[i]) * decay)
    return times, mean_field, memory


def main():
    times, mean_field, memory = synthetic_series()
    result = compare_memory_relaxation(times, mean_field, memory, max_rate=3.0)
    print("UPT-13: falsifiability and held-out model comparison")
    for key, value in result.items():
        print(f"{key}: {value}")
    print("Synthetic data are used to verify recovery and model discrimination.")
    print("No empirical observations or physical parameter estimates are claimed.")


if __name__ == "__main__":
    main()
