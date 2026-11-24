"""Run UPT-9 reversible-memory and thermodynamic-consistency experiment."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.upt9_memory_dynamics import UPTMemoryDynamics

CYCLE4 = ((0,1,0,1),(1,0,1,0),(0,1,0,1),(1,0,1,0))


def main():
    print("UPT-9: Reversibility, Memory, and Thermodynamic Consistency")
    for strength in (0.0, 0.5, 1.2, 2.0):
        model = UPTMemoryDynamics(CYCLE4, coupling=0.7, memory_strength=strength)
        q = model.generator()
        pi = model.stationary_distribution()
        print(f"kappa={strength:.1f} states={len(model.states)} "
              f"detailed_balance_residual={model.detailed_balance_residual():.3e} "
              f"stationary_norm={sum(pi):.12f} "
              f"max_exit_rate={max(-q[i][i] for i in range(len(q))):.6f}")
    model = UPTMemoryDynamics(CYCLE4, coupling=0.7, memory_strength=1.2)
    initial = [0.0]*len(model.states)
    initial[0] = 1.0
    evolved = model.evolve_uniformized(initial, 1.0, 100)
    print(f"evolved_probability_norm={sum(evolved):.12f}")
    print(f"minimum_probability={min(evolved):.6e}")
    print("Finite-model findings only; no physical validation is claimed.")


if __name__ == "__main__":
    main()
