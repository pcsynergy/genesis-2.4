"""Run the UPT-7 finite configuration-space experiment."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.upt7_configuration import UPTConfigurationEnsemble

CYCLE4 = (
    (0, 1, 0, 1),
    (1, 0, 1, 0),
    (0, 1, 0, 1),
    (1, 0, 1, 0),
)


def main():
    print("UPT-7: Potential, Field Interaction, and Observable Emergence")
    print("Finite model: four binary degrees of freedom on a periodic cycle")
    print("Admissibility constraint: exactly two active components")
    for coupling in (0.0, 0.5, 1.0, 2.0):
        model = UPTConfigurationEnsemble(
            CYCLE4, active_count=2, coupling=coupling, beta=1.0
        )
        result = model.observable_summary()
        print(
            f"J={coupling:.1f} states={int(result['admissible_state_count'])} "
            f"Z={result['partition_function']:.8f} "
            f"E[cut]={result['expected_cut']:.8f} "
            f"E[coherence]={result['expected_coherence']:.8f}"
        )
    print("Interpretation: relational coupling changes the distribution over")
    print("admissible configurations; this is a toy-model prediction, not")
    print("a new empirical prediction about fundamental physics.")


if __name__ == "__main__":
    main()
