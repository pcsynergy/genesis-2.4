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
