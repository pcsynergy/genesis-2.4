"""UPT-14: noisy observations, bootstrap uncertainty, and null calibration.

Known initial condition; independent Gaussian measurement errors on m[1:].
The latent trajectory is propagated recursively, not from noisy predictors.
"""
from __future__ import annotations
from math import exp, isfinite, sqrt
from random import Random
from typing import Sequence


def _validate(times, mean_field, observations, sigma, max_rate):
    if len(times) < 10 or len(times) != len(mean_field) or len(times) != len(observations):
        raise ValueError("series must have equal length >= 10")
    if any(not isfinite(float(v)) for seq in (times, mean_field, observations) for v in seq):
        raise ValueError("series values must be finite")
    if any(times[i + 1] <= times[i] for i in range(len(times) - 1)):
        raise ValueError("times must be strictly increasing")
    if not isfinite(sigma) or sigma <= 0:
        raise ValueError("sigma must be finite and positive")
    if not isfinite(max_rate) or max_rate <= 0:
        raise ValueError("max_rate must be finite and positive")


def predict_memory(times, mean_field, initial_memory, rate):
    if not isfinite(rate) or rate < 0:
        raise ValueError("rate must be finite and nonnegative")
    if len(times) != len(mean_field) or len(times) < 2:
        raise ValueError("times and mean_field need equal length >= 2")
    values = [float(initial_memory)]
    for i in range(len(times) - 1):
        dt = times[i + 1] - times[i]
        if dt <= 0:
            raise ValueError("times must be strictly increasing")
        values.append(mean_field[i] + (values[-1] - mean_field[i]) * exp(-rate * dt))
    return values


def _sse(rate, times, mean_field, observations, stop):
    predicted = predict_memory(times[:stop + 1], mean_field[:stop + 1],
                               observations[0], rate)
    return sum((observations[i + 1] - predicted[i + 1]) ** 2 for i in range(stop))


def _golden_minimize(function, lower, upper, iterations=120):
    ratio = (sqrt(5.0) - 1.0) / 2.0
    x1, x2 = upper - ratio * (upper - lower), lower + ratio * (upper - lower)
    f1, f2 = function(x1), function(x2)
    for _ in range(iterations):
        if f1 <= f2:
            upper, x2, f2 = x2, x1, f1
            x1 = upper - ratio * (upper - lower)
            f1 = function(x1)
        else:
            lower, x1, f1 = x1, x2, f2
            x2 = lower + ratio * (upper - lower)
            f2 = function(x2)
    return (lower + upper) / 2.0


def fit_relaxation_rate(times: Sequence[float], mean_field: Sequence[float],
                        observations: Sequence[float], sigma: float,
                        max_rate: float = 10.0):
    """Gaussian maximum-likelihood rate for fixed known observation sigma."""
    _validate(times, mean_field, observations, sigma, max_rate)
    objective = lambda r: _sse(r, times, mean_field, observations, len(times) - 1)
    candidate = _golden_minimize(objective, 0.0, max_rate)
    rate = min((0.0, candidate, max_rate), key=objective)
    sse, null_sse = objective(rate), objective(0.0)
    return {
        "fitted_relaxation_rate": rate,
        "sse_coupled": sse,
        "sse_null": null_sse,
        "likelihood_ratio_statistic": max(0.0, (null_sse - sse) / sigma**2),
        "observations": len(times) - 1,
        "sigma_assumed_known": sigma,
        "scope": "Gaussian observation model; phenomenological parameter estimate",
    }


def simulate_observations(times, mean_field, initial_memory, rate, sigma, seed):
    if not isfinite(sigma) or sigma <= 0:
        raise ValueError("sigma must be finite and positive")
    latent = predict_memory(times, mean_field, initial_memory, rate)
    rng = Random(seed)
    return [latent[0]] + [v + rng.gauss(0.0, sigma) for v in latent[1:]]


def bootstrap_rate_interval(times, mean_field, observations, sigma,
                            max_rate=10.0, replicates=200, seed=1401,
                            confidence=0.95):
    """Parametric percentile interval conditional on fitted Gaussian model."""
    if replicates < 20:
        raise ValueError("replicates must be >= 20")
    if not 0.5 < confidence < 1.0:
        raise ValueError("confidence must be in (0.5, 1)")
    fit = fit_relaxation_rate(times, mean_field, observations, sigma, max_rate)
    fitted = fit["fitted_relaxation_rate"]
    latent = predict_memory(times, mean_field, observations[0], fitted)
    rng, estimates = Random(seed), []
    for _ in range(replicates):
        sample = [latent[0]] + [v + rng.gauss(0.0, sigma) for v in latent[1:]]
        estimates.append(fit_relaxation_rate(
            times, mean_field, sample, sigma, max_rate
        )["fitted_relaxation_rate"])
    estimates.sort()
    alpha = (1.0 - confidence) / 2.0
    return {
        "rate_estimate": fitted, "confidence": confidence,
        "interval_low": estimates[int(alpha * (replicates - 1))],
        "interval_high": estimates[int((1.0 - alpha) * (replicates - 1))],
        "bootstrap_replicates": replicates,
        "method": "parametric percentile bootstrap under fitted Gaussian model",
        "scope": "conditional on known sigma, fixed inputs, and model specification",
    }


def bootstrap_null_test(times, mean_field, observations, sigma,
                        max_rate=10.0, replicates=499, seed=1402):
    """Calibrate boundary-null likelihood ratio by Monte Carlo under r=0."""
    if replicates < 99:
        raise ValueError("replicates must be >= 99 for null calibration")
    observed = fit_relaxation_rate(times, mean_field, observations, sigma, max_rate)
    statistic = observed["likelihood_ratio_statistic"]
    null_latent = predict_memory(times, mean_field, observations[0], 0.0)
    rng, exceedances = Random(seed), 0
    for _ in range(replicates):
        sample = [null_latent[0]] + [v + rng.gauss(0.0, sigma) for v in null_latent[1:]]
        simulated = fit_relaxation_rate(times, mean_field, sample, sigma, max_rate)
        exceedances += simulated["likelihood_ratio_statistic"] >= statistic
    return {
        "likelihood_ratio_statistic": statistic,
        "null_bootstrap_p_value": (1 + exceedances) / (replicates + 1),
        "null_replicates": replicates, "exceedances": exceedances,
        "calibration": "parametric Monte Carlo under r=0; boundary-aware",
        "scope": "valid only under the stated known-sigma Gaussian null model",
    }
