# Symphony 5.5 / UPT — Milestone G: Analytical linear stability

**Status:** implemented; CI validation pending  
**Runner:** `research/examples/symphony_harmonic_stability.py`  
**Tests:** `research/tests/test_symphony_stability.py`

## Question

Can local stability of synchronized and twisted phase configurations be predicted from the Jacobian of the oscillator dynamics, rather than inferred only from time-series simulations?

## Linearization

For the normalized phase model
[
\dot\theta_i=\omega_i+\frac{K}{d_i}\sum_j A_{ij}\sin(\theta_j-\theta_i),
\qquad d_i=\sum_j A_{ij},
]
the interaction Jacobian has off-diagonal entries
[
J_{ij}=\frac{K A_{ij}}{d_i}\cos(\theta_j-\theta_i),\quad i\ne j,
]
and diagonal entries (J_{ii}=-\sum_{j\ne i}J_{ij}). The row sums vanish because a common shift of every phase leaves all phase differences unchanged. The corresponding neutral eigenvalue is the global-phase symmetry mode.

The implementation computes the real symmetric spectra for regular undirected examples using a Jacobi eigenvalue algorithm. The stability classifier excludes eigenvalues near zero and examines the remaining spectrum.

## Cases

1. **Complete graph, synchronized state:** all phases equal. The expected spectrum is one zero eigenvalue and (N-1) eigenvalues equal to (-KN/(N-1)) under the degree-normalized coupling convention.
2. **Ten-node ring, winding number (q=1):** adjacent phase difference (2\pi/10). Since (cos(2\pi/10)>0), the transverse ring modes are expected to decay.
3. **Ten-node ring, winding number (q=2):** adjacent phase difference (4\pi/10). Here (cos(4\pi/10)<0), so non-neutral modes include positive growth rates and the twisted state is linearly unstable.

## Findings and scope

The tests compare the complete-graph numerical spectrum with its closed-form eigenvalues, check the zero row-sum symmetry, and distinguish the two ring winding states by their transverse eigenvalue signs. This provides an analytical local-stability test for these exact configurations.

Linear stability is local: it predicts behavior of sufficiently small perturbations near the selected equilibrium or uniformly rotating state. It does not prove global convergence, characterize all attractors, or establish stability for arbitrary heterogeneous frequencies or non-regular graphs.

## Scientific boundary

This remains a finite Kuramoto-style phase-network model. The eigenvalue results are mathematical consequences of the stated equations and parameter choices. They do not demonstrate that the model describes physical spacetime, cosmological creation, consciousness, or a new fundamental field, and they do not independently validate UPT / One Time Field Theory.
