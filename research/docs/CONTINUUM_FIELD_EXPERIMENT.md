# Experiment 7 — Continuum-field and clock-coupling refinement

**Author:** Pablo Salvador Cardenas  
**Research program:** One Time Field Theory (OTFT), GENESIS 2.4 research layer

## Question

Can the finite-dimensional clock–field interaction be implemented as a spatially extended field model, and does its numerical solution behave consistently under grid refinement?

This experiment is a controlled mathematical extension of Experiment 6. It does not assume Lorentz covariance or claim that the clock coordinate is physical time.

## Continuum ansatz

On a periodic one-dimensional domain of length (L), consider a real scalar field φ(x,t) and one autonomous clock coordinate (T(t)):

[
S=int dtleft{int_0^L dxleft[
rac12(partial_tphi)^2-rac12c^2(partial_xphi)^2
-rac12m^2phi^2ight]
+rac12 Idot T^2-rac12kappa T^2+gT C[phi]ight},
]

[
C[phi]=int_0^L dx,rac12rac{phi^2}{1+phi^2}.
]

The Euler–Lagrange equations are

[
partial_t^2phi=c^2partial_x^2phi-m^2phi+
gTrac{phi}{(1+phi^2)^2},
qquad
Iddot T=-kappa T+gC[phi].
]

The conserved autonomous energy is

[
E=int_0^L dxleft[
rac12phi_t^2+rac12c^2phi_x^2+rac12m^2phi^2
ight]+rac12 Idot T^2+rac12kappa T^2-gTC[phi].
]

The implemented discretization uses a periodic centered second-difference Laplacian and velocity-Verlet time stepping. Grid spacing is Δx=L/N and the timestep is scaled with Δx to respect a conservative wave-equation CFL condition.

## Protocol

- Smooth periodic initial field and velocity profiles are held fixed as the grid is refined.
- Run (N=32,64,128,256) to a common final parameter time.
- Compare each coarser field with periodic linear interpolation of the (N=256) reference.
- Record RMS field difference, clock-coordinate difference, and absolute energy drift.
- Unit tests check bounded energy error, the uncoupled harmonic-clock limit, input validation, and finite refinement outputs.

## Interpretation

A decreasing refinement error supports numerical consistency of this chosen finite-difference scheme for this chosen ansatz. Small energy drift supports the implementation of the autonomous discretized dynamics. Neither result establishes that OTFT is a physical theory, that (T) is operational time, or that the interaction occurs in nature.

## Scope and limitations

This is a classical, dimensionless, one-dimensional periodic scalar-field toy model with one global clock degree of freedom. It is not a complete relativistic field theory: no spacetime metric dynamics, Lorentz-covariant clock field, gauge completion, quantization, renormalization, empirical parameter fit, or observational test is supplied. The bounded observable is a modeling choice. A future step would need a local clock field (T(x,t)), a covariant action with clearly defined transformation properties, dimensional calibration, and independent observable predictions before physical interpretation is warranted.

## Reproduction

`python -m unittest discover -s research/tests -v`

`python research/examples/continuum_action_experiment.py`
