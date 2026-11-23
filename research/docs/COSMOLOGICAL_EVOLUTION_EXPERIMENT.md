# Experiment 14 — Numerical Cosmological Evolution of the Coupled Scalar–Clock Model

**Project:** GENESIS 2.4 — One Time Field Theory research foundation  
**Author:** Pablo Salvador Cardenas  
**Branch:** `research/one-time-field-foundation`  
**Status:** Reproducible numerical study of a classical homogeneous model; not observationally validated.

## 1. Objective and scope

Experiments 12 and 13 established the equations for two interacting scalar fields on a spatially flat Friedmann–Lemaître–Robertson–Walker (FLRW) spacetime and coupled that matter sector to the standard Einstein–Hilbert action. Experiment 14 advances from equation-level checks to an actual initial-value evolution. It numerically integrates the scale factor, Hubble parameter, scalar field, and clock-labelled scalar field as one coupled system.

The aim is narrow and testable: determine whether the selected homogeneous equations can be evolved together, whether the initial Friedmann constraint is respected to numerical precision, and whether constraint error decreases when the integration step is refined. This is a numerical consistency experiment. It is not a test of whether the clock field is physical time, a discovery of a new gravitational interaction, or a fit to the observed universe.

## 2. Model and conventions

We use natural units and metric signature ((-+++)), with spatially flat FLRW line element
[
ds^2=-dt^2+a(t)^2(dx^2+dy^2+dz^2),qquad H=dot a/a.
]
The matter Lagrangian density is
[
mathcal L_m=-rac12(
ablaphi)^2-rac12m^2phi^2
-rac{Z_T}{2}(
abla T)^2-rac{mu_T^2}{2}T^2
+g_cT f(phi),
]
where the bounded coupling function inherited from the preceding experiments is
[
f(phi)=rac12rac{phi^2}{1+phi^2},qquad
f'(phi)=rac{phi}{(1+phi^2)^2}.
]
The gravitational action is the conventional Einstein–Hilbert term,
[
S=int d^4xsqrt{-g}left[rac{M_{m Pl}^2}{2}R+mathcal L_might],
quad M_{m Pl}^2>0.
]
No modified-gravity term is introduced in this experiment.

For homogeneous fields, the Euler–Lagrange equations are
[
ddotphi+3Hdotphi+m^2phi-g_cT f'(phi)=0,
]
[
Z_T(ddot T+3Hdot T)+mu_T^2T-g_cf(phi)=0.
]
The scalar energy density and pressure are
[
ho=rac12dotphi^2+rac{Z_T}{2}dot T^2
+rac12m^2phi^2+rac{mu_T^2}{2}T^2-g_cTf(phi),
]
[
p=rac12dotphi^2+rac{Z_T}{2}dot T^2
-rac12m^2phi^2-rac{mu_T^2}{2}T^2+g_cTf(phi).
]
Einstein's equations reduce to
[
3M_{m Pl}^2H^2=ho,qquad
dot H=-rac{ho+p}{2M_{m Pl}^2},qquad
dot a=aH.
]
The continuity equation follows on shell:
[
dotho+3H(ho+p)=0.
]
Consequently, the Friedmann constraint
(C=3M_{m Pl}^2H^2-ho) is constant under the exact equations. The numerical solver integrates (H) using the acceleration equation rather than recomputing it from (ho) at every step. This deliberate choice makes constraint drift observable.

## 3. Numerical method

The implementation evolves the six-component state
[
y=(a,H,phi,dotphi,T,dot T).
]
The initial Hubble parameter is obtained from the Friedmann constraint,
[
H_0=pmsqrt{ho_0/(3M_{m Pl}^2)},
]
where the sign selects an expanding or contracting branch. The scale factor must be positive, the Planck-mass-squared parameter must be positive, and the initial energy density must be nonnegative. A negative density is rejected because a real spatially flat classical solution cannot satisfy the stated Friedmann constraint with real (H) and positive (M_{m Pl}^2).

A self-contained fixed-step, classical fourth-order Runge–Kutta (RK4) method is used. It avoids adding a numerical-library dependency and makes the integration protocol easy to reproduce. Each output sample records time, (a,H,phi,dotphi,T,dot T,ho,p), and the Friedmann residual. The default demonstration uses (m=0.7), (Z_T=1), (mu_T^2=0.5), (g_c=0.02), (M_{m Pl}^2=1), (a_0=1), (phi_0=0.2), (T_0=0.1), and vanishing initial field velocities. These are dimensionless demonstration values in the model's chosen natural-unit convention, not fitted cosmological parameters.

## 4. Verification protocol

The automated tests check seven properties: (i) the initial Friedmann residual vanishes to floating-point precision; (ii) the scale factor remains positive in the demonstration run; (iii) the expanding branch grows over the selected interval; (iv) the Hubble parameter changes under the acceleration equation; (v) the terminal constraint error decreases when the step count is doubled; (vi) the zero-coupling limit can be evolved; and (vii) the contracting branch and invalid-input guards behave as specified.

The timestep-refinement test is particularly important. RK4 does not preserve the Friedmann constraint exactly at finite step size, even though the continuum equations propagate it analytically. A nonzero discrete residual is therefore not, by itself, evidence of a physical inconsistency. The appropriate numerical check is that the error remains bounded over the stated interval and decreases under refinement. The experiment does not claim symplecticity or exact constraint preservation.

## 5. Results and interpretation

The code produces a reproducible trajectory for the two scalar degrees of freedom and the geometry. The initial data are constructed to satisfy the Friedmann constraint. The acceleration equation then determines the Hubble evolution independently, while the scalar equations exchange energy through the interaction potential. The test suite checks that the numerical constraint error decreases under a finer RK4 discretization. The dedicated runner prints the final state and the maximum absolute constraint residual so the reported values can be regenerated from the branch.

This outcome supports a limited conclusion: the selected homogeneous equations form a numerically integrable classical initial-value system for the tested parameter region and time interval, with constraint behavior consistent with the expected continuum identity. It does not establish that the coupling is realized in nature. In particular, the variable (T) is a scalar matter field in the action. It is not automatically proper time, a universal clock, or a replacement for the spacetime time coordinate. Its interpretation as a physical temporal degree of freedom would require an operational definition and an independently measurable observable.

Nor does this calculation distinguish the model from ordinary two-scalar cosmology. The gravitational sector is standard general relativity, and the clock-labelled scalar contributes to (ho) and (p) in the same formal manner as another scalar matter degree of freedom. A distinct physical claim would need to generate a clear prediction that differs from an appropriate baseline model, survive theoretical consistency checks, and be tested against data.

## 6. Limitations

The model is spatially homogeneous and isotropic. It contains no baryons, photons, neutrinos, cold dark matter fluid, radiation-era initial conditions, spatial curvature, anisotropic stress, or primordial perturbations. It does not calculate a CMB power spectrum, matter power spectrum, supernova distance relation, baryon acoustic oscillation observable, or gravitational-wave signal. It does not perform Bayesian parameter inference or compare likelihoods against (Lambda)CDM. No numerical values in the demonstration should be interpreted as estimates of measured quantities.

The implementation also uses a fixed-step explicit integrator. Stiff parameter regimes, long-duration evolution, transitions near (ho=0), and regions where the potential becomes problematic require separate analysis. The positivity of (Z_T) is enforced by the parameter class; this avoids a wrong-sign kinetic term in the tested matter sector but is not a complete perturbative stability analysis. A homogeneous background can be well behaved while inhomogeneous perturbations are unstable.

## 7. Reproducibility and repository artifacts

The experiment is implemented in:
- `research/one_time_field/cosmological_evolution.py` — RK4 evolution and diagnostics.
- `research/tests/test_cosmological_evolution.py` — initial constraint, expansion/contraction, coupling limit, refinement, and validation tests.
- `research/examples/cosmological_evolution_experiment.py` — reproducible demonstration runner.

Run from the repository root:
```bash
python -m unittest research.tests.test_cosmological_evolution -v
python research/examples/cosmological_evolution_experiment.py
python -m unittest discover -s research/tests -v
```

## 8. Peer-review assessment and next steps

**Finding:** Experiment 14 demonstrates a computationally reproducible homogeneous FLRW evolution for the chosen interacting two-scalar matter ansatz, with the Friedmann constraint imposed initially and its numerical drift tested under timestep refinement.

**What is established:** the equations implemented in the code are numerically evolved together for the stated sample parameters; the solver reports the constraint residual rather than concealing it; and tests cover expanding and contracting branches, an uncoupled control, and refinement behavior.

**What is not established:** a novel gravitational law, an empirically verified One Time Field Theory, a physical interpretation of (T) as time, a solution to the cosmological constant problem, or superiority to (Lambda)CDM.

The next defensible milestone is a perturbative stability and linear-response study around these backgrounds, followed—only if stable—by the inclusion of standard matter and radiation fluids and a comparison of derived observables with public cosmological data. Before any claim of empirical support, parameters, units, initial conditions, numerical tolerances, baseline models, and statistical criteria must be specified in advance.

**Conclusion:** Experiment 14 closes the equation-to-trajectory stage of the current homogeneous research sequence. It provides a tested numerical platform for more demanding work, while keeping the distinction between internal mathematical consistency and empirical physical validation explicit.
