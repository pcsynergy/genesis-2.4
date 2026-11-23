# Unified Potential Theory — integration index

Unified Potential Theory is the conceptual umbrella for this research program. Its foundational sequence is Potential → One → Both → Many → All → Becoming → renewed Potential. See:

- UPT Foundational Specification 0.1: UPT_FOUNDATION.md
- UPT–OTFT Integration 0.1: UPT_OTFT_INTEGRATION.md
- UPT Configuration-Space Formalization 0.1: UPT_CONFIGURATION_SPACE.md — defines admissible configurations, constraints, relations, equivalence, actualization, and observables.
- UPT-3 Two-Component Relational Unity Experiment: UPT_THREE_EXPERIMENT.md — derives the common and difference modes for a symmetric two-node coupling model.
- UPT-4/5 Multi-Component Relational Network Tests: UPT_GRAPH_MILESTONES_4_5.md — tests graph-component convergence, state-domain preservation, and a model observable against an uncoupled baseline.\n- UPT-6 Conservation, Symmetry, and Physical Realization: UPT_SIX_CONSERVATION_CONTINUUM.md — derives a standard scalar-field shift charge, distinguishes diffusion from wave dynamics, and assesses the lack of a new empirical prediction.

UPT distinguishes ontological Potential (the domain of admissible possibilities) from a model's scalar potential-energy function and from an actualized field state. It does not supply a physical evolution law by itself. Every physical implementation must specify its configuration space, dynamics, symmetries, units, observables, and falsifiable predictions. Existing OTFT and cosmological experiments remain specific mathematical models and are not evidence that UPT has been empirically established.

---

# One Time Field Theory — Formal Specification Draft 0.2

**Status:** exploratory mathematical specification  
**Scope:** abstract network dynamics; no claim of physical unification

## 1. Core proposition

The working proposition is: **All Fields Lead to One.**

For this first formalization, interpret “One” modestly and operationally: many distinguishable local states may be represented within one mathematical structure whose relationships and evolution are specified together. This interpretation is testable as a mathematical model. It does not, by itself, imply that all physical fields are literally one field.

## 2. Primitive objects

A model instance is the tuple

    M = (V, W, phi, alpha, kappa, s, T)

where:

- V = {1,...,N} is a finite set of nodes, N >= 1.
- W is a real N-by-N weighted adjacency matrix.
- phi(t) is a real-valued state vector in R^N.
- alpha >= 0 is a local decay parameter.
- kappa >= 0 is a coupling parameter.
- s(t) is an externally specified source vector in R^N.
- T is the time interval over which the model is evaluated.

For the baseline model, W is symmetric, has nonnegative entries, and has a zero diagonal. These assumptions describe an undirected network without self-coupling.

## 3. Axioms of the baseline model

These are modeling axioms for the prototype, not claims about the universe.

**Axiom 1 — State assignment.** Each node i has exactly one real scalar state phi_i(t) at each modeled time.

**Axiom 2 — Relational structure.** Pairwise influence is represented by W_ij. If W_ij = 0, node j contributes no direct coupling term to node i.

**Axiom 3 — Symmetric interaction.** W_ij = W_ji. This makes the baseline network undirected.

**Axiom 4 — Nonnegative coupling.** W_ij >= 0 and kappa >= 0. The coupling term is diffusive: it tends to reduce differences between connected states.

**Axiom 5 — Local decay.** alpha >= 0. In the absence of coupling and source, each state obeys d(phi_i)/dt = -alpha*phi_i.

**Axiom 6 — External influence.** The source s_i(t) is specified independently of the state unless a later model explicitly defines feedback.

**Axiom 7 — Continuous-time evolution.** The state follows the differential equation in Section 4 wherever the source is sufficiently regular for the chosen solution concept.

## 4. Governing dynamics

The node-level equation is

    d(phi_i)/dt = -alpha*phi_i
                   + kappa*sum_j W_ij*(phi_j - phi_i)
                   + s_i(t)

Let D be the diagonal matrix of weighted degrees, D_ii = sum_j W_ij, and let L = D - W be the graph Laplacian. Then

    d(phi)/dt = -(alpha*I + kappa*L)*phi + s(t)

The system is linear when alpha, kappa, W are fixed and s is externally specified.

## 5. Derived mathematical consequences

Under the stated finite, symmetric, nonnegative graph assumptions:

1. L is symmetric and positive semidefinite.
2. With s(t)=0, the quadratic energy E(phi)=0.5*phi^T*phi has derivative

       dE/dt = -alpha*phi^T*phi - kappa*phi^T*L*phi <= 0.

   Thus this Euclidean state norm is non-increasing in continuous time.
3. With alpha=0 and s=0, the sum of node states is conserved because the rows and columns of L sum to zero.
4. If the graph is connected, alpha=0, and s=0, the only equilibrium states satisfy L*phi=0 and are constant across nodes.
5. If alpha>0 and s=0, the zero state is the unique equilibrium and the continuous-time system is asymptotically stable.

These are consequences of the chosen equation and assumptions; they are not empirical discoveries.

## 6. Boundary and initial conditions

A simulation must specify:

- Initial state phi(0)=phi_0.
- The adjacency matrix W and node ordering.
- Parameters alpha and kappa, including units or dimensionless status.
- The source function s(t), including its time dependence.
- A finite simulation interval [0,T].
- A numerical method and time step, plus convergence checks.

The current implementation supports a constant source vector over a run. Time-varying sources can be added through a callable interface in a later version.

## 7. Units and dimensional consistency

The model is dimensionally meaningful only after assigning units. One consistent abstract choice is:

- phi: state units U.
- t: time units T.
- alpha: T^-1.
- kappa*W_ij: T^-1, if W is dimensionless.
- s: U*T^-1.

If W carries units, kappa must be adjusted so that kappa*W has units T^-1. The software currently stores plain floating-point values and does not enforce units.

## 8. Falsifiable mathematical and computational predictions

These predictions test the implementation and model behavior, not the metaphysical proposition by itself.

**P1 — Mean conservation.** For alpha=0 and s=0 on a symmetric graph, the mean state remains constant up to numerical error. A reproducible violation indicates a coding error or a violated assumption.

**P2 — Dissipation.** For alpha>=0, kappa>=0, and s=0, the continuous-time Euclidean state norm cannot increase. Numerical increases that persist under time-step refinement would contradict the expected behavior or reveal an implementation defect.

**P3 — Consensus.** On a connected graph with alpha=0 and s=0, states approach a common value. On disconnected graphs, each connected component approaches its own component mean.

**P4 — Decay.** For kappa=0 and s=0, each state follows phi_i(t)=phi_i(0)*exp(-alpha*t). Numerical solutions should converge toward this analytic result as the step size is reduced.

**P5 — Superposition.** For fixed parameters and an externally prescribed source, the continuous-time model is linear. The response to a sum of initial conditions and sources is the sum of their separate responses.

## 9. What would be required for a physical theory

A physical interpretation must supply, at minimum:

- A defined mapping from phi and W to measurable physical quantities.
- Units and coordinate or gauge transformation behavior.
- Symmetries and conservation laws derived from an action or other explicit structure.
- A relationship to known theories in regimes where those theories are experimentally successful.
- Quantitative predictions that differ from competing models.
- A reproducible route from raw observations to parameter estimates and uncertainty bounds.

Until these are supplied and tested, the model remains an abstract network-dynamics prototype.

## 10. Open questions for later research

1. Should the primitive state be scalar, vector, complex, or tensor-valued?
2. Is the graph fixed, adaptive, or itself a dynamical variable?
3. Should the model be local in time, or should it include memory kernels?
4. What symmetries should constrain allowed couplings?
5. Can a proposed extension recover established oscillator, diffusion, or field equations in suitable limits?
6. What observation could distinguish the proposal from standard alternatives?

## 11. Versioning rule

Any change to the axioms, state space, governing equation, or physical interpretation must increment the specification version and document which prior predictions remain valid.
