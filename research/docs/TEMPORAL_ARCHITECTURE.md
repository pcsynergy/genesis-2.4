# Temporal architecture: parameter, relation, and experience

## Motivation

The existing field solvers advance states using a supplied independent variable and timestep. This is ordinary numerical dynamics; it does not explain what physical time is. Adding a state called time would not solve the foundational question if it still evolves against an external parameter.

## Three distinct layers

1. **Parameter time:** the computational ordering parameter used by the integrator. It is not asserted to be physical time.
2. **Relational time:** an accumulated clock reading whose rate is coupled to a declared event/activity measure.
3. **Observer time:** a phenomenological proxy whose rate may respond differently to activity and a reference activity level.

The module also accumulates total activity. This can serve as a rudimentary event measure, but it is not a count of discrete physical events unless a future model defines an event threshold or event process.

## Implemented prototype

For activity A and parameter increment dλ, the current implementation uses:

    dτ/dλ = 1 + g_r A
    dσ/dλ = max(r_min, 1 + g_o(A - A_ref))
    dI/dλ = A

Here τ is relational time, σ is observer-time proxy, I is accumulated activity, and g_r, g_o, A_ref, r_min are model parameters. Values are dimensionless until calibrated. The positive floor keeps the observer clock from running backward in this prototype; it is a modeling constraint, not a physical result.

## Relation to One Time Field Theory and physics

This architecture allows time to be explored as relational and observer-experienced without prematurely asserting that subjective observation creates physical time. In relativity, proper time is defined along a worldline and differs from an arbitrary coordinate-time label. Thermodynamic irreversibility, event ordering, and subjective duration are also distinct questions.

The prototype does **not** derive proper time from the scalar, phase, or tensor-array fields; it does not implement spacetime geometry, causal cones, Einstein's equations, or a validated observer model. It is a bookkeeping and hypothesis-testing scaffold, not a physical theory.

## Falsifiable next steps

- Define activity from explicit field invariants or discrete state transitions, not a hand-supplied signal.
- Calibrate rates and units against a specified physical clock.
- Test whether predictions expressed in clock readings are invariant under reparameterization of the computational variable.
- Compare multiple physical clock models and quantify disagreement.
- Keep observer-time predictions separate from proper-time predictions.
