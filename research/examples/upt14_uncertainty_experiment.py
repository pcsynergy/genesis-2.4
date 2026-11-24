"""UPT-14: noisy memory-relaxation inference demonstration."""
from pathlib import Path
import math
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.upt14_uncertainty import (
    bootstrap_null_test, bootstrap_rate_interval, fit_relaxation_rate,
    simulate_observations,
)


def main():
    times = [i * 0.12 for i in range(36)]
    mean = [0.25 + 0.18 * math.sin(i * 0.37) for i in range(36)]
    true_rate, sigma = 0.75, 0.015
    observed = simulate_observations(times, mean, 0.72, true_rate, sigma, seed=14014)
    print("UPT-14: noise, uncertainty, and statistical significance")
    print("known synthetic rate:", true_rate, "assumed sigma:", sigma)
    print("fit:", fit_relaxation_rate(times, mean, observed, sigma, max_rate=3.0))
    print("interval:", bootstrap_rate_interval(times, mean, observed, sigma,
          max_rate=3.0, replicates=200, seed=14015))
    print("null test:", bootstrap_null_test(times, mean, observed, sigma,
          max_rate=3.0, replicates=499, seed=14016))
    print("Synthetic outputs validate this workflow only, not a physical theory.")


if __name__ == "__main__":
    main()
