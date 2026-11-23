"""Run Experiment 14 and print numerical diagnostics."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from research.one_time_field.cosmological_evolution import evolve_cosmology
from research.one_time_field.lorentz_covariant import CovariantParameters

if __name__ == "__main__":
    params = CovariantParameters(field_mass=0.7, clock_kinetic=1.0,
                                 clock_mass_squared=0.5, coupling=0.02)
    rows = evolve_cosmology(params, duration=2.0, steps=2000)
    final = rows[-1]
    max_constraint = max(abs(row["friedmann_residual"]) for row in rows)
    print("Experiment 14: coupled scalar-clock FLRW evolution")
    print(f"Samples: {len(rows)}")
    print(f"Final time: {final['time']:.6f}")
    print(f"Final scale factor: {final['scale_factor']:.12g}")
    print(f"Final Hubble parameter: {final['hubble']:.12g}")
    print(f"Final phi, T: {final['phi']:.12g}, {final['clock']:.12g}")
    print(f"Final rho, p: {final['energy_density']:.12g}, {final['pressure']:.12g}")
    print(f"Maximum absolute Friedmann residual: {max_constraint:.6e}")
