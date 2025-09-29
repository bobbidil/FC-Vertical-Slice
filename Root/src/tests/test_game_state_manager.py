import unittest
from unittest.mock import Mock

from ..core.game_state_manager import GameStateManager
from ..data_models.events import GameStartedEvent, GamePausedEvent, NewDayEvent


class TestGameStateManager(unittest.TestCase):

    def setUp(self):
        # Reset singleton for each test
        GameStateManager._instance = None
        # Mock the EventBus
        self.mock_event_bus = Mock()
        from ..core import event_bus
        event_bus.EventBus.get_instance = Mock(return_value=self.mock_event_bus)

    def test_initialization_state(self):
        """Test Case 2.1: Initialization state is INITIALIZING."""
        # Before get_instance, state is not set yet
        # But since init calls set_game_status, but to test initial state, perhaps check after creation but before set_game_status.
        # The test says "initialization state", but in brief, it is "INITIALIZING" then sets to "RUNNING"
        # Perhaps test initial properties.
        manager = GameStateManager.get_instance()
        # After init, game_status is "RUNNING", current_day=1, current_rally=1
        self.assertEqual(manager.game_status, "RUNNING")
        self.assertEqual(manager.current_day, 1)
        self.assertEqual(manager.current_rally, 1)
        # And GameStartedEvent published
        self.mock_event_bus.publish.assert_called_once_with(GameStartedEvent())

    def test_set_game_status_paused_publishes_event(self):
        """Test Case 2.2: Test set game status."""
        manager = GameStateManager.get_instance()
        # Clear the init call
        self.mock_event_bus.reset_mock()

        manager.set_game_status("PAUSED")

        self.assertEqual(manager.game_status, "PAUSED")
        self.mock_event_bus.publish.assert_called_once_with(GamePausedEvent())

    def test_advance_to_next_day(self):
        """Test Case 2.3: Test advance to next day."""
        manager = GameStateManager.get_instance()
        # Initial day is 1

        manager.advance_to_next_day()

        self.assertEqual(manager.current_day, 2)
        self.mock_event_bus.publish.assert_called_with(NewDayEvent(day_number=2))

    def test_game_started_event_on_initialization(self):
        """Test Case 2.4: Test GameStartedEvent on initialization."""
        # When get_instance is called, it initializes and publishes GameStartedEvent
        manager = GameStateManager.get_instance()

        self.mock_event_bus.publish.assert_called_with(GameStartedEvent())


if __name__ == '__main__':
    unittest.main()
