"""Run UPT-12 dimensional scaling and observability comparison."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from one_time_field.upt12_observability import (
    DimensionfulParameters, PhysicalScales, compare_memory_coupling,
)


def main():
    scales = PhysicalScales(length=1.0, time=1.0, field=1.0, energy=1.0)
    params = DimensionfulParameters(1.0, 0.5, 0.2, 1.0, 0.8)
    print("UPT-12: dimensional scaling and observable comparison")
    print("dimensionless coefficients:", params.dimensionless(scales))
    result = compare_memory_coupling()
    print("coupled:", result["coupled"])
    print("uncoupled:", result["uncoupled"])
    print("coupled-minus-uncoupled:", result["difference"])
    print("Interpretation: model-level sensitivity only. Physical inference requires")
    print("a declared measurement map, calibrated units, uncertainties and data.")


if __name__ == "__main__":
    main()
