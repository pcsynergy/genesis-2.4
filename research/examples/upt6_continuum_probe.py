"""Run the UPT-6 symmetry and continuum-equation probe."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.upt6_continuum import (
    diffusion_rate, massless_wave_acceleration, periodic_laplacian,
    shift_noether_charge, shift_symmetry_status,
)

def main():
    field = [0.0, 1.0, 0.0, -1.0, 0.5, 0.2]
    velocity = [0.2, -0.1, 0.4, 0.3, -0.2, 0.1]
    dx = 0.25
    lap = periodic_laplacian(field, dx)
    wave_acc = massless_wave_acceleration(field, dx, 1.0)
    diff_rate = diffusion_rate(field, dx, 1.0)
    print("UPT-6: Noether symmetry and continuum probe")
    print("periodic Laplacian sum:", sum(lap))
    print("massless wave acceleration sum:", sum(wave_acc))
    print("diffusion rate sum:", sum(diff_rate))
    print("shift charge:", shift_noether_charge(velocity, dx))
    print("constant-potential shift symmetry:", shift_symmetry_status(True))
    print("quadratic-potential shift symmetry:", shift_symmetry_status(False))
    print("Interpretation: the wave model is conservative; diffusion is dissipative.")
    print("Neither equation is a novel UPT prediction without a new physical mapping.")

if __name__ == "__main__":
    main()
