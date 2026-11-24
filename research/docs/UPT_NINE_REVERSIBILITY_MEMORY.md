# UPT-9: Reversibility, Memory, and Thermodynamic Consistency

**Author:** Pablo Salvador Cardenas  
**Status:** finite continuous-time Markov-chain prototype; not an empirically established physical theory

## Research program

This milestone addresses all five questions in one shared model: reversible entry and exit from an instantaneous admissible domain; probability conservation; detailed balance; explicit memory dependence; and comparison with a memoryless baseline.

## 1. Augmented state and adaptive admissibility

Let q be a four-component binary configuration and m in {0,1,2,3,4} a discrete memory coordinate storing a prior active-count signal. The augmented state x=(q,m) has 2^4 × 5 = 80 states.

For tolerance δ, define the memory-conditioned admissible set

    D_m = {q : |sum_i q_i - m| <= δ}.

With δ=1, this set expands or contracts as m changes. This is a state-dependent model domain, not literal creation or destruction of physical possibilities.

## 2. Energy and reversible transitions

For symmetric nonnegative adjacency W, define

    H(q,m) = (J/2) sum_(i<j) W_ij(q_i-q_j)^2
             + (κ/2)(sum_i q_i-m)^2.

The first term penalizes relational disagreement; the second couples the configuration to its memory coordinate. The transition graph consists of single-bit flips in q and unit steps in m. For neighboring augmented states x,y, use Metropolis rates

    r(x→y) = ν exp[-β max(0,H(y)-H(x))].

Each proposal edge is bidirectional with the same attempt rate ν. Therefore the Gibbs distribution

    π(x) = exp[-βH(x)] / Z

satisfies detailed balance: π(x)r(x→y)=π(y)r(y→x).

## 3. Probability conservation

The row generator Q has off-diagonal entries Q_xy=r(x→y) and diagonal entries Q_xx=-sum_(y≠x)r(x→y). Every row sums to zero. For a row probability vector p, the master equation is dp/dt=pQ, so total probability is conserved.

The numerical evolution uses small stochastic Euler substeps P=I+Δt Q, with Δt chosen so all entries are nonnegative. This preserves probability normalization and positivity at each substep; it is a convergent numerical approximation, not an exact matrix exponential.

## 4. Thermodynamic consistency

The Metropolis construction is reversible with respect to the Gibbs distribution above. It is an equilibrium detailed-balance model, not a driven nonequilibrium model. It has no stationary equilibrium entropy production. A nonequilibrium extension would require explicit driving, reservoirs, or nonconservative cycle affinities.

H is dimensionless in this prototype; βH must be dimensionless. ν sets the inverse time unit. No parameters are fitted to physical data.

## 5. Memory test

For κ>0, the transition rate for changing q depends on m through the mismatch term. The same q can therefore have different next-transition rates depending on the stored memory coordinate. At κ=0, this coupling disappears.

The augmented (q,m) process is Markovian. The q-only projection generally has memory because m contains information not present in q. This is a standard hidden-state construction, not evidence of a new physical memory law.

## 6. Distinguishing adaptive behavior from a baseline

Hold W, J, β, ν, and q fixed while varying κ. At κ=0, q transition rates are independent of m. At κ>0, they vary with m. This is an exact conditional model-level distinction.

A physical distinction would require a mapping for q and m, independently measured parameters, a measurement protocol, uncertainties, and a competing physical baseline. None is currently supplied.

## 7. Verification

Thirteen unit tests check: 80 augmented states; generator row sums; nonnegative rates; bidirectional transitions; Gibbs normalization and detailed balance; stationarity; positivity and probability conservation; memory-dependent rates; the κ=0 limit; expansion/contraction of D_m; baseline differences; and invalid-input rejection.

## 8. Scope

UPT-9 demonstrates that reversible adaptive admissibility, probability conservation, equilibrium consistency, and memory dependence can coexist in a finite mathematical construction. It does not establish that this construction describes nature or that UPT is empirically validated. A physical theory must derive the variables and energy from a physical action or microscopic model, assign units, identify observables, recover known limits, and produce a falsifiable deviation with uncertainty bounds.

**Attribution:** Pablo Salvador Cardenas.
