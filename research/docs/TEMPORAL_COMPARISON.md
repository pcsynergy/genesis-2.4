# Comparative temporal models

## Purpose

The temporal research layer compares several meanings of a clock without
assuming they are interchangeable. The models below are intentionally small
and auditable. They are candidate descriptions, not established physical laws.

## Implemented clock hypotheses

- **External/parameter clock:** the reading advances by the selected numerical
  parameter increment, d(lambda). This is a useful baseline, not a derivation
  of physical time.
- **Relational clock:** d(tau)/d(lambda) = r(state), with r strictly positive.
  If a state obeys dq/d(lambda) = F(q), then the correctly reparameterized
  equation is dq/d(tau) = F(q)/r(q). This chain-rule relation is tested.
- **Entropy-production clock:** accumulates a nonnegative entropy-production
  rate. It does not accumulate the entropy of an open subsystem, which may
  decrease. The clock can pause when production is zero and requires a
  thermodynamic model and calibration before it can represent duration.
- **Event clock:** counts discrete events. An event count is not a continuous
  duration unless an event-rate model or calibration is supplied.
- **Observer clock:** a phenomenological duration proxy. It is not proper time
  and makes no claim that consciousness creates physical time.
- **Hybrid clock:** reports the readings side by side, preserving distinctions
  instead of forcing a single composite time variable.

## Other theories: scope boundary

The present code does not implement full quantum relational time (such as a
Page-Wootters conditional-state construction), causal-set theory, relativistic
proper time, or a covariant thermodynamic time formulation. Those require
additional mathematical structures: Hilbert spaces and conditional states;
partially ordered causal events and a sprinkling/density prescription;
spacetime metrics and worldlines; or a specified entropy balance, respectively.
They are documented as future model families, not represented by toy clocks.

## How to interpret the comparison

The same numerical trajectory can be assigned different clock readings.
That is a comparison of parameterizations and observables, not evidence that
all readings are equally fundamental. A physical test must specify the system,
observable clock, units, coupling law, initial conditions, and measurable
prediction that differs between hypotheses.

## One Time Field Theory research framing

A useful working hypothesis is a **dual-aspect** program: investigate whether
a deeper physical structure supports both invariant temporal relations and
multiple operational clocks. Keep at least three questions separate:

1. Is there a fundamental temporal structure in the underlying dynamics?
2. Can durations be operationally reconstructed from relations, events, or
   thermodynamic processes?
3. How does an observer's estimated duration differ from instrument time?

This is a research strategy, not a conclusion. The code currently tests
bookkeeping, positivity, monotonicity, and the chain rule; it does not decide
which ontology is correct.
