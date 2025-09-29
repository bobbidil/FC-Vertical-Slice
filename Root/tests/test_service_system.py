import pytest
from unittest.mock import Mock, patch

from src.modules.service_system import ServiceSystem
from src.data_models.customer import Guest
from src.data_models.blend import Blend
from src.data_models.creme import Creme
from src.data_models.events import BlendProducedEvent, GuestServedEvent


class TestServiceSystem:
    """P4A Tests 10.1-10.2: ServiceSystem"""

    @pytest.fixture
    def mock_event_bus(self):
        return Mock()

    @pytest.fixture
    def system(self, mock_event_bus):
        with patch('src.core.event_bus.EventBus.get_instance', return_value=mock_event_bus):
            system = ServiceSystem()
            return system

    def test_10_1_process_served_guest(self, system, mock_event_bus):
        """Test Case 10.1: Test process served guest"""
        # Given: Guest with produced blend
        blend = Blend(
            blend_instance_id="order_01",
            creme=Creme(creme_id="standard_creme", base_quality=0.0),
            flavors=[],
            final_quality_score=0.8,
            final_complexity_score=0.5
        )
        guest = Guest(
            guest_instance_id="guest_01",
            level=0,
            current_state="WAITING_FOR_BLEND",
            order=blend,
            satisfaction_score=None
        )
        event = BlendProducedEvent(guest=guest)

        # When: BlendProducedEvent published
        system._handle_blend_produced(event)

        # Then: GuestServedEvent published
        mock_event_bus.publish.assert_called_once()
        call_args = mock_event_bus.publish.call_args[0][0]
        assert isinstance(call_args, GuestServedEvent)

        assert call_args.guest.current_state == "CONSUMING"

    def test_10_2_update_guest_state(self, system, mock_event_bus):
        """Test Case 10.2: Test update guest state"""
        # Given: Guest in WAITING_FOR_BLEND state
        guest = Guest(
            guest_instance_id="guest_01",
            level=0,
            current_state="WAITING_FOR_BLEND",
            order=None,
            satisfaction_score=None
        )
        event = BlendProducedEvent(guest=guest)

        # When: BlendProducedEvent published
        system._handle_blend_produced(event)

        # Then: Guest state set to "CONSUMING"
        assert isinstance(mock_event_bus.publish.call_args[0][0], GuestServedEvent)
        served_event = mock_event_bus.publish.call_args[0][0]
        assert served_event.guest.current_state == "CONSUMING"
