"""Run Experiment 4: feedback convergence and strength sweep."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.feedback_convergence import main

if __name__ == "__main__":
    main()
