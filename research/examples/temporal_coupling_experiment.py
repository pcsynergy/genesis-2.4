"""Run Experiment 3: explicit field-clock feedback."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.temporal_coupling import main

if __name__ == "__main__":
    main()
