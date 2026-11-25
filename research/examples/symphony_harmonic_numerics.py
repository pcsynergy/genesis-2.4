"""Milestone F: integrator comparison, timestep refinement, and stability probes."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.symphony_numerics import integrate, order_parameter, phase_error

N = 8
PHASES = [0.0, 0.3, 0.9, 1.4, 2.0, 3.1, 4.2, 5.4]
FREQS = [1.0 + 0.025 * (i - (N-1)/2) for i in range(N)]
ADJ = [[0.0 if i == j else 1.0 for j in range(N)] for i in range(N)]
K = 1.2
T_FINAL = 20.0


def main():
    print("method,dt,steps,final_R,phase_error_vs_rk4_fine")
    reference = integrate(PHASES, ADJ, FREQS, K, 0.00125, 16000, "rk4")
    for method in ("euler", "rk4"):
        for dt in (0.02, 0.01, 0.005):
            final = integrate(PHASES, ADJ, FREQS, K, dt, round(T_FINAL/dt), method)
            print(f"{method},{dt:.5f},{round(T_FINAL/dt)},{order_parameter(final):.8f},{phase_error(reference, final):.8e}")

    print("\nstability_probe,initial_R,perturbed_R,relaxed_R")
    locked = [0.15] * N
    perturbed = [0.15 + 0.08 * (i - (N-1)/2) for i in range(N)]
    start_r = order_parameter(perturbed)
    relaxed = integrate(perturbed, ADJ, [1.0]*N, 1.0, 0.005, 4000, "rk4")
    print(f"complete_equal_frequency,{start_r:.8f},{order_parameter(perturbed):.8f},{order_parameter(relaxed):.8f}")


if __name__ == "__main__":
    main()
