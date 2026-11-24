# UPT-11: Continuum Limit and Model-Level Observables

**Author:** Pablo Salvador Cardenas  
**Status:** dimensionless periodic 1-D gradient-flow discretization and refinement experiment

## Research question

Does the relational-memory structure introduced in UPT-10 admit a controlled continuum formulation, and can its numerical solution be compared across spatial resolutions using explicit observables?

UPT-11 constructs one continuum model and tests a finite-difference approximation. It does not infer a unique continuum law from UPT's ontology.

## 1. Continuum energy functional

On a periodic interval of length L, let \(\phi(x,t)\) be a scalar field and \(m(t)\) a spatially global memory coordinate. Consider

\[
H[\phi,m]=\int_0^L dx\left[
\frac J2(\partial_x\phi)^2+
\frac\lambda4\phi^2(1-\phi)^2
\right]
+\frac{\kappa L}{2}(\bar\phi-m)^2,
\qquad
\bar\phi=\frac1L\int_0^L\phi\,dx.
\]

The relational term penalizes spatial gradients. The quartic term favors field values near 0 or 1. The final term couples the spatial mean to a global memory variable. This is a candidate functional selected for tractability, not uniquely dictated by UPT.

## 2. Gradient-flow equations

Using the spatial \(L^2\) metric for the field and a scalar mobility for memory gives

\[
\partial_t\phi=\Gamma_\phi\left[
J\partial_x^2\phi
-\frac\lambda2\phi(1-\phi)(1-2\phi)
-\kappa(\bar\phi-m)
\right],
\]

\[
\dot m=\Gamma_m\kappa(\bar\phi-m).
\]

The equations are dissipative Onsager dynamics. They are not relativistic wave equations, Hamiltonian dynamics, or a claim that physical time emerges from memory.

## 3. Energy dissipation

For periodic boundary conditions,

\[
\frac{dH}{dt}
=-\Gamma_\phi\int_0^L dx
\left(\frac{\delta H}{\delta\phi(x)}\right)^2
-\frac{\Gamma_m}{L}\left(\frac{\partial H}{\partial m}\right)^2
\leq0.
\]

The finite-grid implementation uses the periodic centered Laplacian and a line-searched explicit step. It monitors energy and spatial observables.

## 4. Discretization and refinement

For \(N\) equally spaced sites, \(h=L/N\), and periodic indices, the discrete energy is

\[
H_h=\frac{Jh}{2}\sum_i\left(\frac{\phi_{i+1}-\phi_i}{h}\right)^2
+\frac{\lambda h}{4}\sum_i\phi_i^2(1-\phi_i)^2
+\frac{\kappa L}{2}(\bar\phi_h-m)^2.
\]

The field gradient is divided by \(h\) when using the discrete approximation to the spatial \(L^2\) metric. This scaling is essential: it avoids treating an unscaled graph sum as if it were already a continuum integral.

The refinement experiment compares periodic grids \(N=16,32,64\), and \(128\) at the same final time. The timestep scales with \(h^2\), as expected for an explicit diffusion-like scheme. Coarser solutions are compared with a linearly interpolated finest-grid solution.

## 5. Model-level observables

The code reports:
- spatial mean \(\bar\phi\);
- spatial variance \(L^{-1}\int(\phi-\bar\phi)^2dx\);
- global memory coordinate \(m\);
- energy \(H\);
- RMS field discrepancy relative to the finest grid.

These are observables of this model, not yet observables identified in a laboratory or astronomical dataset.

## 6. Verification

Seven tests check:
1. analytic variational gradients against centered finite differences;
2. nonpositive instantaneous energy rate;
3. energy decrease under a sufficiently small numerical step;
4. periodic uniform-field spatial-gradient behavior;
5. finite mean/variance observables;
6. decreasing refinement error for smooth initial data;
7. input validation.

The experiment runner prints refinement errors and model observables. Passing tests establish numerical consistency of this implementation, not physical correctness.

## 7. Units, interpretation, and limitations

All quantities are dimensionless in this prototype. To interpret \(J,\lambda,\kappa,\Gamma_\phi,\Gamma_m\) physically, one must define units for length, time, field amplitude, energy, and memory, then verify that every term in \(H\) has consistent dimensions. No parameter is fitted to data.

The continuum equations are a scalar dissipative reaction-diffusion system with a global mean-field coupling. They are mathematically related to established gradient-flow and reaction-diffusion models. UPT-11 does not demonstrate a new force, a new time variable, quantum behavior, or a departure from standard physics.

## 8. Next falsifiability step

A physical test requires an independently motivated mapping from \(\phi,m\) to measured quantities, a calibrated parameter protocol, uncertainty propagation, and a competing standard model. Only then can one ask whether UPT predicts a residual difference beyond measurement and model uncertainty.

**Attribution:** Pablo Salvador Cardenas.
