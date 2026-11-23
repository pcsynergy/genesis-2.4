# Experiment 9 — Lorentz-covariant scalar and clock fields

**Status:** Analytical ansatz with executable 1+1-dimensional symmetry tests.  
**Scope:** Classical fields on fixed flat Minkowski spacetime. This is not a theory of dynamical gravity and does not establish that the clock field is physical time.

## 1. Covariant setup

Use coordinates (x^mu=(ct,x)) and metric signature ((- ,+)) in 1+1 dimensions. For compact numerical tests set (c=1). Both (phi(x^mu)) and (T(x^mu)) are postulated to be real Lorentz-scalar fields. The same Minkowski metric and light cone govern both fields.

The action is

[
S=int d^2x,mathcal L,
]

[
mathcal L=
-rac12partial_muphi,partial^muphi
-rac12m^2phi^2
-rac{Z_T}{2}partial_mu T,partial^mu T
-rac{mu_T^2}{2}T^2
+gT f(phi),
]

[
f(phi)=rac12rac{phi^2}{1+phi^2}.
]

Here (Z_T>0), (m^2ge0), and (mu_T^2>0). The interaction (T f(phi)) is a Lorentz scalar because it is built from scalar fields without preferred vectors or frame-dependent derivatives.

## 2. Euler–Lagrange equations

With (Box=partial_mupartial^mu=-partial_t^2+partial_x^2),

[
Boxphi-m^2phi+gT f'(phi)=0,
qquad
f'(phi)=rac{phi}{(1+phi^2)^2},
]

[
Z_TBox T-mu_T^2T+g f(phi)=0.
]

Equivalently,

[
partial_t^2phi=partial_x^2phi-m^2phi+
gTrac{phi}{(1+phi^2)^2},
]

[
partial_t^2T=partial_x^2T-
rac{mu_T^2}{Z_T}T+rac{g}{Z_T}f(phi).
]

Unlike Experiment 8, this formulation does not assign independent propagation speeds to the two fields. Their principal wave operators share the same Minkowski light cone. A model with distinct characteristic speeds in a preferred frame would not satisfy this Lorentz-invariance test.

## 3. What is tested

The executable tests check:

1. Invariance of each Minkowski gradient contraction under boosts.
2. Invariance of the complete Lagrangian density when scalar field values are unchanged and their derivative components are transformed.
3. Invariance of the d'Alembertian under boosts, including mixed second derivatives.
4. Frame-independence of the Euler–Lagrange residuals.
5. Rejection of non-subluminal boost parameters.

The tests use several positive and negative boost velocities and compare floating-point results to tight numerical tolerance. These are algebraic symmetry checks of the stated 1+1-dimensional ansatz, not numerical evolution of a full field solution.

## 4. Stability and interpretation

The potential energy density is

[
V(phi,T)=rac12m^2phi^2+rac12mu_T^2T^2-gT f(phi).
]

Completing the square in (T),

[
V=rac12mu_T^2left(T-rac{g f(phi)}{mu_T^2}ight)^2
+rac12m^2phi^2-rac{g^2 f(phi)^2}{2mu_T^2}.
]

Since (0le f(phi)<1/2), the last negative term is bounded below. For (m^2ge0) and (mu_T^2>0), this potential is bounded below. This elementary boundedness check does not replace a full perturbative stability analysis or quantum stability analysis.

The model is a Lorentz-covariant two-scalar field theory on a fixed flat background, provided the fields transform as scalars and the parameters are constants. It contains no Einstein–Hilbert term and no dynamical metric. It therefore does not yet describe gravitation or general covariance in curved spacetime. Nor does covariance identify (T) with elapsed proper time: (T(x)) is a scalar field coordinate in this ansatz.

## 5. Limitations and next tests

- The implemented test is 1+1-dimensional Minkowski space; extension to 3+1 dimensions is structurally direct but should receive independent tests.
- No curved-spacetime coupling, stress-energy backreaction, gauge fields, quantization, or empirical calibration is included.
- Dimensional units must be assigned before interpreting (m,mu_T,Z_T,g,phi,T) as physical parameters.
- A next stage should derive the symmetric stress-energy tensor, verify its conservation on shell, and test well-posed evolution and perturbative stability.

**Conclusion:** Passing Experiment 9 means the proposed two-scalar action and its Euler–Lagrange equations respect Lorentz boosts in the tested 1+1-dimensional setting. It does not establish a physical time field or a unified theory.
