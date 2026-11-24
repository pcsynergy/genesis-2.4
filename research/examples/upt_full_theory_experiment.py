"""Run the integrated Unified Potential Theory reference model."""
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from one_time_field.upt_full_theory import run_full_theory


def main():
    result = run_full_theory()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
