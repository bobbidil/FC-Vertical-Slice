import pytest
from unittest.mock import Mock, patch

from src.modules.guest_state_and_order_system import GuestStateAndOrderSystem
from src.data_models.customer import Guest
from src.data_models.blend import Blend
from src.data_models.creme import Creme
from src.data_models.events import GuestReadyToOrderEvent, OrderPlacedEvent


class TestGuestStateAndOrderSystem:
    """P4A Tests 7.1-7.2: GuestStateAndOrderSystem"""

    @pytest.fixture
    def mock_event_bus(self):
        return Mock()

    @pytest.fixture
    def system(self, mock_event_bus):
        with patch('src.core.event_bus.EventBus.get_instance', return_value=mock_event_bus):
            system = GuestStateAndOrderSystem()
            return system

    def test_7_1_assign_order_and_update_state(self, system, mock_event_bus):
        """Test Case 7.1: Test assign order and update state"""
        # Given: Guest in ORDERING state
        guest = Guest(
            guest_instance_id="guest_01",
            level=0,
            current_state="ORDERING",
            order=None,
            satisfaction_score=None
        )
        event = GuestReadyToOrderEvent(guest=guest)

        # When: GuestReadyToOrderEvent published
        system._handle_guest_ready_to_order(event)

        # Then: OrderPlacedEvent published with guest state to "WAITING_FOR_BLEND" and order assigned
        mock_event_bus.publish.assert_called_once()
        call_args = mock_event_bus.publish.call_args[0][0]
        assert isinstance(call_args, OrderPlacedEvent)

        updated_guest = call_args.guest
        assert updated_guest.current_state == "WAITING_FOR_BLEND"
        assert updated_guest.order is not None
        assert isinstance(updated_guest.order, Blend)
        assert updated_guest.order.blend_instance_id == "order_01"
        assert updated_guest.order.final_quality_score == 0.0  # Placeholder

    def test_7_2_ignore_invalid_events(self, system, mock_event_bus):
        """Test Case 7.2: Test ignore invalid events"""
        # Given: Non-GuestReadyToOrderEvent
        from src.data_models.events import GameTickEvent
        event = GameTickEvent(delta_time=1.0)

        # When: Invalid event published
        system._handle_guest_ready_to_order(event)

        # Then: No events published
        mock_event_bus.publish.assert_not_called()
