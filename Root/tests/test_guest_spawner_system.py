import pytest
from unittest.mock import Mock, patch

from src.modules.guest_spawner_system import GuestSpawnerSystem
from src.data_models.customer import Guest
from src.data_models.events import GameStartedEvent, GuestArrivedEvent


class TestGuestSpawnerSystem:
    """P4A Tests 5.1-5.2: GuestSpawnerSystem"""

    @pytest.fixture
    def mock_event_bus(self):
        return Mock()

    @pytest.fixture
    def system(self, mock_event_bus):
        with patch('src.core.event_bus.EventBus.get_instance', return_value=mock_event_bus):
            system = GuestSpawnerSystem()
            return system

    def test_5_1_spawn_guest_on_game_started_event(self, system, mock_event_bus):
        """Test Case 5.1: Test spawn guest on GameStartedEvent"""
        # Given: System initialized with EventBus
        assert system is not None

        # When: GameStartedEvent is published
        event = GameStartedEvent()
        system._handle_game_started(event)

        # Then: GuestArrivedEvent published with Level 0 Guest
        mock_event_bus.publish.assert_called_once()
        call_args = mock_event_bus.publish.call_args[0][0]
        assert isinstance(call_args, GuestArrivedEvent)

        guest = call_args.guest
        assert isinstance(guest, Guest)
        assert guest.guest_instance_id == "guest_01"  # Hardcoded
        assert guest.level == 0  # Level 0 "Greys"
        assert guest.current_state == "ARRIVING"
        assert guest.order is None
        assert guest.satisfaction_score is None

    def test_5_2_single_guest_spawn(self, system, mock_event_bus):
        """Test Case 5.2: Test single guest spawn"""
        # Given: System initialized

        # When: GameStartedEvent published twice
        event1 = GameStartedEvent()
        event2 = GameStartedEvent()
        system._handle_game_started(event1)
        system._handle_game_started(event2)

        # Then: Only one GuestArrivedEvent published (vertical slice scope)
        assert mock_event_bus.publish.call_count == 1
