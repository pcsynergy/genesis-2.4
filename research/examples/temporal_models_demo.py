"""Compare distinct clock readings for the same sequence of model steps."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from one_time_field.temporal_models import (
    EntropyProductionClock, EventClock, ExternalClock, HybridClock,
    ObserverClock, RelationalClock,
)

clocks = HybridClock(
    external=ExternalClock(),
    relational=RelationalClock(),
    entropy=EntropyProductionClock(),
    events=EventClock(),
    observer=ObserverClock(),
)
# Illustrative inputs only; no values are fitted to a physical system.
steps = [
    (0.5, 0.8, 0.02, 1),
    (0.5, 1.4, 0.05, 2),
    (0.5, 0.6, 0.01, 1),
]
for dt, activity, entropy_rate, event_count in steps:
    clocks.external.advance(dt)
    clocks.relational.advance(dt, 1.0 + 0.25 * activity)
    clocks.entropy.advance(dt, entropy_rate)
    clocks.events.advance(event_count)
    clocks.observer.advance(dt, activity, sensitivity=0.3, reference=1.0)
    print(clocks.snapshot())
