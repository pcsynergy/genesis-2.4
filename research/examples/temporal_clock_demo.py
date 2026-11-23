"""Demonstrate parameter, relational, and observer clock accumulation."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.temporal import TemporalLayer

clock = TemporalLayer(relational_gain=0.35, observer_gain=0.2,
                      reference_activity=1.0)
print("step,parameter_time,relational_time,observer_time,activity_integral")
for step, activity in enumerate((0.2, 0.8, 1.5, 2.5, 1.0), start=1):
    state = clock.advance(0.2, activity)
    print(f"{step},{state['parameter_time']:.3f},"
          f"{state['relational_time']:.3f},{state['observer_time']:.3f},"
          f"{state['accumulated_activity']:.3f}")
