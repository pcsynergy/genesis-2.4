"""Run the UPT-16 governing-principle compatibility demonstration."""
from one_time_field.upt16_unified_principle import classify_common_energy_compatibility


def main():
    result = classify_common_energy_compatibility(
        gradient=(2.0, -1.0),
        mobility=((1.0, 0.0), (0.0, 1.0)),
        structure=((0.0, 1.0), (-1.0, 0.0)),
    )
    print("UPT-16: gradient-flow / Hamiltonian compatibility")
    for key, value in result.items():
        print(f"{key}: {value}")
    print("Interpretation: distinct dynamics require a derived coupling or limiting relation.")


if __name__ == "__main__":
    main()
