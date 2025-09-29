import pytest
from unittest.mock import Mock, patch

from src.modules.queue_management_system import QueueManagementSystem
from src.data_models.customer import Guest
from src.data_models.events import GuestArrivedEvent, GuestReadyToOrderEvent


class TestQueueManagementSystem:
    """P4A Tests 6.1-6.2: QueueManagementSystem (CQMS)"""

    @pytest.fixture
    def mock_event_bus(self):
        return Mock()

    @pytest.fixture
    def system(self, mock_event_bus):
        with patch('src.core.event_bus.EventBus.get_instance', return_value=mock_event_bus):
            system = QueueManagementSystem()
            return system

    def test_6_1_process_guest_to_ordering_state(self, system, mock_event_bus):
        """Test Case 6.1: Test process guest to ORDERING state"""
        # Given: Guest with ARRIVING state
        guest = Guest(
            guest_instance_id="guest_01",
            level=0,
            current_state="ARRIVING",
            order=None,
            satisfaction_score=None
        )
        event = GuestArrivedEvent(guest=guest)

        # When: GuestArrivedEvent published
        system._handle_guest_arrived(event)

        # Then: GuestReadyToOrderEvent published with guest state set to "ORDERING"
        mock_event_bus.publish.assert_called_once()
        call_args = mock_event_bus.publish.call_args[0][0]
        assert isinstance(call_args, GuestReadyToOrderEvent)

        updated_guest = call_args.guest
        assert updated_guest.current_state == "ORDERING"
        assert updated_guest.guest_instance_id == "guest_01"
        assert updated_guest.level == 0

    def test_6_2_ignore_invalid_events(self, system, mock_event_bus):
        """Test Case 6.2: Test ignore invalid events"""
        # Given: Non-GuestArrivedEvent
        from src.data_models.events import GameTickEvent
        event = GameTickEvent(delta_time=1.0)

        # When: Invalid event published
        system._handle_guest_arrived(event)

        # Then: No events published
        mock_event_bus.publish.assert_not_called()
