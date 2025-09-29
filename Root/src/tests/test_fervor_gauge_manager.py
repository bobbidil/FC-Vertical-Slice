import unittest
from unittest.mock import Mock

from ..core.fervor_gauge_manager import FervorGaugeManager
from ..data_models.events import FervorUpdatedEvent


class TestFervorGaugeManager(unittest.TestCase):

    def setUp(self):
        # Reset singleton for each test
        FervorGaugeManager._instance = None
        # Mock the EventBus
        self.mock_event_bus = Mock()
        from ..core import event_bus
        event_bus.EventBus.get_instance = Mock(return_value=self.mock_event_bus)

    def test_add_fervor_updates_gauge_and_publishes_event(self):
        """Test 5.1: Add Fervor updates gauge and publishes event."""
        manager = FervorGaugeManager.get_instance()
        manager.add_fervor(0, 6)

        self.assertEqual(manager.get_fervor(0), 6)
        self.mock_event_bus.publish.assert_called_once()
        event_called = self.mock_event_bus.publish.call_args[0][0]
        self.assertIsInstance(event_called, FervorUpdatedEvent)
        self.assertEqual(event_called.level, 0)
        self.assertEqual(event_called.new_value, 6)

    def test_add_fervor_overflow_caps_at_max(self):
        """Test add Fervor caps at MAX_FERVOR and publishes event."""
        manager = FervorGaugeManager.get_instance()
        manager.add_fervor(0, 200)

        self.assertEqual(manager.get_fervor(0), 100.0)
        self.mock_event_bus.publish.assert_called_once()
        event_called = self.mock_event_bus.publish.call_args[0][0]
        self.assertEqual(event_called.new_value, 100.0)

    def test_get_fervor_nonexistent_returns_zero(self):
        manager = FervorGaugeManager.get_instance()

        self.assertEqual(manager.get_fervor(1), 0.0)

    def test_add_fervor_multiple_levels(self):
        manager = FervorGaugeManager.get_instance()
        manager.add_fervor(0, 10)
        manager.add_fervor(1, 20)

        self.assertEqual(manager.get_fervor(0), 10)
        self.assertEqual(manager.get_fervor(1), 20)


if __name__ == '__main__':
    unittest.main()
