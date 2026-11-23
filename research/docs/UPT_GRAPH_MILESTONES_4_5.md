# UPT-4 and UPT-5 — Multi-Component Relational Network Tests

**Author:** Pablo Salvador Cardenas  
**Version:** 0.1  
**Status:** reproducible mathematical experiments; not a physical unification claim

## 1. Scope

UPT-4 generalizes the two-component relational model to finite, weighted, undirected graphs. UPT-5 asks whether a simple observable distinguishes coupled evolution from an uncoupled baseline. Both use the existing `GraphFieldNetwork` diffusion-with-decay engine with decay set to zero. The work does not modify the legacy GENESIS simulator.

The state vector is \(x\in\mathbb R^N\), and the symmetric nonnegative adjacency matrix is \(W\). With graph Laplacian \(L=D-W\), the dynamics are

\[
\dot x=-\kappa Lx,\qquad \kappa\geq0.
\]

For a symmetric graph, \(L\) is positive semidefinite and \(L\mathbf 1=0\). Consequently,

\[
\frac{d}{dt}\mathbf 1^Tx
=-\kappa\mathbf 1^TLx=0.
\]

The arithmetic mean is conserved. The quadratic disagreement about the mean,

\[
D(x)=\sum_i(x_i-\bar x)^2,
\qquad
\bar x=\frac1N\sum_i x_i,
\]

is nonincreasing in continuous time because

\[
\frac{dD}{dt}=-2\kappa x^TLx\leq0.
\]

For a connected graph, the only zero mode is the uniform vector, so all nodes converge to the global mean. For a disconnected graph, each connected component has its own conserved mean; convergence is component-wise, not global.

## 2. UPT-4 — admissibility and topology

The ambient state space is \(\Omega=\mathbb R^N\). The graph is fixed during each run. No extra state constraints are imposed. Therefore the linear flow is globally defined and maps finite states to finite states. The numerical implementation uses explicit Euler. For symmetric nonnegative weights, a sufficient monotonicity/stability condition is

\[
\Delta t\,\kappa\,d_{\max}\leq1,
\]

where \(d_{\max}\) is the maximum weighted degree. This follows from \(\lambda_{\max}(L)\leq2d_{\max}\) and the Euler amplification factors \(1-\Delta t\kappa\lambda_j\). The experiments choose time steps well inside this bound.

### Tested configurations

- Three-node connected path, initial state \((0,2,7)\): all nodes converge to mean \(3\).
- Two disconnected pairs, initial state \((0,2,4,10)\): the first pair converges to \(1\), the second to \(7\).
- Nonuniform symmetric edge weights: arithmetic mean remains invariant.
- Zero coupling: every state remains unchanged.

These tests distinguish connected global unity from multiple disconnected collective modes. Network topology determines which components can exchange state through the specified coupling.

## 3. UPT-5 — observable and baseline comparison

The declared model observable is the disagreement

\[
D(x)=\sum_i(x_i-\bar x)^2.
\]

For two nodes initialized at \((0,2)\), the coupled model uses \(\kappa=0.5\), while the baseline uses \(\kappa=0\). With \(\Delta t=0.01\) for 1,000 steps (model time 10), the baseline retains its initial disagreement \(D=2\). The coupled model approaches consensus and its disagreement falls below \(10^{-6}\).

This is a clear prediction *within the toy model*: nonzero symmetric coupling suppresses disagreement, whereas the uncoupled baseline does not. It is not yet a prediction about a physical system. To become empirical, the states, coupling, time scale, and disagreement observable would need an independently justified mapping to measurable quantities, followed by comparison with real data and uncertainty estimates.

## 4. Numerical limitations

Explicit Euler is conditionally stable. The step-size bound is checked for the chosen examples, and the unit tests check mean conservation, component-wise convergence, monotonic disagreement under the selected stable step, and the zero-coupling limit. These are implementation and model-consistency checks, not evidence of a new physical law.

For arbitrary graphs, the rate of convergence depends on the nonzero spectrum of the graph Laplacian. This milestone does not estimate a universal rate law or infer network topology from observations.

## 5. Results and interpretation

**UPT-4:** the admissible state domain \(\mathbb R^N\) is preserved by the linear evolution. Connected graphs approach one common mean; disconnected graphs approach separate component means. The graph's connected components define the independent collective sectors.

**UPT-5:** the disagreement observable distinguishes coupled and uncoupled trajectories in the specified numerical experiment. The difference is reproducible and follows directly from the chosen equations.

The result provides a mathematical interpretation of Potential → One → Both → Many → All: a network can contain many distinguishable components, and its relational topology determines whether one or several collective modes emerge. The conclusion is limited to this graph-diffusion class. It does not show that all physical fields unify, nor does it establish ontological Potential as a measured entity.

## 6. Next scientific threshold

A physical UPT proposal must identify a real system, map model states and couplings to independently measured quantities, derive parameters without arbitrary fitting, and predict an outcome that differs from a credible baseline. It must then survive uncertainty analysis, alternative model comparison, and independent replication.

---
**Attribution:** Pablo Salvador Cardenas.  
**Research status:** mathematical network tests; physical interpretation and independent review remain open.
