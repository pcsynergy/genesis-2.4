"""UPT-13: falsifiable comparison of memory relaxation and a null model.

This is a model-discrimination protocol for a first-order relaxation law.
It is not a claim that the law is a new physical mechanism.
"""
from __future__ import annotations

from math import exp, isfinite, log
from typing import Sequence


def _validate(times, mean_field, memory_values, max_rate):
    if len(times) < 9 or len(times) != len(mean_field) or len(times) != len(memory_values):
        raise ValueError("times, mean_field and memory_values need equal length >= 9")
    if any(not isfinite(float(v)) for seq in (times, mean_field, memory_values) for v in seq):
        raise ValueError("all observations must be finite")
    if any(times[i + 1] <= times[i] for i in range(len(times) - 1)):
        raise ValueError("times must be strictly increasing")
    if not isfinite(max_rate) or max_rate <= 0:
        raise ValueError("max_rate must be finite and positive")


def _transition_prediction(m0, u, dt, rate):
    if rate == 0:
        return m0
    decay = exp(-rate * dt)
    return u + (m0 - u) * decay


def _sse(rate, times, mean_field, memory_values, stop):
    total = 0.0
    for i in range(stop):
        predicted = _transition_prediction(
            memory_values[i], mean_field[i], times[i + 1] - times[i], rate
        )
        residual = memory_values[i + 1] - predicted
        total += residual * residual
    return total


def _golden_minimize(function, lower, upper, iterations=120):
    ratio = (5.0 ** 0.5 - 1.0) / 2.0
    x1 = upper - ratio * (upper - lower)
    x2 = lower + ratio * (upper - lower)
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
    candidate = (lower + upper) / 2.0
    return candidate


def _aicc(sse, n, parameters):
    if n <= parameters + 1:
        raise ValueError("not enough training transitions for AICc")
    # Gaussian likelihood with unknown residual variance; floor only avoids log(0).
    base = n * log(max(sse / n, 1e-300))
    correction = 2 * parameters + (
        2 * parameters * (parameters + 1) / (n - parameters - 1)
    )
    return base + correction


def compare_memory_relaxation(times: Sequence[float],
                              mean_field: Sequence[float],
                              memory_values: Sequence[float],
                              train_fraction=0.7,
                              max_rate=10.0):
    """Fit positive relaxation rate on early transitions; score later ones.

    Model: dm/dt = r * (u - m), where u is held constant over each interval.
    The exact interval propagator is used. The null model fixes r=0.
    """
    _validate(times, mean_field, memory_values, max_rate)
    if not isfinite(train_fraction) or not 0.5 <= train_fraction < 0.9:
        raise ValueError("train_fraction must be in [0.5, 0.9)")
    transitions = len(times) - 1
    train_n = int(transitions * train_fraction)
    if train_n < 5 or transitions - train_n < 2:
        raise ValueError("split must leave >=5 training and >=2 test transitions")

    objective = lambda rate: _sse(rate, times, mean_field, memory_values, train_n)
    fitted_rate = _golden_minimize(objective, 0.0, max_rate)
    candidates = [(0.0, objective(0.0)), (fitted_rate, objective(fitted_rate)),
                  (max_rate, objective(max_rate))]
    fitted_rate, train_sse = min(candidates, key=lambda item: item[1])
    null_train_sse = objective(0.0)

    test_sse = _sse(fitted_rate, times[train_n:], mean_field[train_n:],
                    memory_values[train_n:], transitions - train_n)
    null_test_sse = _sse(0.0, times[train_n:], mean_field[train_n:],
                         memory_values[train_n:], transitions - train_n)
    test_n = transitions - train_n
    train_aicc_coupled = _aicc(train_sse, train_n, 1)
    train_aicc_null = _aicc(null_train_sse, train_n, 0)

    return {
        "fitted_relaxation_rate": fitted_rate,
        "train_rmse_coupled": (train_sse / train_n) ** 0.5,
        "train_rmse_null": (null_train_sse / train_n) ** 0.5,
        "test_rmse_coupled": (test_sse / test_n) ** 0.5,
        "test_rmse_null": (null_test_sse / test_n) ** 0.5,
        "test_sse_coupled": test_sse,
        "test_sse_null": null_test_sse,
        "train_aicc_coupled": train_aicc_coupled,
        "train_aicc_null": train_aicc_null,
        "delta_aicc_null_minus_coupled": train_aicc_null - train_aicc_coupled,
        "training_transitions": train_n,
        "test_transitions": test_n,
        "decision_rule": (
            "Evidence for added predictive value requires lower held-out RMSE "
            "for the coupled model and lower training AICc; otherwise do not "
            "claim support for nonzero memory coupling."
        ),
        "scope": "phenomenological model comparison; not empirical validation",
    }
