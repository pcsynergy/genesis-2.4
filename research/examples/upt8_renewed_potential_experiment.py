"""Run the UPT-8 renewed-potential finite-network experiment."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.upt8_renewed_potential import UPTAdaptivePotentialSpace

CYCLE4 = (
    (0, 1, 0, 1),
    (1, 0, 1, 0),
    (0, 1, 0, 1),
    (1, 0, 1, 0),
)


def main():
    model = UPTAdaptivePotentialSpace(
        CYCLE4, initial_active_count=2, activation_threshold=1.0,
        coupling=1.0, beta=1.0,
    )
    history = model.domain_history(8)
    print("UPT-8: Renewed Potential and Adaptive Admissibility")
    print("Rule: admit q_i=0 -> 1 when weighted active-neighbor support >= 1")
    print("Domain expansion is monotone; probabilities are recomputed on each domain")
    print("round  states  expected_coherence")
    for index, domain in enumerate(history):
        coherence = model.expected_coherence(domain)
        print(f"{index:5d}  {len(domain):6d}  {coherence:.8f}")
    print("closure reached:", model.renewal_step(history[-1]) == history[-1])
    print("Interpretation: a finite model changes its admissible domain;")
    print("this is not evidence of physical or ontological creation.")


if __name__ == "__main__":
    main()
