import unittest
from unittest.mock import Mock

import dataclasses

from ..core.event_bus import EventBus
from ..data_models.events import Event


@dataclasses.dataclass
class TestEvent(Event):
    data: str


@dataclasses.dataclass
class TestEventA(Event):
    data: str


@dataclasses.dataclass
class TestEventB(Event):
    data: str


class TestEventBus(unittest.TestCase):

    def setUp(self):
        # Reset singleton for each test
        EventBus._instance = None

    def test_subscribe_and_publish_correct_payload(self):
        """Test Case 1.1: Successful subscription and publication with correct payload."""
        bus = EventBus.get_instance()
        callback = Mock()
        test_event = TestEvent(data="test_payload")

        bus.subscribe(TestEvent, callback)
        bus.publish(test_event)

        callback.assert_called_once_with(test_event)

    def test_event_type_isolation(self):
        """Test Case 1.2: Correct event type isolation."""
        bus = EventBus.get_instance()
        callback = Mock()

        bus.subscribe(TestEventA, callback)
        test_event_b = TestEventB(data="b_payload")

        bus.publish(test_event_b)

        callback.assert_not_called()

    def test_multiple_subscribers_for_single_event(self):
        """Test Case 1.3: Multiple subscribers for a single event."""
        bus = EventBus.get_instance()
        callback1 = Mock()
        callback2 = Mock()
        callback3 = Mock()
        test_event = TestEventA(data="multi_payload")

        bus.subscribe(TestEventA, callback1)
        bus.subscribe(TestEventA, callback2)
        bus.subscribe(TestEventA, callback3)

        bus.publish(test_event)

        callback1.assert_called_once_with(test_event)
        callback2.assert_called_once_with(test_event)
        callback3.assert_called_once_with(test_event)

    def test_singleton_instance(self):
        """Test Case 1.4: Singleton ensures single instance."""
        bus1 = EventBus.get_instance()
        bus2 = EventBus.get_instance()

        self.assertIs(bus1, bus2)

    def test_error_handling_invalid_callback(self):
        """Test Case 1.5: Test error handling for invalid callback."""
        bus = EventBus.get_instance()

        with self.assertRaises(ValueError) as context:
            bus.subscribe(TestEvent, 123)  # non-callable callback

        self.assertEqual(str(context.exception), "Callback must be callable")

    def test_error_handling_invalid_event_type(self):
        """Test Case 1.6: Test error handling for invalid event type."""
        bus = EventBus.get_instance()
        callback = Mock()

        with self.assertRaises(ValueError) as context:
            bus.subscribe(None, callback)  # None as event type

        self.assertEqual(str(context.exception), "Invalid event type")


if __name__ == '__main__':
    unittest.main()
