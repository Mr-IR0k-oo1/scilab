"""
Unit tests for EventBus publish-subscribe mechanism and wildcard matching.
"""

import unittest
from core.event_bus import Event, EventBus


class TestEventBus(unittest.TestCase):

    def test_event_bus_subscribe_publish(self):
        bus = EventBus()
        bus.initialize()
        bus.start()

        received_events = []

        def handler(event: Event) -> None:
            received_events.append(event)

        bus.subscribe("workspace.opened", handler)

        evt = Event(topic="workspace.opened", payload={"name": "TestProj"}, sender="test")
        bus.publish(evt)

        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0].topic, "workspace.opened")
        self.assertEqual(received_events[0].payload["name"], "TestProj")

        bus.stop()
        bus.dispose()

    def test_event_bus_wildcard_subscription(self):
        bus = EventBus()
        bus.initialize()
        bus.start()

        received_events = []

        def handler(event: Event) -> None:
            received_events.append(event)

        bus.subscribe("workspace.*", handler)

        bus.publish(Event(topic="workspace.opened", payload={}, sender="test"))
        bus.publish(Event(topic="workspace.closed", payload={}, sender="test"))
        bus.publish(Event(topic="ui.theme_changed", payload={}, sender="test"))

        self.assertEqual(len(received_events), 2)
        self.assertEqual(received_events[0].topic, "workspace.opened")
        self.assertEqual(received_events[1].topic, "workspace.closed")

        bus.stop()
        bus.dispose()

    def test_event_bus_unsubscribe(self):
        bus = EventBus()
        bus.initialize()
        bus.start()

        received_events = []

        def handler(event: Event) -> None:
            received_events.append(event)

        bus.subscribe("test.topic", handler)
        bus.publish(Event(topic="test.topic", payload={}, sender="test"))
        self.assertEqual(len(received_events), 1)

        bus.unsubscribe("test.topic", handler)
        bus.publish(Event(topic="test.topic", payload={}, sender="test"))
        self.assertEqual(len(received_events), 1)

        bus.stop()
        bus.dispose()


if __name__ == "__main__":
    unittest.main()
