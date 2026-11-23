# Research Extensions — Draft 0.4

## 1. Conservation and dissipation

For the scalar baseline with symmetric adjacency W, graph Laplacian L=D-W, no source, and alpha=0:

    d(phi)/dt = -kappa*L*phi

Because rows and columns of L sum to zero, total state and mean are conserved in continuous time. The quadratic norm satisfies:

    d/dt (0.5*phi^T*phi) = -kappa*phi^T*L*phi <= 0

When alpha is positive, the sum is no longer conserved; the norm decreases through local decay and coupling. Explicit Euler introduces discretization error and can become unstable for an excessive time step.

## 2. Harmonic extension

PhaseOscillatorNetwork implements a finite graph Kuramoto-style phase model:

    d(theta_i)/dt = omega_i
        + K * sum_j W_ij*sin(theta_j-theta_i) / degree_i

Each node has phase theta_i and intrinsic angular frequency omega_i. The order parameter

    R = |(1/N) * sum_j exp(i*theta_j)|

measures phase coherence from 0 to 1. It is not an energy, and high coherence alone does not establish a physical resonance mechanism. The model uses explicit Euler and wraps phases to [0, 2*pi).

## 3. Tensor-state extension

TensorFieldNetwork associates a fixed-shape array with each graph node. Each component index a independently follows:

    d(phi_i[a])/dt = -alpha*phi_i[a]
        + kappa*sum_j W_ij*(phi_j[a]-phi_i[a])

This tests whether the scalar graph operator can be applied component-by-component to vector or rank-2 arrays.

Important limitation: an array with multiple components is not automatically a geometric tensor field. This prototype does not define coordinate transformations, tensor index variance, metrics, connections, covariant derivatives, or spacetime behavior. Those structures must be specified before physical tensor interpretation.

## 4. Testable milestones

1. Verify mean conservation for each component when alpha=0 and source=0.
2. Compare uncoupled scalar decay with the analytic exponential solution as dt decreases.
3. Verify identical phases remain identical for identical natural frequencies.
4. Measure phase coherence across graph structures and frequency distributions.
5. Verify component-wise tensor states reproduce independent scalar runs.
6. Introduce coordinate transformations only after precise tensor representations and transformation rules are specified.

## 5. Interpretation boundary

Conservation, synchronization, and component-wise evolution are properties of these selected equations. They do not establish that nature uses this architecture, that time is a field, or that all known interactions reduce to one physical field. Physical claims require independent definitions, quantitative predictions, and empirical comparison.

## 6. Shared-topology dimensional engine

`DimensionalFieldEngine` composes the scalar, phase, and tensor-array reference models on one weighted graph. Every present model must have the exact same adjacency matrix. Each domain retains its own state representation and governing equation.

The first prototype exposes two explicit cross-domain mappings. Let the scalar state be `phi`, the oscillator phases be `theta`, and the phase order parameter be `R`:

    omega_i,eff = omega_i + g_sf * mean(phi)
    source_i,eff = source_i,base + g_fs * R

The scalar mean shifts each oscillator's natural frequency by a uniform offset. Phase coherence contributes a uniform scalar source. The gains are user-defined conversion parameters, not physical constants.

At each time step, both signals are calculated from the pre-step state. Then all present submodels advance once. This defines a simultaneous explicit-Euler update scheme. It is not an exact integration of a continuous coupled system, and stability/convergence must be studied as the time step changes.

## 7. Shared variational potential prototype

`VariationalFieldSystem` defines a common dimensionless functional over normalized scalar coordinates x_i, phase coordinates theta_i, and tensor-component arrays T_i:

    V = 1/2*m_s*sum_i x_i^2
      + 1/2*m_t*sum_i ||T_i||^2
      + 1/2*sum_{i<j} W_ij * [
            g_s*(x_i-x_j)^2
          + g_t*||T_i-T_j||^2
          + 2*g_h*(1-cos(theta_i-theta_j))
          + lambda_s*(x_i-x_j)^2*(1-cos(theta_i-theta_j))
          + lambda_t*||T_i-T_j||^2*(1-cos(theta_i-theta_j))
        ]

Terms for absent domains are omitted. The cross terms couple scalar, phase, and tensor-array coordinates through one selected functional.

The undriven gradient flow is:

    dx/dtau       = -mu_s * partial(V)/partial(x)
    dtheta/dtau   = -mu_h * partial(V)/partial(theta)
    dT/dtau       = -mu_t * partial(V)/partial(T)

For positive mobilities and exact continuous-time flow with no external drive:

    dV/dtau = -mu_s*||grad_x V||^2
              -mu_h*||grad_theta V||^2
              -mu_t*||grad_T V||^2 <= 0

This is a consequence of the chosen gradient-flow construction, not a discovery about physical energy conservation. Explicit Euler requires time-step stability and convergence checks.

## 8. Hamiltonian conservative prototype

`HamiltonianFieldSystem` reuses V as a candidate potential and adds canonical momenta with positive diagonal inertias:

    H(q,p) = sum_a p_a^2/(2*m_a) + V(q)

It advances this separable autonomous Hamiltonian with velocity-Verlet. Natural-frequency forcing is rejected because it is not generated by the stated Hamiltonian. Inertias are dimensionless model parameters; V is not established physical energy.

## 9. Rayleigh-damped Hamiltonian prototype

`DampedHamiltonianFieldSystem` adds linear friction to each generalized coordinate block:

    q_dot_a = p_a / m_a
    p_dot_a = -partial(V)/partial(q_a) - gamma_a*p_a

For nonnegative damping coefficients gamma_a, the continuous energy balance is:

    dH/dt = -sum_a gamma_a * ||p_a||^2/m_a <= 0

The implementation uses symmetric operator splitting: exact half-step exponential momentum damping, one conservative velocity-Verlet step, then a second exact half-step damping. This is a second-order split integrator. The continuous energy law is exact for the stated differential equations; the discrete trajectory can show small energy fluctuations from the conservative integrator, so tests assess resolved long-run energy reduction rather than requiring strict per-step monotonicity.

## 10. Three-regime comparison experiment

`dynamics_comparison_demo.py` initializes three independent copies of the same one-coordinate quadratic potential, with the same initial coordinate and zero initial momentum:

- Gradient flow: `q_dot = -dV/dq`. It relaxes toward the minimum without inertial oscillation.
- Hamiltonian: `q_dot=p/m`, `p_dot=-dV/dq`. It oscillates while the ideal continuous Hamiltonian is conserved.
- Rayleigh damped: `q_dot=p/m`, `p_dot=-dV/dq-gamma*p`. It oscillates while losing energy to the modeled friction.

The demo emits CSV time series of coordinate and energy values. It is a controlled numerical comparison of three equations built from the same V, not evidence that the three regimes are all present in nature or that V is a physical energy. A follow-up study should vary dt, inertia, and damping; compare trajectories at matched physical/dimensionless times; and report convergence and energy-balance residuals.
