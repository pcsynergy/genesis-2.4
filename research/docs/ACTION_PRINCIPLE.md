# Action, Lagrangian, and Hamiltonian Formulations — Draft 0.1

## 1. Research question and scope

The current `VariationalFieldSystem` defines a dimensionless potential V and chooses first-order, mobility-weighted gradient flow. This note asks what changes if the same state coordinates are instead placed in a conservative action-based model.

The distinction is essential:
- A potential functional is a scalar function of state.
- An action is a time integral of a Lagrangian and determines equations through stationary action.
- A Hamiltonian is an energy function on phase space and generates canonical evolution.
- Gradient flow is dissipative and generally is not the same dynamics as an ordinary conservative Lagrangian system.

The existing code is not changed by this note. Equations below are candidate mathematical extensions, not claims about nature.

## 2. Common configuration space

Collect the present state coordinates into a configuration vector

    q = (x_1,...,x_N, theta_1,...,theta_N, T_11,...,T_Nd).

The tensor-array entries are treated here only as ordinary generalized coordinates. This does not make them geometric tensors. The phase coordinates are periodic, so their configuration space contains circles rather than unrestricted real lines. For calculations involving phase sums, a local unwrapped coordinate chart must be used and branch crossings handled explicitly.

Let V(q) be the shared dimensionless functional already implemented. Choose an energy scale E0 and define

    U(q) = E0 * V(q_bar),

where q_bar denotes the dimensionless coordinates. This interpretation is conditional on eventually assigning physical meaning and units to the coordinates and E0.

## 3. Formulation A — dissipative gradient flow

The existing model is

    dq/dtau = -Mmob * grad_q V(q),

where Mmob is a positive mobility matrix. In the current implementation it is block diagonal with scalar, phase, and tensor mobilities.

For a time-independent V and no external phase drive,

    dV/dtau = -(grad V)^T Mmob (grad V) <= 0.

This is a dissipative relaxation law. It has no inertial state variables and no general conservation of the potential. Its equilibria are stationary points of V, with stability depending on the Hessian and mobility.

A related physical formulation is an Onsager/Rayleigh dissipation principle. For a positive resistance matrix Z, define the Rayleigh dissipation function

    R(qdot) = 1/2 * qdot^T Z qdot.

A first-order overdamped evolution can be specified by minimizing the instantaneous dissipation-plus-energy rate, yielding

    Z qdot + grad_q U = 0.

This is the dimensional analogue of gradient flow with mobility Z^-1. It is a variational principle for dissipative dynamics, but it is not Hamilton's stationary-action principle.

## 4. Formulation B — conservative Lagrangian mechanics

Introduce a symmetric positive-definite generalized inertia matrix G(q), and define

    L(q,qdot) = 1/2 * qdot^T G(q) qdot - U(q).

The action over [t_a,t_b] is

    S[q] = integral_(t_a)^(t_b) L(q,qdot) dt.

Stationary action, with fixed endpoint variations, gives the Euler-Lagrange equations

    d/dt (partial L / partial qdot_a)
      - partial L / partial q_a = 0.

For constant G this reduces to

    G qddot + grad_q U = 0.

The model is conservative when L has no explicit time dependence and no dissipative forces. The conserved mechanical energy is

    H = 1/2 * qdot^T G qdot + U(q).

This is a genuinely different evolution from first-order gradient flow: it has velocities, inertia, and typically oscillates around stable minima rather than simply relaxing toward them.

For a coordinate-dependent G(q), the Euler-Lagrange equations include the corresponding geometric/inertial terms. They must not be omitted in an implementation.

## 5. Formulation C — Hamiltonian mechanics

For constant positive-definite G, define canonical momentum

    p = partial L / partial qdot = G qdot.

The Hamiltonian is the Legendre transform

    H(q,p) = 1/2 * p^T G^-1 p + U(q).

Hamilton's equations are

    qdot = partial H / partial p = G^-1 p
    pdot = -partial H / partial q = -grad_q U.

For an autonomous Hamiltonian, dH/dt = 0. Canonical phase-space evolution preserves symplectic structure and phase-space volume. These properties do not hold for the current overdamped gradient-flow model.

If G depends on q, the Hamiltonian remains defined by the Legendre transform when the transform is regular, but the explicit equations and kinetic term require the full q dependence.

## 6. Side-by-side comparison

| Property | Gradient flow | Lagrangian / Hamiltonian |
|---|---|---|
| State | q | q and qdot, or q and p |
| Typical order | First order | Second order |
| Dynamics | Dissipative relaxation | Conservative motion |
| Potential/energy | V decreases in undriven exact flow | Total H conserved if autonomous |
| Inertia | Absent | Present through G |
| Equilibrium behavior | Relaxation to stationary states | Oscillation or stable/unstable motion |
| Symmetry consequences | Derive directly from gradient equations | Noether theorem for continuous action symmetries |
| External drive | Can break monotonic V | Can make H time-dependent or add forces |

The shared V can be used in both models, but the equations of motion and physical interpretation are not interchangeable.

## 7. Symmetry and conservation in the conservative model

If U is invariant under a continuous transformation of q, the Lagrangian inherits that symmetry when the kinetic term is invariant too. Noether's theorem then supplies a conserved quantity for the conservative Euler-Lagrange dynamics.

Examples require care:
- A global phase shift is a symmetry of the current potential because it depends on phase differences. It gives a conserved canonical momentum conjugate to the common phase only if the kinetic metric and any other terms preserve that symmetry.
- A common scalar shift is a symmetry of the potential only when scalar_mass is zero. It yields a conserved momentum only if the kinetic sector also preserves the shift.
- Tensor-component shifts have the analogous condition when tensor_mass is zero, again requiring kinetic-sector invariance.

These are conditional predictions of a specified Lagrangian, not automatic consequences of the potential alone. The conserved Noether charge is generally a momentum, not simply the sum of coordinates.

## 8. Dissipation as a controlled extension

To compare conservative and dissipative behavior without conflating them, add a Rayleigh function

    R(qdot) = 1/2 * qdot^T Z qdot,  Z positive semidefinite.

The Lagrange-Rayleigh equations become

    d/dt (partial L / partial qdot)
      - partial L / partial q
      + partial R / partial qdot = 0.

For constant G and Z:

    G qddot + Z qdot + grad_q U = 0.

The energy balance is

    dH/dt = -qdot^T Z qdot <= 0

in the absence of external forcing. In the strongly overdamped limit, the inertial term becomes negligible and the dynamics approach

    Z qdot + grad_q U = 0.

This supplies a mathematically controlled bridge between conservative dynamics and the existing gradient-flow prototype. The limit must be studied, not assumed to hold for arbitrary parameters.

## 9. What must be specified before implementation

1. State meanings and units for x, theta, and each tensor-array component.
2. A positive-definite kinetic/inertia metric G, including whether it is diagonal, block-coupled, or state-dependent.
3. A physically justified energy scale E0 and potential U.
4. Boundary/initial conditions for both q and qdot (or p).
5. Whether dissipation Z is present and how its entries are measured or constrained.
6. The transformation group whose symmetries are intended to represent physical invariances.
7. A numerical integrator appropriate to the chosen system: symplectic methods for conservative Hamiltonian dynamics, and stable dissipative solvers for gradient/Rayleigh dynamics.
8. Limiting-case tests against established oscillator, diffusion, and field equations.

Without these choices, there is no unique action to derive from V. Many inequivalent kinetic metrics and dissipation laws can share the same potential.

## 10. Recommended staged implementation

**Stage 1 — finite-dimensional conservative reference.** Implement a separate `HamiltonianFieldSystem` with constant diagonal positive inertia, the existing V and analytic gradient, and canonical q,p stepping. Keep it separate from `VariationalFieldSystem`.

**Stage 2 — validation.** Test Hamilton's equations against finite differences, verify energy conservation under a symplectic integrator as the step is refined, and verify time-reversal behavior in the undamped system.

**Stage 3 — Rayleigh damping.** Add an explicitly declared positive-semidefinite damping matrix and verify the predicted energy dissipation.

**Stage 4 — field-theory generalization.** Only after state meanings, geometry, and units are defined, replace the finite graph coordinates with fields and spatial derivatives. Derive an action density, Euler-Lagrange field equations, and boundary conditions. Compare with established field theories in their tested regimes.

## 11. Interpretation boundary

The shared potential is a useful common mathematical object, but it does not uniquely determine dynamics. Gradient flow, conservative Lagrangian motion, Hamiltonian evolution, and Rayleigh-damped mechanics are distinct models built from additional assumptions.

The OTFT proposition **“All Fields Lead to One”** is therefore best treated as a research hypothesis motivating the search for a common state space and action. The present work establishes a framework for asking that question; it does not yet establish a unique unifying action or a physical theory.
