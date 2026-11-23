# UPT-7: Potential, Field Interaction, and Observable Emergence

**Author:** Pablo Salvador Cardenas  
**Status:** finite mathematical prototype; not an empirically established physical theory

## 1. Research question

Can the UPT sequence be given a small operational realization in which (i) a space of possibilities is defined before selecting a state, (ii) admissibility constraints restrict that space, (iii) relationships alter the relative weight of admissible states, and (iv) an observable records the resulting change?

This milestone constructs a deliberately modest finite model. It does not identify ontological Potential with a physical field or claim a new fundamental interaction.

## 2. Configuration space: Potential

Take four binary degrees of freedom,

    q = (q_1, q_2, q_3, q_4),  q_i in {0,1}.

The ambient configuration space contains 2^4 = 16 states. Impose the admissibility constraint

    C(q) = sum_i q_i - 2 = 0.

The admissible domain therefore contains exactly six states:

    Omega_P = {q in {0,1}^4 : sum_i q_i = 2}.

This is a finite, explicit model representation of a restricted possibility space. It is not the totality of ontological possibility.

## 3. One, Both, and Many: common structure and relations

All four components belong to one declared model. The components remain distinguishable, while a symmetric adjacency matrix W defines their relational structure. For the four-cycle,

    W_12 = W_23 = W_34 = W_41 = 1,

with other off-diagonal weights zero. The common structure is the “One” in the limited operational sense established in the UPT configuration-space formalization. Four binary variables provide a small “Many”; the fixed-count condition ensures at least two active and two inactive components (“Both”).

## 4. Relational interaction and actualization weights

Define the relational disagreement measure

    K(q) = sum_(i<j) W_ij (q_i - q_j)^2.

Define a dimensionless model energy

    E_J(q) = (J/2) K(q),  J >= 0.

For a declared inverse-noise or inverse-temperature parameter beta >= 0, assign each admissible state the normalized weight

    p_J(q) = exp[-beta E_J(q)] / Z,
    Z = sum_(q in Omega_P) exp[-beta E_J(q)].

This is a standard finite Gibbs distribution. It is used here as one possible stochastic actualization rule. It is not derived uniquely from the UPT ontology. J and beta are dimensionless model parameters in this prototype; no physical units or measured values are claimed.

At J=0 all six admissible states are equiprobable. At positive J, states with fewer disagreeing edges receive greater weight. The admissibility constraint remains exact: the model redistributes probability among allowed states but never assigns weight outside Omega_P.

## 5. Observable emergence

Use the normalized relational coherence observable

    C(q) = 1 - K(q) / sum_(i<j) W_ij.

Its expectation is

    <C>_J = sum_(q in Omega_P) p_J(q) C(q).

The comparison is between the uncoupled baseline J=0 and a coupled model J>0, with the same graph, admissible domain, and beta. For the four-cycle with two active sites:

- There are six admissible configurations.
- Four configurations have edge cut K=2.
- Two configurations have edge cut K=4.
- At J=0, <K>=8/3 and <C>=1/3.
- At beta=1 and J=1, the exact finite sum gives a lower expected cut and higher expected coherence than the uncoupled baseline.

This is a conditional model-level prediction: if the specified Gibbs weighting is adopted, relational coupling shifts the distribution toward configurations with fewer disagreeing edges. It is not evidence that nature follows this distribution.

## 6. Interpretation in UPT terms

| UPT stage | Operational element in this experiment |
|---|---|
| Potential | Ambient 16-state space, then admissible six-state subset |
| One | One shared mathematical structure containing all four variables |
| Both | Binary distinction between active and inactive components |
| Many | Four related degrees of freedom on a cycle |
| All | Complete finite graph/model domain under study |
| Becoming | Stochastic weighting/selection over admissible configurations |
| Renewed Potential | Not implemented; would require a rule changing the admissible domain itself |

The sequence is an interpretive mapping, not a claim that these stages are universal physical events.

## 7. What this does and does not establish

**Established by exact enumeration and tests:** the admissible state count, normalization of probabilities, the uniform zero-coupling baseline, and the change in the coherence expectation when J is positive.

**Not established:** that the Gibbs rule is the correct actualization law for UPT; that J corresponds to a fundamental physical coupling; that the binary variables represent a known physical field; or that the result differs from statistical mechanics. In fact, the construction is mathematically a small constrained Gibbs ensemble with pairwise interaction.

Therefore UPT-7 makes a clear, reproducible model prediction but does not yet make a distinctive empirical prediction about nature.

## 8. Requirements for the next physical step

To move beyond the toy model, a candidate realization must:

1. Identify physical degrees of freedom corresponding to q_i.
2. Derive or independently justify the admissibility constraint.
3. Derive the relational interaction from an action, microscopic dynamics, or independently supported stochastic process.
4. Fix J and beta from independent physical measurements and specify their units or dimensionless definitions.
5. Identify a measurable coherence observable and its measurement protocol.
6. Compare against the relevant established model under identical conditions.
7. State an uncertainty budget and a falsification criterion.

## 9. Reproducibility

From the repository root:

    python -m unittest discover -s research/tests -v
    python research/examples/upt7_configuration_experiment.py

The implementation uses exact enumeration of the finite state space; no Monte Carlo approximation is needed.

---
**Attribution:** Pablo Salvador Cardenas.  
**Research status:** UPT-7 prototype 0.1; mathematical demonstration only.
