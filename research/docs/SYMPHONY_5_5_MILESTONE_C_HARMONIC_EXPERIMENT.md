# Symphony 5.5 / UPT — Milestone C: Harmonic Creation Experiment

**Status:** implemented as a reproducible mathematical toy experiment  
**Code:** `one_time_field/harmonic.py`, `examples/symphony_harmonic_creation.py`  
**Tests:** `tests/test_harmonic.py`

## Question

Can a network of initially dispersed oscillators develop collective phase coherence through local coupling, and how does that behavior change when coupling is removed or strengthened?

This operationalizes the manuscript's recurring musical language—rhythm, harmony, resonance, orchestration, and the relation of parts to a whole—without treating metaphor as a physical derivation.

## Model

The existing phase network implements a normalized Kuramoto-style system:

\[
\dot\theta_i = \omega_i +
K\frac{\sum_j W_{ij}\sin(\theta_j-\theta_i)}
{\sum_j W_{ij}},
\]

where \(\theta_i\) is oscillator phase, \(\omega_i\) its natural angular frequency, \(W_{ij}\) a symmetric nonnegative adjacency weight, and \(K\geq0\) the coupling strength. Isolated nodes have no interaction term.

The global phase-coherence observable is

\[
R(t)=\left|\frac{1}{N}\sum_{j=1}^{N}e^{i\theta_j(t)}\right|,
\qquad 0\leq R\leq1.
\]

Values near zero indicate dispersed phases; values near one indicate phase alignment. This is a mathematical coherence statistic, not a measure of consciousness, cosmic unity, or total physical energy.

## Reproducible setup

- Eight oscillators on a fully connected, undirected, unit-weight graph.
- Initial phases evenly spaced around the circle, giving near-zero initial coherence.
- Natural frequencies \(\omega_i=1+0.03(i-3.5)\), in arbitrary inverse-time units.
- Explicit Euler phase updates, \(\Delta t=0.01\), for 3,000 steps.
- Coupling cases \(K=0,0.5,1,2\).

## Reference numerical outcome

For the stated setup, the existing implementation gives approximately:

| Coupling \(K\) | Initial \(R\) | Final \(R\) |
|---:|---:|---:|
| 0.0 | 0.000000 | 0.0741 |
| 0.5 | 0.000000 | 0.9926 |
| 1.0 | 0.000000 | 0.9982 |
| 2.0 | 0.000000 | 0.9995 |

These are outputs of this finite-dimensional toy model, not observations of nature. The near-zero initial value is numerical roundoff around the exact evenly spaced-phase result of zero.

## Interpretation

1. **Uncoupled case:** natural-frequency differences gradually move the phase pattern, but no interaction mechanism coordinates the oscillators.
2. **Coupled cases:** the sine interaction transfers phase information across the graph. In this selected parameter regime, coherence rises sharply.
3. **Stronger coupling:** coherence approaches one more closely in the tested range. This does not establish a universal monotonic law for arbitrary graphs, frequencies, or initial conditions.
4. **Musical analogy:** the model gives a precise, limited meaning to “many rhythms becoming coordinated.” It does not derive the origin of matter, life, intelligence, or the universe.

## Stability and limitations

The current integrator is explicit Euler. The phase variable is wrapped modulo \(2\pi\), and the implementation does not calculate a conserved mechanical energy. Therefore this experiment reports phase coherence and instantaneous frequency-rate spread, not energy conservation. Numerical reliability should be checked by repeating with smaller time steps and comparing observables.

The Kuramoto model is a phenomenological oscillator model. It is not Lorentz-covariant, does not include spacetime curvature, and does not provide a relativistic field action. It should remain separate from the repository's scalar-field and FLRW experiments.

## UPT / Symphony mapping

The manuscript's symbolic movement from potential to unity, duality, multiplicity, and a relational whole can be used as a narrative interpretation of this experiment:

\[
\mathcal P \rightarrow 1 \rightarrow 2 \rightarrow N
\rightarrow \text{collective coherence}.
\]

Only the final network dynamics and the defined observable are mathematical content here. The symbolic sequence is an interpretive overlay; it is not an equation derived by the oscillator model.

## Falsifiable next steps

- Sweep coupling strength, frequency dispersion, graph topology, and initial phase distributions.
- Compare Euler results against smaller time steps and a higher-order integrator.
- Test whether coherence thresholds depend on topology and frequency distribution.
- Add a clearly defined energy-bearing oscillator model only if a physical energy interpretation is required.

A stronger scientific claim would require a distinct prediction and comparison against an established baseline. This milestone demonstrates synchronization in a standard toy model; it does not validate UPT or a new fundamental field theory.
