# Experiment 10 — stress-energy tensor and conservation

**Status:** Analytical derivation with executable algebraic tests.  
**Scope:** Classical two-scalar field theory on fixed 1+1-dimensional Minkowski spacetime, signature ((- ,+)).

## 1. Symmetric stress-energy tensor

Starting from the Lorentz-covariant Lagrangian of Experiment 9, translation invariance gives the canonical tensor. Because the fields are scalars and the Lagrangian depends on their derivatives only through Lorentz contractions, the resulting tensor is already symmetric:

[
T^{mu
u}=
partial^muphi,partial^
uphi
+Z_Tpartial^mu T,partial^
u T
+eta^{mu
u}mathcal L.
]

For (eta_{mu
u}=mathrm{diag}(-1,+1)), the components are

[
T^{00}=dotphi^2+Z_Tdot T^2-mathcal L,
]

[
T^{01}=T^{10}=-dotphi,phi_x-Z_Tdot T,T_x,
]

[
T^{11}=phi_x^2+Z_T T_x^2+mathcal L.
]

The energy density (T^{00}) agrees with the Hamiltonian density.

## 2. Conservation identity

Let the Euler–Lagrange residuals be

[
R_phi=Boxphi-m^2phi+gT f'(phi),
qquad
R_T=Z_TBox T-mu_T^2T+g f(phi).
]

Direct differentiation of the stress-energy tensor gives the off-shell identity

[
partial_mu T^{mu
u}
=R_phi,partial^
uphi+R_T,partial^
u T.
]

Therefore, when both field equations hold ((R_phi=R_T=0)),

[
oxed{partial_mu T^{mu
u}=0.}
]

This is local energy-momentum conservation in flat spacetime. It follows from spacetime-translation invariance of the action; it is not an independent empirical prediction of the chosen coupling.

## 3. Executable checks

The Experiment 10 test suite checks:
- symmetry (T^{01}=T^{10});
- agreement of (T^{00}) with the Hamiltonian density;
- zero divergence for derivatives satisfying the field equations;
- the off-shell divergence identity for arbitrary test derivatives.

The checks are algebraic pointwise tests of the continuum equations, not a lattice evolution or experimental measurement.

## 4. Interpretation and limits

The result supplies the expected Noether conservation law for the covariant two-scalar model on a fixed Minkowski background. It does not imply that the clock scalar is physical time. It also does not establish gravitational dynamics: there is no dynamical metric or Einstein equation in this model.

The next major step would be a 3+1-dimensional formulation and then a carefully defined curved-background extension. Coupling to a dynamical metric would require varying a generally covariant action with respect to that metric and checking the corresponding covariant conservation identity.

