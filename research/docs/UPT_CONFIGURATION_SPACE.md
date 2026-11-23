# Unified Potential Theory — Configuration-Space Formalization 0.1

**Author:** Pablo Salvador Cardenas  
**Project:** GENESIS 2.4 / One Time Field research foundation  
**Status:** mathematical framework proposal; not an empirically established physical theory

## 1. Objective and scope

This document turns one part of Unified Potential Theory (UPT) into a precise mathematical research object: the space of admissible configurations. It does not claim that ontological Potential has been discovered as a physical field, nor does it introduce a new force or evolution law.

The guiding proposition remains:

> **The Potential precedes the One.**

Here, “Potential” means the range of configurations that a theory permits before a particular configuration is selected or realized. A mathematical model can represent part of this idea, but the representation is not automatically identical to the full ontological claim.

## 2. The configuration-space object

Let a candidate model be specified by

\[
\mathfrak M=(\Omega,\mathscr S,\mathscr C,\mathscr R,\mathscr D,\mathscr O),
\]

where:

- \(\Omega\) is a declared ambient set of candidate configurations;
- \(\mathscr S\) is the mathematical structure on \(\Omega\) (for example, topology, measurable structure, differentiable structure, or a Hilbert-space structure, as appropriate);
- \(\mathscr C\) is the collection of admissibility constraints;
- \(\mathscr R\) specifies relations among configurations or degrees of freedom;
- \(\mathscr D\) specifies permitted dynamics or transition rules;
- \(\mathscr O\) specifies observables and the map from model states to predicted records.

The **admissible configuration space** is

\[
\boxed{\Omega_{\mathcal P}
=\{q\in\Omega:\ C_a(q)=0\ \forall a,\quad
G_b(q)\leq 0\ \forall b\}.}
\]

The symbols \(C_a\) and \(G_b\) denote equality and inequality constraints. The constraint families may be finite or infinite. Their form, regularity, and physical meaning must be declared for each model.

This is a model-level representation of admissible potential. It is not a proof that all conceivable or ontologically possible states have been captured.

## 3. Three objects that must not be conflated

UPT requires a strict distinction among:

1. **Ontological Potential** \(\mathcal P\): the philosophical proposal that possibility or capacity is prior to realized distinctions.
2. **Admissible configuration space** \(\Omega_{\mathcal P}\): the set of configurations allowed by a specified mathematical model and its constraints.
3. **Potential-energy functional** \(V[q]\) or \(V(\Psi)\): a model-dependent function with defined units that contributes to the dynamics of a particular physical system.

In general,

\[
\mathcal P\;\not\equiv\;\Omega_{\mathcal P}
\qquad\text{and}\qquad
\Omega_{\mathcal P}\;\not\equiv\;V.
\]

A potential-energy function can help determine which configurations are dynamically favored, but it does not by itself define the complete set of admissible configurations. A configuration space may exist mathematically without a unique energy functional.

## 4. Relations, distinction, and the “One”

A configuration may contain distinguishable components. Write a general configuration as

\[
q=(q^1,q^2,\ldots,q^n),
\]

where the components need not be spatial fields; they may be variables, fields, network states, or other degrees of freedom.

Relations are represented by a declared structure \(\mathscr R\). Depending on the model, this may be:

- a graph or adjacency relation among components;
- a coupling map between fields;
- a constraint linking otherwise distinct variables;
- a metric, connection, or other geometric structure;
- a relational observable.

The “One” can then be represented modestly as a common mathematical structure in which distinguishable components and their relations are specified together. This is an operational interpretation of unity, not a claim that all physical fields have been proven to be one substance.

The distinction “Both” is represented by at least two distinguishable degrees of freedom. “Many” is represented by a larger collection of degrees of freedom and relations. “All” refers to the complete coupled model domain under consideration—not necessarily the totality of the universe.

## 5. Equivalence and physically distinct states

Different mathematical descriptions can represent the same physical state. If a model has a declared equivalence relation \(\sim\) on \(\Omega_{\mathcal P}\), its reduced configuration space may be written

\[
\widehat\Omega_{\mathcal P}=\Omega_{\mathcal P}/\sim.
\]

The equivalence relation must be justified. It could encode a gauge redundancy, a coordinate relabeling, or another proven representational redundancy. It must not be introduced merely to make the model simpler.

This distinction matters because a count of mathematical configurations is not necessarily a count of physically distinct possibilities.

## 6. Actualization and evolution

An actualization rule selects or generates a realized state from admissible configurations. In a deterministic model, one possible structure is a map

\[
\mathcal A_\lambda:
\Omega_{\mathcal P}\times\mathcal B
\longrightarrow\Omega_{\mathcal P},
\]

where \(\mathcal B\) is a declared set of boundary conditions, controls, or contextual inputs and \(\lambda\) is an evolution parameter. For a continuous deterministic flow, the family must satisfy appropriate composition and regularity properties, such as

\[
\mathcal A_{0}(q)=q,\qquad
\mathcal A_{\lambda_2}\!\left(
\mathcal A_{\lambda_1}(q)\right)
=\mathcal A_{\lambda_1+\lambda_2}(q),
\]

when a time-homogeneous flow is intended.

A stochastic model instead requires a transition kernel

\[
K_\lambda(q,B),
\]

giving the probability of transition from state \(q\) into a measurable subset \(B\subseteq\Omega_{\mathcal P}\). The probability measure, normalization, and empirical interpretation must be specified.

These are alternative mathematical possibilities, not claims that UPT has already chosen deterministic or stochastic actualization. The model must also establish that its evolution preserves admissibility:

\[
q\in\Omega_{\mathcal P}
\;\Longrightarrow\;
\mathcal A_\lambda(q)\in\Omega_{\mathcal P},
\]

or state precisely when and why this condition is relaxed.

## 7. Observables and experience

A physical theory must connect its mathematical states to measurable quantities. Let

\[
\mathcal O: \Omega_{\mathcal P}\to\mathcal Y
\]

map model configurations to an observable space \(\mathcal Y\). For stochastic theories, observables may instead be random variables or probability distributions.

The UPT component \(\mathcal X\), previously used for experience, observation, or recorded outcomes, belongs at this interface. Human experience may motivate questions about measurement and interpretation, but it must not be silently equated with a physical measurement operator. A scientific model must state which records are instrumentally measurable and how predictions are compared with them.

## 8. Relation to the UPT sequence

| UPT concept | Configuration-space interpretation | What remains to be specified |
|---|---|---|
| Potential | \(\Omega_{\mathcal P}\), the admissible possibilities of a model | Why this domain is fundamental and how it is selected |
| One | A common structure containing all declared degrees of freedom | A precise unity principle or invariant |
| Both | Distinguishable components or sectors | Their operational definition |
| Many | Multiple components and their relational network | Couplings, topology, and scaling behavior |
| All | The full domain of the model | Whether the model is complete for its intended scope |
| Becoming | A trajectory or transition process in the domain | Equations, initial/boundary data, and well-posedness |
| Renewed Potential | New admissible possibilities after evolution or interaction | A defined mechanism that changes the configuration space |

The sequence is an organizing hypothesis. The table does not establish that these stages occur as a universal physical chronology.

## 9. Connection to existing OTFT and cosmological work

The existing OTFT and FLRW experiments specify particular state variables, equations, parameters, and numerical procedures. Their state spaces are examples of model configuration spaces. They do not yet derive the full UPT admissibility domain from first principles.

In the Experiment 14 cosmological model, the scalar variables \(\phi\) and \(T\), together with the scale factor and expansion variables, define a restricted dynamical state description. Its scalar potential-energy function is a model-specific term. In particular, the clock-labelled scalar \(T\) is a matter field evolved with respect to FLRW coordinate time; it is not thereby ontological Potential or proper time.

To claim a genuinely UPT-derived physical model, a later study must derive—not simply name—the relevant state space, constraints, action or transition law, symmetries, conservation laws, and observable predictions.

## 10. Minimum mathematical and scientific obligations

Any concrete UPT realization must answer the following:

1. **Domain:** What are the degrees of freedom, and what is the precise set \(\Omega\)?
2. **Admissibility:** Which constraints define \(\Omega_{\mathcal P}\), and why?
3. **Structure:** What topology, measure, differentiable structure, or inner product is required?
4. **Relations:** Which relations are primitive, and which are derived?
5. **Redundancy:** Which configurations are physically equivalent, and what justifies the quotient?
6. **Dynamics:** What determines the transition or evolution rule?
7. **Consistency:** Is the evolution well-posed and does it preserve the constraints?
8. **Physics:** Are units, symmetries, conservation laws, and limiting cases correct?
9. **Observation:** What measurable quantities distinguish the model from established alternatives?
10. **Refutation:** What result would count against the proposed physical realization?

Until these questions are answered for a specified model, UPT remains a conceptual and mathematical research framework rather than a validated fundamental physical theory.

## 11. Proposed next experiments

- **UPT-3 — Relational structure:** choose a minimal model with two or more distinguishable degrees of freedom and define its relations without assuming a preferred physical interpretation.
- **UPT-4 — Admissibility preservation:** prove or numerically test whether a proposed evolution law preserves the declared constraints.
- **UPT-5 — Observable consequences:** identify a prediction that differs from a baseline model and design a reproducible comparison.

## 12. Conclusion

The configuration-space formalization gives UPT a disciplined mathematical bridge between the idea of Potential and concrete models. It defines a model's admissible possibilities, distinguishes those possibilities from energy and realized states, and identifies the mathematical structures required for relations, actualization, and observation.

The central proposition—**the Potential precedes the One**—remains the guiding ontological hypothesis. Its physical significance will depend on whether a concrete realization can produce internally consistent mathematics and distinct, testable predictions.

---
**Attribution:** Pablo Salvador Cardenas.  
**Research status:** Version 0.1; proposed formalization, awaiting independent mathematical and physical review.
