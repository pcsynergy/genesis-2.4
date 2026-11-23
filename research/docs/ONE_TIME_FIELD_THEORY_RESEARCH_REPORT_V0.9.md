# One Time Field Theory: Numerical Cosmological Evolution of a Coupled Scalar–Clock Field Model

**Research paper — Experiment 14**  
**Author:** Pablo Salvador Cardenas  
**Project:** GENESIS 2.4 — One Time Field Foundation  
**Research branch:** `research/one-time-field-foundation`  
**Date:** 23 November 2026  
**Version:** 0.9  
**Article type:** Computational/theoretical methods paper  
**Review status:** Submitted as a reproducible research report; independent peer review has not yet occurred.

## Abstract

This paper reports Experiment 14 in the One Time Field Theory (OTFT) research program: a numerical evolution of an interacting two-scalar matter sector coupled to standard Einstein gravity in a spatially flat, homogeneous and isotropic FLRW spacetime. Previous stages derived the curved-background scalar equations and the corresponding Friedmann and acceleration equations. The present stage integrates the scale factor, Hubble parameter, scalar field, and a second scalar denoted (T), while monitoring the Friedmann constraint as an independent numerical diagnostic. A fixed-step fourth-order Runge–Kutta (RK4) solver is implemented without adding external numerical dependencies. Initial expansion or contraction rates are selected from the Friedmann constraint; thereafter the Hubble parameter is integrated using the acceleration equation, rather than reconstructed algebraically at every step. Automated tests cover initial constraint satisfaction, positive scale factor, expansion and contraction branches, evolution of the Hubble parameter, an uncoupled control, input validation, and reduction of constraint drift under timestep refinement. The experiment supports the limited finding that the specified homogeneous classical equations can be evolved together in the tested parameter regime with numerical behavior consistent with the continuum constraint-propagation identity. It does not establish that (T) is physical time, introduce a novel gravity law, validate OTFT empirically, or demonstrate superiority to (Lambda)CDM. The report provides equations, method, reproducibility instructions, interpretation, limitations, and a peer-review agenda.

**Keywords:** One Time Field Theory; scalar field; FLRW cosmology; Einstein equations; Friedmann constraint; Runge–Kutta; numerical relativity; clock field; constraint propagation.

## 1. Introduction

The central research question motivating OTFT is whether temporal behavior can be described through field relationships and interactions, rather than treated only as an external parameter in a model. The earlier numerical experiments explored candidate field-derived activity measures, relational clock parameterizations, and a dynamical scalar variable labelled (T). Those preliminary models were useful for defining hypotheses and testing mathematical constructions, but they did not by themselves constitute a relativistic cosmological theory.

The research sequence therefore moved through several necessary stages. A two-scalar action was first examined in flat spacetime, then extended to a spatially flat FLRW background. Metric variation was subsequently introduced through the conventional Einstein–Hilbert action. Experiment 13 established the homogeneous gravitational equations and showed analytically how the Friedmann constraint propagates when the matter equations and continuity equation hold. However, those equation-level checks did not yet demonstrate a complete numerical trajectory in which the geometry and matter fields evolve together.

Experiment 14 addresses that gap. Its purpose is not to claim a discovery from a numerical integration. Rather, it turns the selected equations into a reproducible initial-value problem and makes the numerical constraint error visible. This is a foundational computational requirement before perturbation theory, matter-sector extensions, or observational comparisons can be responsibly attempted.

## 2. Covariant model and assumptions

We work in natural units with metric signature ((-+++)) and a spatially flat FLRW line element,
[
ds^2=-dt^2+a(t)^2(dx^2+dy^2+dz^2),qquad H(t)=rac{dot a}{a}.
]
The matter Lagrangian is
[
mathcal L_m=-rac12g^{mu
u}partial_muphipartial_
uphi
-rac12m^2phi^2
-rac{Z_T}{2}g^{mu
u}partial_mu Tpartial_
u T
-rac{mu_T^2}{2}T^2+g_cT f(phi),
]
where the bounded interaction inherited from earlier experiments is
[
f(phi)=rac12rac{phi^2}{1+phi^2},qquad
f'(phi)=rac{phi}{(1+phi^2)^2}.
]
The gravitational sector is the standard Einstein–Hilbert term:
[
S=int d^4xsqrt{-g}left[rac{M_{m Pl}^2}{2}R+mathcal L_might],
qquad M_{m Pl}^2=(8pi G)^{-1}>0.
]
No new curvature coupling, modified Einstein tensor, or higher-derivative gravitational term is postulated here. The model is therefore general relativity with a particular interacting scalar matter ansatz.

For homogeneous fields, the matter equations are
[
ddotphi+3Hdotphi+m^2phi-g_cT f'(phi)=0,
]
[
Z_T(ddot T+3Hdot T)+mu_T^2T-g_cf(phi)=0.
]
The energy density and isotropic pressure are
[
ho=rac12dotphi^2+rac{Z_T}{2}dot T^2+
rac12m^2phi^2+rac{mu_T^2}{2}T^2-g_cTf(phi),
]
[
p=rac12dotphi^2+rac{Z_T}{2}dot T^2-
rac12m^2phi^2-rac{mu_T^2}{2}T^2+g_cTf(phi).
]
The homogeneous Einstein equations become
[
3M_{m Pl}^2H^2=ho,qquad
-2M_{m Pl}^2dot H=ho+p,qquad
dot a=aH.
]
On solutions of the scalar equations, covariant stress-energy conservation gives
[
dotho+3H(ho+p)=0.
]
Defining the Friedmann constraint as
[
C(t)=3M_{m Pl}^2H(t)^2-ho(t),
]
one obtains
[
dot C=6M_{m Pl}^2Hdot H-dotho=0
]
when the acceleration equation and continuity equation are both satisfied. Thus, an initially satisfied constraint remains satisfied in the exact continuum system.

## 3. Initial-value formulation and numerical method

The numerical state is
[
y(t)=(a,H,phi,dotphi,T,dot T).
]
At the initial time, field values and velocities determine (ho_0). For a spatially flat solution with real (H_0) and positive (M_{m Pl}^2), the initial density must be nonnegative. The initial Hubble value is then selected as
[
H_0=+sqrt{rac{ho_0}{3M_{m Pl}^2}}
]
for the expanding branch, or the negative root for the contracting branch. The scale factor is required to be positive.

The solver advances the six state variables with a fixed-step classical fourth-order Runge–Kutta method. At each intermediate stage it evaluates the scalar equations and the acceleration equation,
[
dot H=-rac{ho+p}{2M_{m Pl}^2}.
]
Crucially, (H) is an independently integrated state variable. The implementation does not force the Friedmann relation to hold by recomputing (H) from (ho) after every step. If it did, a constraint residual calculated from the same reconstructed value would be zero by construction and would provide no meaningful diagnostic of integration error. Independent evolution permits the residual (C(t)) to measure the extent to which the numerical trajectory departs from the continuum constraint surface.

The implementation uses a self-contained RK4 routine to keep the research layer lightweight and reproducible. It validates finite initial data, positive (M_{m Pl}^2), positive initial scale factor, positive integration duration, and a positive integer step count. It rejects a negative initial energy density because it cannot produce a real initial Hubble value under the stated flat-FLRW constraint. During integration, nonpositive scale factor or negative density is treated as an invalid trajectory for this solver and reported as an error rather than silently continued.

## 4. Demonstration parameters and verification design

The reproducible example uses
[
m=0.7,quad Z_T=1.0,quad mu_T^2=0.5,quad
g_c=0.02,quad M_{m Pl}^2=1,
]
with
[
a_0=1,quad phi_0=0.2,quad T_0=0.1,quad
dotphi_0=dot T_0=0.
]
These are illustrative dimensionless values in the chosen natural-unit convention. They are not estimates derived from the cosmic microwave background, supernovae, baryon acoustic oscillations, or any other observational data. The default demonstration integrates to a finite final time with 2,000 equal RK4 steps and records every state sample.

The automated verification protocol includes the following checks:

1. **Initial constraint:** the initial Friedmann residual is zero within floating-point tolerance because the initial Hubble value is initialized from the constraint.
2. **Scale-factor admissibility:** the scale factor remains positive throughout the tested demonstration interval.
3. **Expanding branch:** for the selected positive-root initial condition, the scale factor grows over the tested interval.
4. **Dynamical Hubble parameter:** (H) changes as dictated by the acceleration equation rather than remaining fixed.
5. **Timestep refinement:** doubling the number of steps reduces the terminal absolute Friedmann residual for the chosen smooth trajectory.
6. **Uncoupled control:** the system remains numerically evolvable when (g_c=0), providing a control in which the two scalar sectors no longer exchange energy through the interaction term.
7. **Contracting branch and input checks:** the negative-root branch contracts over the selected short interval, while invalid scale factors, durations, and step counts are rejected.

The tests are designed to establish behavior of the equations as implemented. They are not an exhaustive proof of global existence, stability, or accuracy for every allowed parameter combination. In particular, a finite number of successful steps cannot establish long-time stability or robustness near singular boundaries.

## 5. Findings

The experiment demonstrates a reproducible numerical path from the coupled scalar equations and standard FLRW Einstein equations to a time series for the geometry and matter fields. The initial state is placed on the Friedmann constraint surface, and the Hubble parameter is then advanced independently through the acceleration equation. The output records the scale factor, Hubble parameter, both field values and velocities, density, pressure, and Friedmann residual. This provides a direct diagnostic of both the physical variables in the ansatz and the numerical consistency of the integration.

The refinement test is an essential part of the finding. Exact continuum equations propagate the constraint, but a finite-step explicit numerical method generally introduces truncation error. It would therefore be inappropriate to demand that the Friedmann residual remain identically zero at every RK4 sample. The meaningful criterion used here is that the residual remains finite over the tested interval and decreases as the step size is reduced. The tests encode this convergence criterion for the selected demonstration case. The dedicated example prints the maximum absolute residual and final state so that the numerical values can be independently reproduced from the repository.

The uncoupled control is also important for interpretation. A working (g_c=0) run confirms that the numerical machinery is not dependent on a nonzero interaction to function. It does not, however, show that the coupling is necessary in nature or that it creates a unique observable effect. Likewise, the expanding and contracting branches show that the sign choice in the initial Friedmann root is handled consistently over the selected short intervals; they do not constitute a model of a cosmic bounce or a complete cyclic cosmology.

The principal result is therefore methodological: the homogeneous two-scalar matter model can be integrated together with the standard FLRW gravitational equations in the tested region, and the independent Friedmann residual provides a useful numerical consistency monitor. This closes the equation-to-trajectory stage of the current research sequence.

## 6. Discussion: what the result means for OTFT

The symbol (T) is called a clock field in the research program because it is intended to explore possible relationships between field dynamics and temporal description. In the action used here, however, (T) is mathematically a real scalar matter field. It evolves with respect to the FLRW coordinate (t), has a kinetic term and potential, and contributes to the stress-energy tensor. The equations do not identify it with proper time, do not show that clocks measure its value, and do not establish that it replaces or generates the spacetime time coordinate.

A physical temporal interpretation would require an operational prescription. For example, the theory would need to specify what observable couples to (T), how a local clock would measure that observable, how the result transforms between observers, and what prediction differs from standard scalar-field cosmology. It would also need to address whether (T) is gauge-dependent or physically distinguishable from an ordinary scalar degree of freedom. Without those steps, the clock interpretation remains a research hypothesis rather than an established physical conclusion.

The calculation also does not provide a new theory of gravity. The gravitational equations are those of general relativity. The two-scalar sector is a chosen matter model minimally coupled to the metric. A claim of a new gravitational effect would require a modified action or a distinct, testable consequence that cannot be absorbed into conventional matter dynamics. No such consequence is demonstrated in Experiment 14.

## 7. Limitations and unresolved questions

The model is restricted to a homogeneous, isotropic, spatially flat background. It contains no explicit baryon, photon, neutrino, radiation, or cold-dark-matter fluid. It has no spatial perturbations, anisotropic stress, primordial fluctuation spectrum, transfer functions, or structure-growth calculation. Consequently, it cannot yet be compared meaningfully with the full set of precision cosmological observations. No fit to (Lambda)CDM parameters has been performed, and no likelihood analysis, posterior distribution, uncertainty budget, or model-selection statistic is reported.

The numerical method is fixed-step explicit RK4. This is transparent and adequate for the demonstration, but it is not necessarily efficient or reliable in stiff regimes, over very long intervals, or near boundaries where the density approaches zero. Adaptive integration, independent solver cross-checks, convergence-order measurements, and error-budget reporting should precede any high-precision application. The current tests check that refinement reduces a selected residual; they do not establish fourth-order convergence across all observables or all parameter choices.

The positivity of (Z_T) is required by the parameter definition to avoid a wrong-sign kinetic contribution in this elementary model. Nevertheless, a positive homogeneous kinetic coefficient is not a full stability proof. Perturbations around the background may reveal gradient instabilities, tachyonic modes, strong coupling, or other pathologies. A dedicated perturbative analysis is needed before interpreting the background as a viable cosmology.

Finally, all demonstration parameters are illustrative. Their dimensions and normalization must be fully specified before comparison with measured quantities. The model has not been calibrated to a physical energy scale or connected to a complete standard cosmological matter inventory.

## 8. Reproducibility and repository implementation

Experiment 14 is isolated in the research layer and does not modify the legacy GENESIS 2.4 C simulator. The relevant files are:

- `research/one_time_field/cosmological_evolution.py` — coupled RK4 integrator and trajectory diagnostics.
- `research/tests/test_cosmological_evolution.py` — automated verification suite.
- `research/examples/cosmological_evolution_experiment.py` — reproducible demonstration runner.
- `research/docs/COSMOLOGICAL_EVOLUTION_EXPERIMENT.md` — experiment protocol and detailed limitations.

From the repository root, run:

```bash
python -m unittest research.tests.test_cosmological_evolution -v
python research/examples/cosmological_evolution_experiment.py
python -m unittest discover -s research/tests -v
```

The research workflow also runs the full suite across Python 3.10, 3.11, and 3.12. A successful workflow confirms that the committed code passes those automated tests in the configured environments; it does not constitute independent peer review or physical validation.

## 9. Conclusion and peer-review recommendations

Experiment 14 provides a tested computational implementation of homogeneous FLRW evolution for the selected interacting scalar–clock matter ansatz. It initializes the Friedmann constraint, integrates the Hubble parameter independently through the acceleration equation, evolves the scale factor and scalar fields, and monitors numerical constraint drift. The tests address the expanding and contracting branches, an uncoupled control, admissibility conditions, and improvement under timestep refinement.

The appropriate conclusion is deliberately bounded. The experiment establishes a numerical consistency result for a specified classical model and tested parameter regime. It does not establish that the clock field is physical time, that OTFT is empirically correct, that the model modifies gravity, or that it improves on (Lambda)CDM. These are separate hypotheses requiring additional mathematical and observational evidence.

For peer review, the next steps should be: (1) independently reproduce the trajectories and residuals; (2) compare RK4 against an adaptive high-accuracy solver; (3) quantify convergence order and global error; (4) derive and analyze linear scalar and metric perturbations; (5) establish ghost, gradient, and tachyonic stability conditions; (6) add standard radiation and matter sectors; and (7) define in advance a falsifiable observable and compare the model statistically against a baseline cosmology. Only after these stages would a claim of empirical relevance be justified.

**Final finding:** the current homogeneous OTFT-inspired two-scalar model is numerically evolvable and constraint-consistent to the tested discretization accuracy. This is a foundation for further research, not a confirmation of a new physical theory.
