# Dimensional Analysis and Symmetry — Draft 0.1

## 1. Purpose and status

This note supplies a consistent route from the dimensionless variational prototype to a model that could, after further physical specification, carry units. It also separates symmetries of the chosen functional from conservation laws of its particular gradient-flow dynamics.

Nothing here assigns measured values to the parameters or establishes that the functional describes a physical field. The current implementation remains dimensionless.

## 2. Reference-scale convention

Let the dimensionless variables used by `VariationalFieldSystem` be

    x_bar = x / X0
    T_bar = T / Q0
    tau   = t / t0

where X0 and Q0 are nonzero reference scales for the scalar and tensor-component states, and t0 is a reference time. Phase `theta` is an angle and is dimensionless in SI dimensional analysis (radians are a named dimensionless unit). Assume graph weights W_ij are dimensionless.

Choose an energy scale E0 and define a candidate physical energy by

    E(x, theta, T) = E0 * V(x_bar, theta, T_bar).

This is a scaling convention, not evidence that V is physical energy. It becomes a physical energy only if x, theta, T, and the functional are tied to measurable quantities and justified dynamics.

Under this convention, every coefficient appearing inside the implemented dimensionless V (m_s, m_t, g_s, g_t, g_h, lambda_s, lambda_t) is dimensionless. If a future formulation uses dimensional state variables directly, the coefficients must instead carry the units required to make every term in E have units of energy.

## 3. Mobility units and normalized equations

Consider physical overdamped gradient flow:

    dx/dt       = -Gamma_x * partial(E)/partial(x)
    dtheta/dt   = -Gamma_h * partial(E)/partial(theta)
    dT/dt       = -Gamma_T * partial(E)/partial(T)

For E measured in joules, time in seconds, and state units [x]=U_x and [T]=U_T, the mobilities have units

    [Gamma_x] = U_x^2 / (J s)
    [Gamma_h] = 1 / (J s)
    [Gamma_T] = U_T^2 / (J s)

Substitution of the reference scales gives the dimensionless mobilities used by the code:

    mu_x = Gamma_x * E0 * t0 / X0^2
    mu_h = Gamma_h * E0 * t0
    mu_T = Gamma_T * E0 * t0 / Q0^2

Each mu is dimensionless. The code's time step dt is therefore measured in units of tau, not seconds. The optional natural frequency must likewise be dimensionless in the implementation:

    omega_bar = omega_physical * t0

A physical parameter set must publish E0, t0, X0, Q0, the corresponding mobilities, and the mapping from model states to observables. Without those declarations, numerical coefficients are only dimensionless controls.

## 4. Dimensional audit checklist

Before interpreting a simulation physically, record:

| Quantity | Required declaration |
|---|---|
| Scalar state x | Observable or latent quantity; unit U_x; reference X0 |
| Tensor-array state T | Component meaning and unit U_T; reference Q0 |
| Phase theta | Meaning of phase and reference convention |
| Time | Physical time mapping t=t0*tau |
| Potential V | Dimensionless functional; physical energy scale E0 only if justified |
| Graph W | Meaning, normalization, and whether weights are dimensionless |
| Mobilities | Physical units and dimensionless conversion to mu |
| Natural frequency | rad/s physically; omega_bar=omega*t0 in code |
| Couplings | Units or dimensionless status derived from the exact term |
| Observables | Explicit measurement procedure and uncertainty |

The tensor array is still not a geometric tensor. A physical tensor theory also needs transformation rules, index conventions, a metric where relevant, and appropriate derivatives.

## 5. Symmetries and what they imply

### 5.1 Global phase-shift symmetry

The functional depends on phase differences through cos(theta_i-theta_j). Therefore it is invariant under

    theta_i -> theta_i + c   for every node i.

For the undriven gradient-flow equation with one common phase mobility,

    dtheta_i/dtau = -mu_h * partial(V)/partial(theta_i),

pairwise antisymmetry gives

    sum_i partial(V)/partial(theta_i) = 0
    d/dtau sum_i theta_i = 0.

Thus the sum of *unwrapped* phases is constant in the undriven model. The implementation stores phases modulo 2*pi, so the raw sum of wrapped values can jump at the branch cut; conservation should be checked using unwrapped phases or circular quantities. With natural-frequency forcing,

    d/dtau sum_i theta_i = sum_i omega_bar_i,

so the unwrapped phase sum is constant only when the total drive is zero. This is a property of this gradient-flow equation, not a Hamiltonian Noether momentum claim.

### 5.2 Scalar translation symmetry and mean

If scalar_mass is zero, the functional is unchanged by a common shift

    x_i -> x_i + c.

The pairwise scalar differences cancel in the summed gradient, so

    d/dtau sum_i x_i = 0.

If scalar_mass is nonzero, the local quadratic term breaks this symmetry and

    d/dtau sum_i x_i = -mu_x * scalar_mass * sum_i x_i.

A nonzero scalar mean then decays according to the mass term. There is no scalar source in this variational prototype.

### 5.3 Tensor-component translation symmetry and means

If tensor_mass is zero, adding the same constant to a given tensor-array component at every node leaves all pairwise tensor differences unchanged. Each component's node-sum is therefore conserved by the undriven gradient flow. A nonzero tensor_mass breaks these independent component-wise shift symmetries and damps the corresponding means.

This statement concerns the implemented component array, not a covariant tensor conservation law.

## 6. Symmetry is not the same as physical conservation

The phase-shift invariance is a symmetry of V. In a Hamiltonian field theory, Noether's theorem connects continuous symmetries of an action to conserved charges under its assumptions. The present prototype is instead a dissipative, first-order gradient flow. Its mean-phase result follows directly by summing the implemented equations; it should not be advertised as a general Noether charge.

Likewise, scalar and tensor-component means are conserved only in the zero-mass, source-free limits described above. The functional V itself is non-increasing in exact undriven gradient flow:

    dV/dtau = -mu_x*||grad_x V||^2
              -mu_h*||grad_theta V||^2
              -mu_T*||grad_T V||^2 <= 0.

This is a Lyapunov/dissipation statement. It is not conservation of V. With explicit Euler, monotonic decrease is only expected within a suitable step-size regime and must be checked by refinement.

## 7. Minimum validation programme

1. Verify the three analytical gradient blocks against finite differences.
2. For zero scalar mass, test scalar-sum conservation over many steps while reducing dt.
3. For zero tensor mass, test each component sum in the same way.
4. Track unwrapped phase sum with no natural frequencies; separately test nonzero drives with predicted drift sum(omega_bar)*tau.
5. Test the corresponding symmetry-breaking decay when scalar_mass or tensor_mass is positive.
6. Compare V(tau) at dt, dt/2, and dt/4; do not infer continuous-time monotonicity from one coarse run.
7. Repeat with graph sizes and topologies varied, and report numerical tolerances.

## 8. Research boundary and next physical requirements

This analysis makes the mathematical prototype more explicit, but it does not select a unique physical meaning for x, T, theta, W, or E0. A physical theory still needs:
- operational definitions of its state variables and measurable observables;
- transformation behavior under coordinate changes and relevant gauge symmetries;
- a justified action, energy, or constitutive principle for the proposed dynamics;
- recovery of established results in tested regimes;
- quantitative predictions that differ from standard models;
- comparison with data, including parameter uncertainty and model-selection criteria.

The guiding OTFT proposition, **“All Fields Lead to One,”** can remain the research motivation. The mathematical claim currently supported is narrower: distinct state domains can be coupled through one specified dimensionless functional on a shared graph.
