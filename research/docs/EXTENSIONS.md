# Research Extensions — Draft 0.3

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

The first prototype exposes two explicit cross-domain mappings. Let the scalar state be `phi`, the oscillator phases be `theta`, and the phase order parameter be `R):

    omega_i,eff = omega_i + g_sf * mean(phi)
    source_i,eff = source_i,base + g_fs * R

The scalar mean shifts each oscillator's natural frequency by a uniform offset. Phase coherence contributes a uniform scalar source. The gains g_sf and g_fs are user-defined conversion parameters whose units must be selected for a particular experiment. They are not physical constants.

At each time step, both signals are calculated from the pre-step state. Then all present submodels advance once. This defines a simultaneous explicit-Euler update scheme. It is not an exact integration of a continuous coupled system, and stability/convergence must be studied as the time step changes.

The tensor-array domain currently shares the graph and advances independently. It has no cross-domain coupling yet. This is intentional: a coupling should be added only after its mathematical mapping, units, and intended interpretation are stated.

### What the engine demonstrates

- Heterogeneous state domains can share a common graph topology.
- Distinct update laws can be composed without pretending that all state components are the same kind of quantity.
- Cross-domain effects can be introduced as explicit, testable model assumptions.
- A detached snapshot/history can record the combined state for later analysis.

### What it does not demonstrate

The engine does not derive a unique unified field equation, establish that time is a physical field, or show that scalar, vector, tensor, and phase variables are interchangeable. It is a modular computational architecture. A physical interpretation requires a dimensional analysis, transformation laws where appropriate, independent predictions, and comparison with observations.


## 7. Shared variational potential prototype

`VariationalFieldSystem` is a second architecture, distinct from the earlier modular dimensional engine. It asks whether scalar, phase, and tensor-array states can be evolved from one common dimensionless potential functional.

For normalized scalar coordinates x_i, phase coordinates theta_i, and tensor-component arrays T_i, define

    V = 1/2*m_s*sum_i x_i^2
      + 1/2*m_t*sum_i ||T_i||^2
      + 1/2*sum_{i<j} W_ij * [
            g_s*(x_i-x_j)^2
          + g_t*||T_i-T_j||^2
          + 2*g_h*(1-cos(theta_i-theta_j))
          + lambda_s*(x_i-x_j)^2*(1-cos(theta_i-theta_j))
          + lambda_t*||T_i-T_j||^2*(1-cos(theta_i-theta_j))
        ]

Terms for absent state domains are omitted. The lambda_s and lambda_t terms make the scalar and tensor graph penalties depend on relative phase. Conversely, their state differences modify the phase gradient. Thus the three state domains are coupled through a single scalar functional while retaining distinct coordinates.

The deterministic, undriven evolution is a mobility-weighted gradient flow:

    dx/dtau       = -mu_s * partial(V)/partial(x)
    dtheta/dtau   = -mu_h * partial(V)/partial(theta)
    dT/dtau       = -mu_t * partial(V)/partial(T)

Optional natural phase frequencies add an external drive to the phase equation. In that driven case V is not generally a Lyapunov function and need not decrease monotonically.

### Mathematical interpretation

For positive mobilities and exact continuous-time gradient flow with no external drive,

    dV/dtau = -mu_s*||grad_x V||^2
              -mu_h*||grad_theta V||^2
              -mu_t*||grad_T V||^2 <= 0

with absent-domain terms omitted. This is a consequence of the chosen gradient-flow construction, not a discovery about physical energy conservation. Explicit Euler only approximates this behavior and requires time-step convergence and stability tests.

All coordinates are normalized and dimensionless in this prototype. To interpret V as a physical energy, one must specify reference scales, units, and a justified mapping to observables. The coefficients are model parameters, not measured constants. The tensor state remains a component array, not a geometric tensor with transformation laws.

### What this prototype tests

- Whether several state domains can be coupled by one well-defined functional.
- Whether the implemented gradients match numerical finite differences.
- Whether undriven gradient flow reduces the functional for sufficiently small time steps.
- Whether the phase sector respects global phase-shift symmetry.

It does not establish that the universe is governed by this functional, that the functional is unique, or that its coordinates represent fundamental physical fields.
