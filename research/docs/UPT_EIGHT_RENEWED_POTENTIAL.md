# UPT-8: Renewed Potential and Adaptive Admissibility

**Author:** Pablo Salvador Cardenas  
**Status:** finite mathematical prototype; not an empirically established physical theory

## 1. Research question

UPT-7 changed probabilities over a fixed admissible configuration space. UPT-8 asks whether an explicit interaction rule can change the admissible space itself:

\[
\Omega_{r}\longrightarrow\Omega_{r+1}.
\]

Here, r labels a renewal round, not physical time. The model distinguishes domain expansion from probability redistribution.

## 2. Initial possibility space

Use four binary degrees of freedom on an undirected four-cycle:

\[
q=(q_1,q_2,q_3,q_4),\qquad q_i\in\{0,1\}.
\]

The ambient space contains 16 states. The initial admissible domain is

\[
\Omega_0=\{q:\sum_iq_i=2\},
\]

which contains six configurations, matching UPT-7.

## 3. Interaction-driven renewal rule

Let W be the symmetric, nonnegative cycle adjacency matrix. For node i, define active-neighbor support

\[
h_i(q)=\sum_jW_{ij}q_j.
\]

A previously inactive component becomes eligible for activation when

\[
q_i=0,\qquad h_i(q)\geq\theta,
\]

where the threshold \(\theta>0\) is declared before the simulation. A synchronous renewal round is

\[
\Omega_{r+1}=\Omega_r\cup
\{q+e_i:q\in\Omega_r,\ q_i=0,\ h_i(q)\geq\theta\}.
\]

The rule is explicit, local on the graph, monotone, and finite. It is a modeling choice, not a law derived from UPT or from nature. It is intentionally irreversible: no state is removed. A reversible extension would require a separate deactivation rule and a specified balance condition.

## 4. Relational weighting and observable

On each current domain, retain the UPT-7 relational energy

\[
E_J(q)=\frac{J}{2}\sum_{i<j}W_{ij}(q_i-q_j)^2
\]

and normalized distribution

\[
p_r(q)=\frac{e^{-\beta E_J(q)}}{Z_r},\qquad
Z_r=\sum_{q\in\Omega_r}e^{-\beta E_J(q)}.
\]

For total edge weight \(W_\Sigma=\sum_{i<j}W_{ij}\), define

\[
\langle C\rangle_r=
\sum_{q\in\Omega_r}p_r(q)
\left[1-\frac{\sum_{i<j}W_{ij}(q_i-q_j)^2}{W_\Sigma}\right].
\]

The distribution is recomputed after every domain expansion. Thus two effects remain distinct: the admissible state count changes, and the probability distribution is renormalized over the new domain.

## 5. Exact four-cycle result

For unit-weight edges and threshold \(\theta=1\):

| Renewal round | Admissible states | Newly admitted states |
|---:|---:|---:|
| 0 | 6 | 0 |
| 1 | 10 | 4 |
| 2 | 11 | 1 |
| 3 and later | 11 | 0 |

The six initial two-active states each permit at least one neighboring activation; collectively they admit all four three-active states. Those states then admit the fully active state. The resulting 11-state domain is closed under the rule. The remaining five ambient states (zero- and one-active configurations) are not reachable under this activation-only mechanism.

This demonstrates a mathematically defined change in admissibility, not the creation of possibilities in the physical universe.

## 6. Tests and interpretation

The implementation tests:
- agreement of the initial six-state domain with UPT-7;
- exact state counts 6, 10, and 11;
- monotonicity and finite closure;
- no renewal without graph edges;
- threshold dependence;
- probability normalization at each round;
- uniform probabilities at zero relational coupling;
- rejection of invalid inputs.

The model separates UPT's stages operationally: the ambient binary space represents the declared possibility set; the six-state constraint defines initial admissibility; graph relations provide local support; the renewal rule enlarges the admissible domain; and the Gibbs distribution supplies a separate weighting over that domain.

## 7. Limitations and next requirements

The activation rule is one explicit mechanism among many. Its monotonicity makes closure easy to test but excludes deactivation, memory, and detailed balance. The graph and binary variables have no established physical interpretation. The parameters \(J\), \(\beta\), and \(\theta\) are model parameters, not measured constants.

A physical proposal would need to identify the degrees of freedom, derive the activation rule from microscopic dynamics or an action, define units and observables, compare against a fixed-domain baseline, and produce a measurable deviation with uncertainty bounds. Until then, UPT-8 is a finite mathematical demonstration of adaptive admissibility, not empirical validation of UPT.
