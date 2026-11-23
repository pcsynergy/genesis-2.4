"""Experimental mathematical models for the GENESIS Research layer."""
from .clock_action import ClockCoupledHamiltonianSystem
from .damped import DampedHamiltonianFieldSystem
from .engine import DimensionalFieldEngine
from .field_activity import FieldActivity
from .hamiltonian import HamiltonianFieldSystem
from .harmonic import PhaseOscillatorNetwork
from .network import GraphFieldNetwork
from .tensor import TensorFieldNetwork
from .temporal import TemporalLayer
from .temporal_comparison import run_comparison as run_temporal_comparison
from .temporal_coupling import run_coupling_experiment
from .temporal_models import (
    EntropyProductionClock, EventClock, ExternalClock, HybridClock,
    ObserverClock, RelationalClock,
)
from .variational import VariationalFieldSystem

__all__ = [
    "ClockCoupledHamiltonianSystem",
    "DampedHamiltonianFieldSystem",
    "DimensionalFieldEngine",
    "FieldActivity",
    "GraphFieldNetwork",
    "HamiltonianFieldSystem",
    "PhaseOscillatorNetwork",
    "TensorFieldNetwork",
    "TemporalLayer",
    "run_temporal_comparison",
    "run_coupling_experiment",
    "EntropyProductionClock",
    "EventClock",
    "ExternalClock",
    "HybridClock",
    "ObserverClock",
    "RelationalClock",
    "VariationalFieldSystem",
]
