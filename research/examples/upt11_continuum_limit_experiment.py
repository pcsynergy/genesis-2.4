"""Run UPT-11 continuum-limit and observable refinement study."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.upt11_continuum_limit import continuum_refinement


def main():
    rows, reference = continuum_refinement()
    print("UPT-11: periodic relational-memory continuum limit")
    print("reference:", reference)
    print("nodes,dx,field_rms_error,mean_error,memory_error,energy,steps")
    for row in rows:
        print("{nodes},{dx:.8g},{field_rms_error:.8g},{mean_error:.8g},"
              "{memory_error:.8g},{energy:.10g},{steps}".format(**row))
    print("Interpretation: numerical refinement of a specified continuum model; "
          "not empirical validation or a distinctive physical prediction.")


if __name__ == "__main__":
    main()
