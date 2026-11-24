"""Run the UPT-10 finite-dimensional Onsager-flow demonstration."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.upt10_action_principle import UPTActionPrinciple


def main():
    model = UPTActionPrinciple(
        adjacency=((0, 1, 0, 0), (1, 0, 1, 0),
                   (0, 1, 0, 1), (0, 0, 1, 0)),
        relational_strength=0.8,
        memory_strength=0.6,
        bistable_strength=0.5,
        field_mobility=1.0,
        memory_mobility=0.7,
    )
    field, memory = (0.15, 0.75, 0.35, 0.9), 1.4
    print("UPT-10: Onsager gradient-flow prototype")
    print("initial field:", field, "memory:", memory)
    print("initial energy:", f"{model.energy(field, memory):.12f}")
    print("instantaneous dH/dt:", f"{model.energy_rate(field, memory):.12f}")
    print("predicted dissipation:", f"{model.dissipation_rate(field, memory):.12f}")
    for step in range(1, 101):
        field, memory, _ = model.step(field, memory, 0.05)
        if step in (1, 10, 25, 50, 100):
            print(f"step {step:3d}: H={model.energy(field, memory):.12f}, "
                  f"memory={memory:.8f}, field={tuple(round(v, 6) for v in field)}")
    print("final energy:", f"{model.energy(field, memory):.12f}")
    print("Interpretation: dissipative variational consistency, not physical validation.")


if __name__ == "__main__":
    main()
