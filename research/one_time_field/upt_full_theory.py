"""Integrated UPT reference model: potential, relations, dynamics, and records.

This is a modular research architecture, not a claim that all layers share
one established physical law. Each layer retains its own model semantics.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from random import Random
from typing import Any

from .upt8_renewed_potential import UPTAdaptivePotentialSpace
from .upt9_memory_dynamics import UPTMemoryDynamics
from .upt10_action_principle import UPTActionPrinciple
from .upt11_continuum_limit import continuum_refinement
from .upt14_uncertainty import (
    bootstrap_null_test, bootstrap_rate_interval, fit_relaxation_rate,
)


def cycle_adjacency(size: int = 4) -> tuple[tuple[float, ...], ...]:
    if not isinstance(size, int) or size < 3:
        raise ValueError("cycle size must be an integer >= 3")
    matrix = [[0.0] * size for _ in range(size)]
    for i in range(size):
        j = (i + 1) % size
        matrix[i][j] = matrix[j][i] = 1.0
    return tuple(tuple(row) for row in matrix)


@dataclass(frozen=True)
class FullUPTConfig:
    node_count: int = 4
    renewal_rounds: int = 3
    continuous_steps: int = 240
    dt: float = 0.001
    observation_sigma: float = 0.0005
    bootstrap_replicates: int = 40
    null_replicates: int = 99
    seed: int = 15015

    def __post_init__(self):
        if self.node_count < 3:
            raise ValueError("node_count must be >= 3")
        if self.renewal_rounds < 0 or self.continuous_steps < 10:
            raise ValueError("invalid renewal rounds or continuous step count")
        if self.dt <= 0 or self.observation_sigma <= 0:
            raise ValueError("dt and observation_sigma must be positive")
        if self.bootstrap_replicates < 20 or self.null_replicates < 99:
            raise ValueError("bootstrap needs >=20 and null calibration >=99 replicates")


def run_full_theory(config: FullUPTConfig = FullUPTConfig()) -> dict[str, Any]:
    """Run the UPT layers in a transparent, reproducible reference sequence.

    Discrete renewal, reversible CTMC, dissipative graph flow, continuum
    refinement, and observation inference are separate model layers. Their
    outputs are reported together but are not silently equated.
    """
    adjacency = cycle_adjacency(config.node_count)

    # Potential: explicit finite admissible configuration space and renewal.
    potential = UPTAdaptivePotentialSpace(
        adjacency=adjacency,
        initial_active_count=config.node_count // 2,
        activation_threshold=1.0,
        coupling=1.0,
        beta=0.8,
    )
    domains = potential.domain_history(config.renewal_rounds)

    # Reversible memory: finite augmented CTMC, separately defined dynamics.
    stochastic = UPTMemoryDynamics(
        adjacency=adjacency, coupling=0.7, memory_strength=0.4,
        beta=0.8, attempt_rate=1.0,
    )
    stationary = stochastic.stationary_distribution()
    markov_report = {
        "augmented_state_count": len(stochastic.states),
        "stationary_probability_sum": sum(stationary),
        "detailed_balance_max_residual": stochastic.detailed_balance_residual(),
        "interpretation": "equilibrium reversible CTMC; not the gradient-flow trajectory",
    }

    # Actualized field: finite graph Onsager gradient flow with global memory.
    action = UPTActionPrinciple(
        adjacency=adjacency, relational_strength=0.7,
        memory_strength=0.4, bistable_strength=0.15,
        field_mobility=0.8, memory_mobility=0.8,
    )
    field = tuple(0.15 + 0.25 * i for i in range(config.node_count))
    memory = 0.25
    initial_energy = action.energy(field, memory)
    times = [0.0]
    inputs = [sum(field)]
    latent_memory = [memory]
    accepted_steps = 0
    for _ in range(config.continuous_steps):
        field, memory, used_dt = action.step(field, memory, config.dt)
        accepted_steps += 1
        times.append(times[-1] + used_dt)
        inputs.append(sum(field))
        latent_memory.append(memory)
    final_energy = action.energy(field, memory)
    continuous_report = {
        "initial_energy": initial_energy,
        "final_energy": final_energy,
        "energy_change": final_energy - initial_energy,
        "energy_rate_at_final_state": action.energy_rate(field, memory),
        "final_field": list(field),
        "final_field_sum": sum(field),
        "final_memory": memory,
        "accepted_steps": accepted_steps,
        "elapsed_model_time": times[-1],
        "interpretation": "dissipative graph gradient flow; not Hamiltonian or stochastic CTMC evolution",
    }

    # Measurement layer: add declared independent Gaussian noise to memory
    # observations, retaining the initial condition as known.
    rng = Random(config.seed)
    observations = [latent_memory[0]] + [
        value + rng.gauss(0.0, config.observation_sigma)
        for value in latent_memory[1:]
    ]
    fit = fit_relaxation_rate(
        times, inputs, observations, config.observation_sigma, max_rate=5.0
    )
    interval = bootstrap_rate_interval(
        times, inputs, observations, config.observation_sigma,
        max_rate=5.0, replicates=config.bootstrap_replicates,
        seed=config.seed + 1,
    )
    null_test = bootstrap_null_test(
        times, inputs, observations, config.observation_sigma,
        max_rate=5.0, replicates=config.null_replicates,
        seed=config.seed + 2,
    )

    # Continuum cross-check is a separate limit of the scalar field model.
    refinement_rows, refinement_reference = continuum_refinement(
        final_time=0.01, counts=(16, 32, 64, 128), cfl=0.12
    )

    return {
        "framework": "Unified Potential Theory integrated reference model",
        "author": "Pablo Salvador Cardenas",
        "configuration": asdict(config),
        "ontological_sequence": [
            "Potential", "One", "Both", "Many", "All", "Becoming", "Renewed Potential"
        ],
        "potential_space": {
            "ambient_configuration_count": 2 ** config.node_count,
            "domain_sizes_by_renewal_round": [len(domain) for domain in domains],
            "closure_reached": len(domains) > 1 and domains[-1] == domains[-2],
            "expected_coherence_final_domain": potential.expected_coherence(domains[-1]),
            "interpretation": "finite admissibility model; domain renewal is not physical creation",
        },
        "reversible_memory": markov_report,
        "continuous_field": continuous_report,
        "continuum_refinement": {
            "coarse_to_fine": refinement_rows,
            "reference": refinement_reference,
            "interpretation": "numerical refinement of a 1-D gradient-flow model",
        },
        "observation_and_inference": {
            "fit": fit,
            "bootstrap_interval": interval,
            "null_test": null_test,
            "noise_sigma": config.observation_sigma,
            "interpretation": "synthetic noisy observations; not empirical evidence",
        },
        "integration_contract": {
            "shared_relation_graph": True,
            "potential_domain_to_ctmc": "shared finite graph, distinct admissible-state rules",
            "ctmc_to_gradient_flow": "parallel descriptions, not a derived transition",
            "gradient_flow_to_measurement": "sampled field sum drives a phenomenological relaxation fit",
            "continuum_model": "independent refinement cross-check, not an automatic limit of every discrete layer",
        },
        "scientific_status": (
            "Integrated computational framework. Mathematical and numerical checks "
            "do not establish ontological claims or empirical physical validity."
        ),
    }
