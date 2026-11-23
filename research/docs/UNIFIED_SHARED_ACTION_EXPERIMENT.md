# Experiment 6 — Unified shared field action

Author: Pablo Salvador Cardenas  
Date: 2026-11-23

## Aim
Place scalar, phase, tensor-array, and dynamical-clock degrees of freedom in
one autonomous finite-dimensional action. The clock couples to bounded
observables from all three field domains.

## Action and metric
For q=(x_i, theta_i, T_ia) and clock coordinate Tc, the selected constant,
positive, block-diagonal kinetic metric gives

L = 1/2 qdot^T M qdot + 1/2 Ic Tcdot^2 - U(q,Tc),
U = V(q) + 1/2 kappa Tc^2 - g Tc C(q).

The scalar, phase, and tensor inertias are the block entries of M. This is a
common configuration-space metric, not a general spacetime metric.

The bounded clock observable is C=Cs+Cphase+Ctensor, where

Cs = ws/2 sum_i x_i^2/(1+x_i^2)
Cphase = wp/W sum_{i<j} Aij [1-cos(theta_i-theta_j)]
Ctensor = wt/2 sum_i ||Ti||^2/(1+||Ti||^2),

and W=sum_{i<j} Aij. If there are no phase edges, Cphase=0. The weights are
dimensionless normalization choices.

## Equations
M qddot = -grad(V) + g Tc grad(C)
Ic Tcddot = -kappa Tc + g C

The canonical Hamiltonian H=K+U is integrated by velocity-Verlet.

## Symmetry and Noether charge
The full action is invariant under a uniform phase shift
theta_i -> theta_i + alpha because both V and Cphase depend only on phase
differences. The corresponding conserved canonical charge is
Pphase = sum_i p_phase_i, with dPphase/dt=0. This is a Noether result for
this finite-dimensional model, not a claim about physical angular momentum.
No tensor gauge symmetry or spacetime diffeomorphism symmetry is asserted.

## Controlled limits and comparisons
At g=0, the clock oscillator separates and the field subsystem follows the
existing HamiltonianFieldSystem with the same V, inertias, and initial data.
Keeping only phases with a graph cosine potential gives inertial coupled
phase oscillators. Keeping only a scalar field with quadratic mass and graph
gradient terms gives a finite-graph quadratic scalar-field model. These are
structural reductions, not continuum-limit derivations.

## Validation and limitations
Tests cover bounded energy drift, zero-coupling recovery, global phase-shift
invariance, phase-momentum conservation, and all-domain clock coupling.
All variables are dimensionless absent physical scales. Tensor states are
component arrays, not geometric tensors with transformation laws. The metric
is constant and block diagonal; the graph is finite. No Lorentz covariance,
gauge completion, quantization, empirical fit, or physical validation is
claimed. Passing tests validates implementation against the selected
equations only.
