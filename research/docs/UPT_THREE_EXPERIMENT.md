# UPT-3 — Two-Component Relational Unity Experiment

**Author:** Pablo Salvador Cardenas  
**Version:** 0.1  
**Status:** exact mathematical toy model; not a physical unification claim

## 1. Research question

Can a relation between two distinguishable states produce a shared mode that is not identical to either component alone?

This experiment operationalizes a narrow part of the UPT sequence:

\[
\text{Potential domain}\;\longrightarrow\;\text{One common structure}
\;\longrightarrow\;\text{Both distinguishable states}
\;\longrightarrow\;\text{relational interaction}.
\]

The model does not assume that the One is a substance or a new physical field. It asks whether a common relational mode can be identified mathematically.

## 2. Model

Let two real-valued states be \(x_1(t)\) and \(x_2(t)\). Their symmetric coupling is

\[
\dot{x}_1=\kappa(x_2-x_1),\qquad
\dot{x}_2=\kappa(x_1-x_2),\qquad \kappa\geq0.
\]

In vector form,

\[
\dot{\mathbf x}=-\kappa L\mathbf x,\qquad
L=\begin{pmatrix}1&-1\\-1&1\end{pmatrix}.
\]

The graph Laplacian has eigenvectors

\[
v_+=(1,1)^T,\quad \lambda_+=0;
\qquad
v_-=(1,-1)^T,\quad \lambda_-=2.
\]

Thus the common mode is stationary and the difference mode decays. Defining

\[
m=\frac{x_1+x_2}{2},\qquad d=x_1-x_2,
\]

gives

\[
\dot m=0,\qquad \dot d=-2\kappa d.
\]

The exact solution is

\[
m(t)=m(0),\qquad d(t)=d(0)e^{-2\kappa t},
\]

\[
x_1(t)=m(0)+\frac{d(0)}2e^{-2\kappa t},\qquad
x_2(t)=m(0)-\frac{d(0)}2e^{-2\kappa t}.
\]

## 3. Relational energy and admissibility

Define a nonnegative disagreement functional

\[
E_R(t)=\frac{\kappa}{2}(x_1-x_2)^2.
\]

Its derivative is

\[
\frac{dE_R}{dt}
=\kappa d\dot d
=-2\kappa^2d^2\leq0.
\]

For positive coupling, disagreement decreases monotonically and both states approach the conserved mean. For zero coupling, the states remain independent. This limiting case is important: shared structure is not forced when the relation is absent.

For this toy model the admissible state space is \(\Omega=\mathbb R^2\); there are no additional constraints. The exact flow maps finite initial states to finite states for all finite nonnegative times, so it preserves this domain.

## 4. Experiment protocol

The reproducible runner uses initial state \((0,2)\) and coupling \(\kappa=0.3\). It evaluates the exact solution at selected times and reports each component, common mode, and difference. Unit tests check:

- exact exponential decay of the difference mode;
- invariance of the mean;
- monotonic decrease of relational energy;
- the uncoupled limit;
- rejection of invalid inputs.

The implementation is in `research/one_time_field/two_node_relational.py`, tests in `research/tests/test_two_node_relational.py`, and runner in `research/examples/two_node_relational_experiment.py`.

## 5. Interpretation

The mathematical result is exact for the specified model: symmetric coupling preserves the common mode and exponentially suppresses the difference mode. In the long-time limit, the two components converge to their initial arithmetic mean.

This is a standard consensus/diffusion result for a two-node graph Laplacian. It does **not** show that unity is more fundamental than its components in nature, that physical fields unify through this mechanism, or that UPT has empirical support. The common mode is present because the model's symmetric coupling and graph Laplacian were specified at the outset.

The result does clarify one operational reading of UPT: a unified description can contain distinguishable components while its relational dynamics selects a shared collective mode. Unity here is a property of the coupled mathematical system, not an additional entity.

## 6. Result and next test

**UPT-3 outcome:** the model analytically exhibits a conserved common mode and decaying difference mode for \(\kappa>0\); no numerical integration error is involved because the solution is evaluated in closed form. The software tests verify the implementation of these identities.

The next milestone, UPT-4, should generalize the construction to a small weighted graph and test whether the declared admissible subspace is preserved under the graph dynamics, including disconnected graphs, nonuniform weights, and multiple zero Laplacian eigenvalues.

---
**Attribution:** Pablo Salvador Cardenas.  
**Scientific status:** mathematical demonstration only; independent review and physical interpretation remain open.
