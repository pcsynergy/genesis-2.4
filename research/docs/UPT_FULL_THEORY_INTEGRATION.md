# Unified Potential Theory — Integrated Full-Theory Reference Model

**Author:** Pablo Salvador Cardenas  
**Version:** Integrated computational reference, 0.1  
**Status:** A modular research framework with executable mathematical prototypes; not an empirically established physical theory.

## 1. Purpose

This document connects the UPT research strands into one explicit architecture. It is not a claim that the current modules have been derived from a single fundamental equation. The integration is a shared relational graph and a transparent sequence of model layers, each retaining its own state space, dynamics, assumptions, and validation criteria.

The guiding proposition remains:

**The Potential precedes the One.**

\[
\mathcal P\rightarrow 1\rightarrow 2\rightarrow N\rightarrow\mathcal A
\rightarrow\mathcal C\rightarrow\mathcal P'.
\]

Potential denotes admissible possibility; One denotes a coherent whole; Both denotes distinction and relation; Many denotes differentiated components; All denotes the complete modeled relational system; Becoming denotes state evolution; and renewed Potential denotes a changed admissible domain.

This sequence is an ontological organizing hypothesis. It is not asserted to be a measured chronology or a physical time parameter.

## 2. Full state architecture

The UPT conceptual state is

\[
\mathfrak U=(\Omega,\Psi,\mathcal R,\mathcal I,\mathcal E,
\mathcal M,\mathcal X),
\]

where:

- \(\Omega\): admissible configuration space;
- \(\Psi\): actualized model state;
- \(\mathcal R\): relational graph, constraints, or correlations;
- \(\mathcal I\): interaction and transition rules;
- \(\mathcal E\): energy functionals, transfer, and conservation statements;
- \(\mathcal M\): organized field or matter configurations;
- \(\mathcal X\): observations, records, and experience variables.

A model instance must further specify an evolution parameter \(\lambda\), a state space, boundary conditions, and parameters:

\[
\frac{d\Psi}{d\lambda}
=\mathcal F(\Psi,\mathcal R,\mathcal I;\theta).
\]

UPT does not uniquely determine \(\mathcal F\). The executable reference model therefore uses multiple well-defined operators rather than pretending that one has already been derived.

## 3. The integrated mathematical layers

### 3.1 Potential: admissible configurations and renewal

For a finite binary network, configurations are \(q\in\{0,1\}^N\). An initial admissible set can be constrained by a fixed active count:

\[
\Omega_0=\{q:\sum_iq_i=k\}.
\]

A declared local activation rule expands the domain when an inactive node has sufficient active-neighbor support:

\[
q_i=0,\qquad \sum_jW_{ij}q_j\geq\vartheta.
\]

The finite renewal operator gives \(\Omega_{n+1}=\mathscr R(\Omega_n)\). This makes the distinction between redistribution within a fixed domain and expansion of the admissible domain explicit. It is a toy configuration-space rule, not evidence of physical creation.

### 3.2 One, Both, Many, and All: relational structure

The shared relation network is a symmetric nonnegative adjacency matrix \(W\), with graph Laplacian \(L=D-W\). A simple relational disagreement functional is

\[
E_{\rm rel}(\phi)=\frac{J}{2}
\sum_{i<j}W_{ij}(\phi_i-\phi_j)^2.
\]

The common graph is the mathematical bridge across discrete configurations and continuous node fields. The One is represented operationally by a common state description; Both by distinguishable nodes and edges; Many by the collection of node variables; All by the complete graph and its boundary conditions. These are model roles, not new physical entities.

### 3.3 Energy and continuous becoming: dissipative graph field

For node fields \(\phi_i\) and a global memory coordinate \(m\), the reference energy is

\[
H(\phi,m)=
\frac{J}{2}\sum_{i<j}W_{ij}(\phi_i-\phi_j)^2
+\frac{\kappa}{2}\left(\sum_i\phi_i-m\right)^2
+\frac{\lambda}{4}\sum_i\phi_i^2(1-\phi_i)^2.
\]

With positive mobilities, the Onsager gradient flow is

\[
\dot\phi_i=-\Gamma_\phi\frac{\partial H}{\partial\phi_i},
\qquad
\dot m=-\Gamma_m\frac{\partial H}{\partial m}.
\]

It obeys

\[
\frac{dH}{dt}=
-\Gamma_\phi\sum_i\left(\frac{\partial H}{\partial\phi_i}\right)^2
-\Gamma_m\left(\frac{\partial H}{\partial m}\right)^2\leq0.
\]

This is a dissipative gradient-flow model. It is not conservative Hamiltonian evolution, relativistic wave dynamics, or a derived law of nature.

### 3.4 Reversible memory: a distinct stochastic model class

The finite augmented state \(X=(q,m_d)\), with discrete memory coordinate \(m_d\), is modeled as a continuous-time Markov chain with Metropolis rates. Its Gibbs stationary distribution obeys detailed balance. This stochastic equilibrium model is not the same trajectory as the deterministic gradient flow above. In the reference implementation it is a parallel description of relational memory on the same finite graph, not a transition rule derived from the continuous field.

### 3.5 Continuum limit

The scalar field continuum prototype has energy

\[
H[\phi,m]=\int_0^L\left[
\frac J2(\partial_x\phi)^2+
\frac\lambda4\phi^2(1-\phi)^2
\right]dx+
\frac{\kappa L}{2}(\bar\phi-m)^2.
\]

Its periodic finite-difference implementation is refined across spatial resolutions. The refinement test checks numerical convergence for a specified smooth initial condition. This is a continuum limit of that selected gradient-flow model, not a derivation of the entire UPT ontology or of every discrete stochastic layer.

### 3.6 Observation and experience: measurement layer

The reference inference model uses

\[
m_{i+1}=u_i+(m_i-u_i)e^{-r\Delta t_i},\qquad
y_i=m_i+\epsilon_i,\qquad
\epsilon_i\sim\mathcal N(0,\sigma^2).
\]

It estimates \(r\), constructs a parametric bootstrap interval, and calibrates a null test under \(r=0\). The initial condition and noise scale are treated as known; inputs are prescribed. This layer represents an observation protocol, not a theory of consciousness and not proof that experience creates physical reality.

## 4. How the executable integration is assembled

The reference runner uses one four-node cycle graph and reports:

1. finite admissible-domain sizes under renewal;
2. stationary probability normalization and detailed-balance residual for the reversible Markov model;
3. energy change and final state for the dissipative graph field;
4. continuum-grid refinement errors;
5. noisy relaxation-rate estimation, a bootstrap interval, and null-calibrated p-value.

The layers share a graph and a reporting contract. Their distinct dynamics are kept explicit. In particular:

- the discrete renewal rule is not the Markov transition generator;
- the equilibrium CTMC is not the gradient-flow ODE;
- the continuum refinement is not automatically the continuum limit of the CTMC;
- the observation relaxation fit is a phenomenological model applied to sampled signals.

The runner's integration contract records these boundaries so a future derivation cannot silently conflate them.

## 5. Potential and energy: unresolved ontological hypotheses

UPT continues to preserve two live hypotheses:

- **Potential-first:** admissible possibility and relational structure are primitive; energy is defined after a model and its interactions are specified.
- **Co-fundamental potential-energy structure:** potential and energy are inseparable aspects of a deeper relational structure.

The current computational modules do not decide between these ontologies. The scalar function \(V(\Psi)\) in a conventional action is model potential energy; it is not identical by definition to ontological Potential \(\mathcal P\).

## 6. Mapping the wider research program

| Program | Role in the integrated architecture | Current evidential status |
|---|---|---|
| Unified Potential Theory | Ontological and mathematical umbrella | Conceptual framework |
| One Time Field Theory | Relational temporal order and clock observables | Research hypothesis; no derived universal time field |
| OntoField Theory | Candidate field-state and relation architecture | Formal development required |
| Polyhedron/Cube Field Network | Geometric and graph representations of relations | Model geometry |
| Harmonic Consciousness Theory | Resonance, information, and experience questions | Speculative research; no consciousness mechanism established |
| Harmonic Branching | Alternative trajectories and admissible paths | Mathematical/visual representation |
| Harmonic Becoming | Temporal and developmental visualization | Interpretive/visual framework |

No symbolic correspondence or analogy in this table is evidence of physical equivalence.

## 7. Verification and scientific status

The integration tests check domain expansion, finite closure, probability normalization, detailed balance, energy nonincrease, continuum refinement, and noisy-inference outputs. Passing tests establish implementation properties under stated assumptions.

They do not establish:
- that Potential is a physical substance or field;
- that all known interactions are unified;
- that time is a field or emerges from the model;
- that the memory variable exists in nature;
- that the framework explains consciousness;
- that any fitted synthetic parameter is a physical constant.

## 8. Requirements before calling UPT a validated physical theory

A physical theory needs at least one fully specified model with:

1. operational definitions and measurement operators for every claimed physical variable;
2. dimensional consistency and calibrated units;
3. a well-posed action or evolution law derived from stated principles;
4. symmetries, conservation laws, and causal structure;
5. limiting agreement with established physics where existing tests are strong;
6. a quantitative prediction that differs from competing theories;
7. uncertainty-aware comparison on independent empirical data;
8. reproducible numerical convergence, stability, and robustness tests;
9. independent replication and explicit failure conditions.

## 9. Executable entry points

- Module: research/one_time_field/upt_full_theory.py
- Tests: research/tests/test_upt_full_theory.py
- Runner: research/examples/upt_full_theory_experiment.py

Run the integrated suite with the repository research-test workflow. The default runner uses fixed seeds and synthetic observations.

**Foundational statement:** The Potential precedes the One; the One permits distinction; distinction establishes relationship; relationship enables interaction; interaction expresses actuality; actuality continues through becoming; and becoming opens renewed potential.

**Attribution:** Pablo Salvador Cardenas.
