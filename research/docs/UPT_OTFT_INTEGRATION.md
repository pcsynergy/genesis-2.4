# UPT–OTFT Integration: Mapping Unified Potential Theory onto the Research Models

**Author:** Pablo Salvador Cardenas  
**Version:** 0.1  
**Status:** Conceptual integration and model audit; no new physical law is asserted.

## 1. Purpose

This document connects Unified Potential Theory (UPT) to the One Time Field Theory (OTFT) research sequence and the GENESIS 2.4 research modules. UPT supplies the overarching conceptual architecture. OTFT investigates temporal ordering and change within that architecture. Existing numerical models remain specific mathematical systems whose validity is judged by their equations, tests, and empirical performance—not by the interpretation assigned to them.

## 2. Layered architecture

**Layer A — Ontological framework (UPT).** Defines Potential → One → Both → Many → All → Becoming → renewed Potential. It asks how possibility, distinction, relation, interaction, and actuality are connected.

**Layer B — Relational and field architecture (OntoField / network models).** Defines mathematical degrees of freedom, field configurations, network links, couplings, and geometric relations. Graphs, tensors, and fields are candidate representations, not interchangeable objects.

**Layer C — Dynamics and temporal description (OTFT / HCT / Harmonic Branching).** Specifies evolution equations, resonance, clock variables, temporal ordering, and alternative trajectories. Time may be treated as a coordinate, parameter, observable, or relational construction depending on the model. Those interpretations must not be conflated.

**Layer D — Physical realization and tests.** Supplies units, action principles, stress-energy, conservation laws, stability criteria, observable predictions, and comparison with measurements.

The layers are connected, but each has a distinct burden of proof. UPT provides a research ontology; it does not supply missing dynamical equations automatically.

## 3. Mapping the sequence onto the current codebase

| UPT concept | Operational interpretation in current research | Existing implementation |
|---|---|---|
| Potential | Space of admissible configurations and model functionals | unified action and continuum action; formalized in UPT specification |
| One | One shared state/action/network description | shared engine and unified action |
| Both | Distinguishable state sectors and pairwise relations | scalar, phase, tensor, and clock sectors; coupling terms |
| Many | Multiple interacting nodes, fields, or modes | network, harmonic, and tensor models |
| All | Full coupled model with boundary and conservation structure | shared action, stress-energy, and FLRW models |
| Interaction / actualization | Evolution law taking a state to another state | gradient flow, Hamiltonian, scalar-field equations |
| Becoming | Trajectory through configuration space | temporal and cosmological integrators |
| Renewed Potential | New accessible configurations after transitions | future research question; not yet implemented |

The table maps research roles. It does not claim that the software has realized the full ontology.

## 4. UPT and the current cosmological model

Experiments 12–14 use a conventional minimally coupled two-scalar matter model in general relativity. Its matter Lagrangian is
\[
\mathcal L_m=-\frac12(\nabla\phi)^2-\frac12m^2\phi^2
-\frac{Z_T}{2}(\nabla T)^2-\frac{\mu_T^2}{2}T^2+g_cT f(\phi),
\]
with
\[
f(\phi)=\frac12\frac{\phi^2}{1+\phi^2}.
\]
The corresponding model potential-energy function is
\[
V_{\rm model}(\phi,T)=\frac12m^2\phi^2+
\frac12\mu_T^2T^2-g_cT f(\phi).
\]

This \(V_{\rm model}\) is a specific energy function inside the action. It is **not** the full ontological Potential \(\mathcal P\) of UPT. The fields \(\phi\) and \(T\) are the model's actualized degrees of freedom; their coupling represents a relation/interaction; and their solutions are trajectories through the model's configuration space. The stress-energy tensor and Einstein equations describe how this particular matter sector sources the metric.

In this model, \(T\) remains a scalar field evolving with respect to FLRW coordinate time. It is not proper time, and it is not identified with foundational Potential. A future UPT-derived temporal model must define an operational clock observable and derive its relation to proper time.

## 5. What would count as a genuinely UPT-derived physical model?

A physical integration requires more than adding the label UPT to an existing Lagrangian. It must produce a precise mathematical consequence. A defensible sequence is:

1. Define a configuration space \(\Omega\) of allowed field/relational states.
2. Define a UPT potential structure over that space, distinguishing it from ordinary potential energy.
3. Specify how relations and interactions select or evolve configurations.
4. Derive an action or evolution law, including kinetic terms, couplings, and constraints.
5. Show that the theory recovers successful limits of established physics.
6. Derive a prediction that differs from the standard two-scalar GR model or another declared baseline.
7. Test stability, conservation, covariance, and numerical convergence.
8. Compare the prediction with an observational dataset using stated uncertainties and statistical criteria.

A proposed dependence of the action on a new UPT variable must be justified by symmetry and dimensional analysis. It cannot be inserted solely because it matches the conceptual sequence.

## 6. Two candidate hypotheses for potential and energy

UPT retains two explicit alternatives:

- **Potential-first hypothesis:** energetic quantities emerge after the potential domain, relations, and actualization law are specified.
- **Co-fundamental hypothesis:** potential and energy are inseparable aspects of a deeper relational structure; energy expresses measurable capacity for change.

The existing scalar-field model does not decide between these hypotheses. In that model, energy density is calculated from kinetic and potential-energy terms in the standard way. It is a model-level result, not an ontological proof.

## 7. Research consequences and next experiments

- **UPT-1: Formal ontology and category separation.** Freeze definitions of ontological Potential, model potential energy, actualized state, relation, interaction, and experience. This specification establishes the first draft.
- **UPT-2: Configuration-space model.** Define a concrete \(\Omega\), admissible transformations, and a potential structure without conflating it with a scalar energy function.
- **UPT-3: Derivation audit.** Determine whether a candidate action follows from declared principles, symmetries, and units rather than being chosen ad hoc.
- **UPT-4: Perturbative stability.** Analyze the existing two-scalar cosmological background before proposing new couplings.
- **UPT-5: Distinguishing prediction.** Only after stability and consistency are established, compare a UPT-derived model with its standard baseline.

## 8. Conclusion

UPT is the overarching conceptual framework; OTFT is a focused investigation of time, change, and relational ordering within it; and the existing GENESIS research modules are mathematical laboratories for particular representations of relations and dynamics.

The central ordering remains **Potential → One → Both → Many → All → Becoming → New Potential**. Its scientific development depends on translating each conceptual transition into explicit mathematical structures and, ultimately, testable predictions. This integration is substantive at the level of architecture and definitions while keeping existing numerical findings and their limitations intact.
