# Symphony 5.5 / UPT — Milestone F: Numerical stability and convergence

**Status:** implemented; CI validation pending  
**Runner:** `research/examples/symphony_harmonic_numerics.py`  
**Tests:** `research/tests/test_symphony_numerics.py`

## Objective

Check whether the phase-network outcomes depend strongly on the numerical time step and compare first-order explicit Euler integration with fourth-order Runge–Kutta (RK4). Include a simple perturbation-relaxation probe for a complete graph with identical natural frequencies.

## Numerical protocol

The experiment integrates the same normalized Kuramoto-style phase equation using both methods. It compares (Delta t=0.02,0.01,0.005) over a fixed interval (T=20). A fine RK4 reference uses (Delta t=0.00125). Phase-vector errors are computed after removing the arbitrary common phase by anchoring each vector to its first oscillator; this avoids treating a uniform rotation as a physical discrepancy.

The stability probe begins with a small linear phase perturbation around a common phase for an eight-node complete graph with equal frequencies. The network is integrated using RK4 at (Delta t=0.005) for 4,000 steps. The order parameter before and after relaxation is reported.

## What the tests establish

The tests require:
- decreasing phase error as RK4 time steps are refined;
- RK4 to outperform Euler at the same tested step size against the fine reference;
- increased global coherence as a small perturbation relaxes in the equal-frequency complete graph;
- explicit rejection of invalid integrator settings.

These are internal numerical checks for this finite oscillator system. They do not establish general stability for every topology, parameter choice, or initial condition.

## Interpretation

For a smooth ODE, RK4 has formal global error order four while explicit Euler has global error order one under the usual regularity and stability assumptions. The implemented tests check that the chosen finite experiment behaves consistently with this expectation; they do not prove a universal error bound.

The equal-frequency complete-graph probe is a local relaxation example. It is not a proof that every synchronized or twisted state is stable. A full stability classification would require linearizing around each stationary or uniformly rotating solution and analyzing the resulting Jacobian spectrum.

## Scientific boundary

This is numerical verification of a phenomenological phase-oscillator model. It does not test spacetime curvature, gravitational dynamics, quantum fields, or empirical predictions of UPT / One Time Field Theory. The result should be described as numerical consistency and model-level stability evidence only.
