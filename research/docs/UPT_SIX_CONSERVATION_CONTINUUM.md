# UPT-6: Conservation, Symmetry, and Physical Realization

**Author:** Pablo Salvador Cardenas  
**Status:** exploratory mathematical investigation  
**Scope:** Noether shift symmetry, graph-to-continuum equations, and distinctive predictions.

## Executive result

UPT-6 establishes three distinctions:

1. A conserved charge follows from a continuous symmetry of an action, not merely from a numerical pattern. The massless scalar field has a constant-shift symmetry and a corresponding Noether charge.
2. A graph Laplacian has a continuum limit only after a graph family, spatial scaling, and coupling scaling are specified. A first-order graph diffusion law approaches a diffusion-type PDE; a second-order variational field law approaches a wave/Klein–Gordon-type PDE. These are different dynamical classes.
3. The current UPT/OTFT prototype does not yet produce a distinctive empirical prediction. The graph model reproduces standard consensus/diffusion mathematics, and the continuum action reproduces a standard scalar-wave structure. A physical observable and a parameter-fixed deviation from a competing theory are still missing.

## 1. Noether symmetry and conservation

Take a real scalar field in 1+1 dimensional flat spacetime, metric signature (-,+), with action density

    L = 1/2 (partial_t phi)^2 - 1/2 c^2 (partial_x phi)^2.

The action is invariant under the global field shift phi -> phi + epsilon, where epsilon is constant. The canonical momentum density is pi = partial L / partial(partial_t phi) = partial_t phi. The Euler–Lagrange equation is

    partial_t^2 phi - c^2 partial_x^2 phi = 0.

Noether's theorem gives the shift charge

    Q = integral_0^L dx pi = integral_0^L dx partial_t phi.

For periodic boundary conditions (or vanishing boundary flux),

    dQ/dt = c^2 integral_0^L dx partial_x^2 phi
          = c^2 [partial_x phi]_0^L = 0.

Thus Q is conserved. The conserved quantity is the spatial integral of canonical momentum, not the arithmetic mean of phi itself. A non-constant potential V(phi) generally breaks this shift symmetry; a constant V does not affect the field equation.

**Important distinction:** the existing graph diffusion model

    partial_t phi = -kappa L_graph phi

is a dissipative first-order gradient flow. Its mean is conserved on an undirected graph because 1^T L_graph = 0, but this is not by itself a Noether derivation from a conservative wave action. Its quadratic disagreement decreases. Do not conflate graph mean conservation with the Noether charge of a scalar wave field.

## 2. Graph-to-continuum bridge

For a regular one-dimensional lattice with spacing h, the discrete Laplacian

    (phi_(i+1)-2phi_i+phi_(i-1))/h^2

approaches the second spatial derivative partial_x^2 phi as h tends to zero.

### 2.1 First-order diffusion

Starting from

    partial_t phi_i = D (phi_(i+1)-2phi_i+phi_(i-1))/h^2,

the continuum equation is

    partial_t phi = D partial_x^2 phi.

This is parabolic and dissipative. It smooths gradients and has no finite propagation speed in the ideal continuum PDE.

### 2.2 Second-order wave dynamics

Starting from a variational scalar-field model,

    partial_t^2 phi_i = c^2 (phi_(i+1)-2phi_i+phi_(i-1))/h^2 - m^2 phi_i,

the continuum equation is

    partial_t^2 phi - c^2 partial_x^2 phi + m^2 phi = 0.

This is the Klein–Gordon equation in 1+1 dimensions (under the stated conventions). It has a conserved energy for time-independent parameters and suitable boundary conditions. It is not the same equation as graph diffusion.

The existing GraphFieldNetwork is the first-order dissipative model. The existing ContinuumClockFieldSystem is a finite-difference second-order wave-like model coupled to an oscillator-like clock coordinate. These models should remain separate unless a derivation justifies a bridge between them.

## 3. Numerical probe and tests

New implementation:

- research/one_time_field/upt6_continuum.py
- research/tests/test_upt6_continuum.py
- research/examples/upt6_continuum_probe.py

The probe checks periodic Laplacian identities, the zero-sum acceleration that protects the shift charge, diffusion-rate balance, and basic energy positivity. It does not claim to numerically integrate a new physical theory.

The periodic identity is

    sum_i (phi_(i+1)-2phi_i+phi_(i-1)) = 0,

so the discrete wave equation preserves the discretized shift charge under the semi-discrete equations. The diffusion equation also has a zero-sum rate on a periodic grid, but its dynamics dissipate gradients; the shared zero-sum identity does not make diffusion a conservative Noether system.

## 4. Does UPT currently make a distinctive prediction?

**Not yet.** At this stage:

- The graph model is a standard weighted consensus/diffusion system.
- The continuum scalar equation is a standard wave/Klein–Gordon-type field equation.
- The shift-current conservation law is a standard Noether result.
- The OTFT scalar labelled T is a model field coordinate, not automatically physical time.
- Ontological Potential is not identified with the scalar potential-energy function V(phi).
- The current models do not define a new measurable quantity whose value differs from a competing established theory.

The coupled-versus-uncoupled graph comparison in UPT-5 is a model prediction conditional on choosing a nonzero coupling. It is not an empirical prediction about nature until nodes, states, couplings, units, and a measurement protocol are mapped to an actual physical system.

## 5. Requirements for a distinctive physical prediction

A future UPT extension must specify:

1. **Physical mapping:** identify what the state variables and relational couplings represent in a real system.
2. **Independent parameter fixing:** constrain parameters from independent measurements, not by fitting the target effect after the fact.
3. **Observable:** define a directly measurable quantity and its units.
4. **Competing baseline:** state the quantitative prediction of the relevant established theory under the same conditions.
5. **Deviation:** derive a numerical difference, including sign, scale, and parameter dependence.
6. **Uncertainty:** propagate theoretical, numerical, and measurement uncertainties.
7. **Falsification:** define an observation that would rule out the proposed extension.

Until these steps are completed, UPT is a conceptual and mathematical research framework with standard-model prototypes, not an empirically distinguished physical theory.

## 6. UPT interpretation

The UPT sequence Potential → One → Both → Many → All → Becoming can organize the conceptual interpretation of admissible states and relationships. The present calculations support only narrower mathematical statements: symmetric coupling can conserve a network mean; a shift-invariant action yields a Noether charge; and specified continuum scalings produce familiar PDEs. They do not demonstrate that ontological Potential is a physical field or that all fields are one.

## 7. Reproducibility

From the repository root:

    python -m unittest discover -s research/tests -v
    python research/examples/upt6_continuum_probe.py

All findings are mathematical consistency checks under stated assumptions, not empirical confirmation.
