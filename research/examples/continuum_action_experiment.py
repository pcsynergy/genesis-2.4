"""Run Experiment 7: continuum-field refinement and clock coupling."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.continuum_action import refinement_experiment


def main():
    rows, reference = refinement_experiment()
    print("Experiment 7: periodic continuum-field refinement")
    print("reference_grid", reference["nodes"], "dt", f'{reference["dt"]:.8g}')
    print("nodes,dt,field_rms_error,clock_error,energy_drift")
    for row in rows:
        print("{nodes},{dt:.8g},{field_rms_error:.8g},{clock_error:.8g},{energy_drift:.8g}".format(**row))


if __name__ == "__main__":
    main()
