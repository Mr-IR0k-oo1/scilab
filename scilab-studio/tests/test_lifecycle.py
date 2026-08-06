"""
Unit tests for ApplicationLifecycle state transitions.
"""

import unittest
from core.event_bus import Event, EventBus
from core.lifecycle import ApplicationLifecycle, LifecycleState


class TestApplicationLifecycle(unittest.TestCase):

    def test_lifecycle_transitions_and_events(self):
        bus = EventBus()
        bus.initialize()
        bus.start()

        events = []

        def on_lifecycle(evt: Event) -> None:
            events.append(evt)

        bus.subscribe("lifecycle.state_changed", on_lifecycle)

        lifecycle = ApplicationLifecycle(event_bus=bus)
        self.assertEqual(lifecycle.state, LifecycleState.PRE_INIT)

        lifecycle.initialize()
        self.assertEqual(lifecycle.state, LifecycleState.INITIALIZING)

        lifecycle.start()
        self.assertEqual(lifecycle.state, LifecycleState.RUNNING)

        lifecycle.stop()
        self.assertEqual(lifecycle.state, LifecycleState.SHUTTING_DOWN)

        lifecycle.dispose()
        self.assertEqual(lifecycle.state, LifecycleState.STOPPED)

        self.assertEqual(len(events), 5)
        self.assertEqual(events[0].payload["new_state"], "INITIALIZING")
        self.assertEqual(events[-1].payload["new_state"], "STOPPED")


if __name__ == "__main__":
    unittest.main()
