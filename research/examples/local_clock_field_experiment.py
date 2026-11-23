"""Run Experiment 8: a spatially local clock field."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from one_time_field.local_clock_field import refinement_experiment


def main():
    rows,ref=refinement_experiment()
    print("Experiment 8: local clock-field spatial refinement")
    print("reference_grid",ref["nodes"],"dt",f'{ref["dt"]:.8g}')
    print("nodes,dt,field_rms_error,clock_rms_error,energy_drift")
    for row in rows:
        print("{nodes},{dt:.8g},{field_rms_error:.8g},{clock_rms_error:.8g},{energy_drift:.8g}".format(**row))


if __name__=="__main__":
    main()
