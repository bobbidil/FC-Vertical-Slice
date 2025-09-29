import pytest
from unittest.mock import Mock, patch

from src.modules.guest_satisfaction_evaluation_system import GuestSatisfactionEvaluationSystem
from src.data_models.customer import Guest
from src.data_models.blend import Blend
from src.data_models.creme import Creme
from src.data_models.events import GuestServedEvent, SatisfactionCalculatedEvent


class TestGuestSatisfactionEvaluationSystem:
    """P4A Tests 11.1-11.2: GuestSatisfactionEvaluationSystem"""

    @pytest.fixture
    def mock_event_bus(self):
        return Mock()

    @pytest.fixture
    def system(self, mock_event_bus):
        with patch('src.core.event_bus.EventBus.get_instance', return_value=mock_event_bus):
            system = GuestSatisfactionEvaluationSystem()
            return system

    def test_11_1_successful_satisfaction_calculation(self, system, mock_event_bus):
        """Test Case 11.1: Test successful satisfaction calculation"""
        # Given: Guest with final quality score of 0.8
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
            current_state="CONSUMING",
            order=blend,
            satisfaction_score=None
        )
        event = GuestServedEvent(guest=guest)

        # When: GuestServedEvent published
        system._handle_guest_served(event)

        # Then: SatisfactionCalculatedEvent published with score = 0.8 * 25 = 20.0
        mock_event_bus.publish.assert_called_once()
        call_args = mock_event_bus.publish.call_args[0][0]
        assert isinstance(call_args, SatisfactionCalculatedEvent)

        updated_guest = call_args.guest
        assert updated_guest.satisfaction_score == 20.0

    def test_11_2_error_handling_for_missing_order_data(self, system, mock_event_bus):
        """Test Case 11.2: Test error handling for missing order data"""
        # Given: Guest with no order
        guest = Guest(
            guest_instance_id="guest_01",
            level=0,
            current_state="CONSUMING",
            order=None,
            satisfaction_score=None
        )
        event = GuestServedEvent(guest=guest)

        # When: GuestServedEvent with missing order data published
        # Then: System raises ValueError
        with pytest.raises(ValueError):
            system._handle_guest_served(event)
