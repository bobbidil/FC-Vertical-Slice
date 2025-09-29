import pytest
from unittest.mock import Mock, patch

from src.modules.production_system import ProductionSystem
from src.data_models.customer import Guest
from src.data_models.blend import Blend
from src.data_models.creme import Creme
from src.data_models.events import OrderPlacedEvent, BlendProducedEvent


class TestProductionSystem:
    """P4A Tests 9.1-9.2: ProductionSystem"""

    @pytest.fixture
    def mock_event_bus(self):
        return Mock()

    @pytest.fixture
    def system(self, mock_event_bus):
        with patch('src.core.event_bus.EventBus.get_instance', return_value=mock_event_bus):
            system = ProductionSystem()
            return system

    def test_9_1_produce_blend_with_hardcoded_stats(self, system, mock_event_bus):
        """Test Case 9.1: Test produce Blend with hardcoded stats"""
        # Given: Guest with Blend order
        blend = Blend(
            blend_instance_id="order_01",
            creme=Creme(creme_id="standard_creme", base_quality=0.0),
            flavors=[],
            final_quality_score=0.0,
            final_complexity_score=0.5
        )
        guest = Guest(
            guest_instance_id="guest_01",
            level=0,
            current_state="WAITING_FOR_BLEND",
            order=blend,
            satisfaction_score=None
        )
        event = OrderPlacedEvent(guest=guest)

        # When: OrderPlacedEvent published
        system._handle_order_placed(event)

        # Then: BlendProducedEvent published with quality=0.8 and complexity=0.5
        mock_event_bus.publish.assert_called_once()
        call_args = mock_event_bus.publish.call_args[0][0]
        assert isinstance(call_args, BlendProducedEvent)

        updated_guest = call_args.guest
        assert updated_guest.order is not None
        assert updated_guest.order.final_quality_score == 0.8
        assert updated_guest.order.final_complexity_score == 0.5

    def test_9_2_ignore_invalid_events(self, system, mock_event_bus):
        """Test Case 9.2: Test ignore invalid events"""
        # Given: Non-OrderPlacedEvent
        from src.data_models.events import GameTickEvent
        event = GameTickEvent(delta_time=1.0)

        # When: Invalid event published
        system._handle_order_placed(event)

        # Then: No events published
        mock_event_bus.publish.assert_not_called()
