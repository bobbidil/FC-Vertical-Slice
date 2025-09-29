import unittest
from unittest.mock import Mock

from ..core.player_inventory_service import PlayerInventoryService
from ..data_models.events import ResourceUpdatedEvent


class TestPlayerInventoryService(unittest.TestCase):

    def setUp(self):
        # Reset singleton for each test
        PlayerInventoryService._instance = None
        # Mock the EventBus
        self.mock_event_bus = Mock()
        from ..core import event_bus
        event_bus.EventBus.get_instance = Mock(return_value=self.mock_event_bus)

    def test_add_resource_joy_notes_updates_inventory_and_publishes_event(self):
        """Test Case 3.1: add JoyNotes updates inventory and publishes event."""
        service = PlayerInventoryService.get_instance()
        service.add_resource("JoyNotes", 5)

        self.assertEqual(service.get_resource_quantity("JoyNotes"), 5)
        self.mock_event_bus.publish.assert_called_once()
        event_called = self.mock_event_bus.publish.call_args[0][0]
        self.assertIsInstance(event_called, ResourceUpdatedEvent)
        self.assertEqual(event_called.resource_key, "JoyNotes")
        self.assertEqual(event_called.new_quantity, 5)
        self.assertEqual(event_called.delta, 5)

    def test_add_resource_auxiliary_updates_inventory_and_publishes_event(self):
        """Test Case 3.2: add AuxiliaryResource updates inventory."""
        service = PlayerInventoryService.get_instance()
        service.add_resource("AuxiliaryResource", 10)

        self.assertEqual(service.get_resource_quantity("AuxiliaryResource"), 10)
        self.mock_event_bus.publish.assert_called_once()
        event_called = self.mock_event_bus.publish.call_args[0][0]
        self.assertIsInstance(event_called, ResourceUpdatedEvent)
        self.assertEqual(event_called.resource_key, "AuxiliaryResource")
        self.assertEqual(event_called.new_quantity, 10)
        self.assertEqual(event_called.delta, 10)

    def test_get_resource_quantity_joy_notes(self):
        """Test Case 3.3: get_resource_quantity for JoyNotes."""
        service = PlayerInventoryService.get_instance()
        service.add_resource("JoyNotes", 5)

        self.assertEqual(service.get_resource_quantity("JoyNotes"), 5)

    def test_has_sufficient_resources_joy_notes_true(self):
        """Test Case 3.4: has_sufficient_resources true for JoyNotes."""
        service = PlayerInventoryService.get_instance()
        service.add_resource("JoyNotes", 5)

        self.assertTrue(service.has_sufficient_resources("JoyNotes", 5))

    def test_has_sufficient_resources_joy_notes_false(self):
        """Test Case 3.5: has_sufficient_resources false for JoyNotes."""
        service = PlayerInventoryService.get_instance()
        service.add_resource("JoyNotes", 5)

        self.assertFalse(service.has_sufficient_resources("JoyNotes", 10))

    def test_add_resource_negative_quantity_raises_value_error(self):
        """Test Case 3.x: negative quantity raises ValueError."""
        service = PlayerInventoryService.get_instance()

        with self.assertRaises(ValueError) as context:
            service.add_resource("JoyNotes", -1)

        self.assertEqual(str(context.exception), "Quantity must be non-negative")

    def test_get_resource_quantity_nonexistent_returns_zero(self):
        service = PlayerInventoryService.get_instance()

        self.assertEqual(service.get_resource_quantity("Nonexistent"), 0.0)


if __name__ == '__main__':
    unittest.main()
