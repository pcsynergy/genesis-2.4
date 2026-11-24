# UPT-10: Deriving Relational and Memory Dynamics from a Variational Principle

**Author:** Pablo Salvador Cardenas  
**Status:** finite-dimensional dissipative variational prototype; no empirical physical claim

## Research question

Can relational coupling, memory coupling, and a tendency toward discrete-like configurations be represented by one energy functional, with dynamics derived from a variational principle rather than chosen as unrelated update rules?

UPT-10 supplies a limited affirmative mathematical demonstration. It does not derive the UPT-9 Metropolis transition rates from an ordinary conservative action.

## 1. State and energy

Let \(\phi_i\in\mathbb R\) be a continuous field value on each vertex of a finite, undirected weighted graph, and let \(m\in\mathbb R\) be a global memory coordinate. For symmetric nonnegative adjacency \(W\), define

\[
H(\phi,m)=\frac J2\sum_{i<j}W_{ij}(\phi_i-\phi_j)^2
+\frac\kappa2\left(\sum_i\phi_i-m\right)^2
+\frac\lambda4\sum_i\phi_i^2(1-\phi_i)^2.
\]

The first term penalizes graph disagreement. The second couples the present field aggregate to memory. The quartic term has minima at 0 and 1 and provides a continuous interpolation toward binary configurations. These are model choices, not uniquely implied by UPT.

## 2. Dissipative variational principle (Onsager)

For positive mobilities \(\Gamma_\phi,\Gamma_m\), define the Rayleigh dissipation potential

\[
\mathcal D(\dot\phi,\dot m)=
\frac{1}{2\Gamma_\phi}\sum_i\dot\phi_i^2
+\frac{1}{2\Gamma_m}\dot m^2.
\]

At each instant, minimize the Rayleighian

\[
\mathscr R=\frac{dH}{dt}+\mathcal D
=\nabla_\phi H\cdot\dot\phi
+\partial_mH\,\dot m+\mathcal D.
\]

Stationarity with respect to each velocity gives

\[
\dot\phi_i=-\Gamma_\phi\frac{\partial H}{\partial\phi_i},
\qquad
\dot m=-\Gamma_m\frac{\partial H}{\partial m}.
\]

This is an Onsager/gradient-flow principle for dissipative relaxation. It is not Hamilton's least-action principle for a conservative system.

The derivatives are

\[
\frac{\partial H}{\partial\phi_i}
=J\sum_{j\ne i}W_{ij}(\phi_i-\phi_j)
+\kappa\left(\sum_j\phi_j-m\right)
+\frac\lambda2\phi_i(1-\phi_i)(1-2\phi_i),
\]

\[
\frac{\partial H}{\partial m}
=-\kappa\left(\sum_i\phi_i-m\right).
\]

## 3. Dissipation identity

Along the derived flow,

\[
\frac{dH}{dt}
=-\Gamma_\phi\sum_i\left(\frac{\partial H}{\partial\phi_i}\right)^2
-\Gamma_m\left(\frac{\partial H}{\partial m}\right)^2
\le 0.
\]

The implementation checks this identity and uses backtracking explicit steps to prevent numerical energy increase. This is a model-level Lyapunov result, not a claim that all physical processes monotonically reduce energy.

## 4. Relation to UPT-9 and conservative action

UPT-9 is a finite continuous-time Markov chain with Metropolis rates and a Gibbs stationary distribution. Its generator and detailed balance are defined by transition rates over discrete augmented states. The UPT-10 flow is deterministic and continuous-valued. The shared conceptual element is a relational-plus-memory energy, but the dynamics differ.

In particular:
- A conservative Lagrangian yields Euler–Lagrange equations and generally permits energy exchange/conservation.
- The Onsager principle above yields dissipative gradient flow.
- A Markov master equation evolves probability distributions and needs a transition generator.
- A nonequilibrium model requires explicit driving, reservoirs, or nonzero cycle affinities.

Therefore UPT-10 does **not** claim that the UPT-9 Metropolis rates follow from this deterministic variational principle. A stochastic path-space or master-equation variational formulation would be a separate extension.

## 5. Verification protocol

Seven tests verify the analytic gradient against centered finite differences, the exact energy-dissipation identity, non-increasing energy under backtracked steps, graph-uniform-mode behavior, mobility limits, and input validation. The experiment runner prints the initial dissipation and a short energy trajectory.

## 6. Scope and next questions

The prototype demonstrates that one chosen relational-memory functional can generate a consistent dissipative flow. It does not establish that this functional is unique, fundamental, or physically realized. Parameters are dimensionless and not fitted to observations.

Next research steps:
1. Establish units and a controlled graph-to-continuum limit.
2. Compare the Onsager flow with the UPT-9 Markov generator in an explicitly defined limit.
3. Add noise with a fluctuation-dissipation relation if an equilibrium stochastic field model is intended.
4. Derive observables and compare against standard statistical-mechanical baselines.
5. Keep conservative, dissipative, and driven dynamics as separate model classes unless a derivation connects them.

**Attribution:** Pablo Salvador Cardenas.
