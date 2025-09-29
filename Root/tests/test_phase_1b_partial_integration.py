"""
Partial Integration Test for Phase 1B: Game Logic Foundations

Spawn guest and process through queue/order/production.
Verify BlendProducedEvent published with valid Blend.
"""
import pytest
from unittest.mock import Mock

from src.core.event_bus import EventBus
from src.core.game_state_manager import GameStateManager
from src.modules.guest_spawner_system import GuestSpawnerSystem
from src.modules.queue_management_system import QueueManagementSystem
from src.modules.guest_state_and_order_system import GuestStateAndOrderSystem
from src.modules.production_system import ProductionSystem
from src.data_models.events import GameStartedEvent, BlendProducedEvent


class TestPhase1BPartialIntegration:
    """Partial integration test for Phase 1B systems."""

    @pytest.fixture
    def event_bus(self):
        return EventBus.get_instance()

    @pytest.fixture
    def systems(self, event_bus):
        """Initialize all Phase 1B systems."""
        game_state_manager = GameStateManager()
        guest_spawner = GuestSpawnerSystem()
        queue_system = QueueManagementSystem()
        order_system = GuestStateAndOrderSystem()
        production_system = ProductionSystem()

        return {
            'game_state_manager': game_state_manager,
            'guest_spawner': guest_spawner,
            'queue_system': queue_system,
            'order_system': order_system,
            'production_system': production_system
        }

    def test_1b_partial_integration(self, systems, event_bus):
        """Test full chain: GameStarted -> BlendProduced."""
        # Mock to capture events
        event_published = []

        original_publish = event_bus.publish
        def mock_publish(event):
            event_published.append(event)
            return original_publish(event)

        event_bus.publish = mock_publish

        try:
            # When: Game starts (publish GameStartedEvent)
            game_started = GameStartedEvent()
            event_bus.publish(game_started)

            # Then: Full chain completes with BlendProducedEvent
            blend_produced_events = [e for e in event_published if isinstance(e, BlendProducedEvent)]
            assert len(blend_produced_events) == 1

            event = blend_produced_events[0]
            guest = event.guest

            # Verify guest and blend state
            assert guest.guest_instance_id == "guest_01"
            assert guest.level == 0
            assert guest.current_state == "WAITING_FOR_BLEND"  # Not updated yet in this phase
            assert guest.order is not None
            assert guest.order.blend_instance_id == "order_01"
            assert guest.order.final_quality_score == 0.8
            assert guest.order.final_complexity_score == 0.5

            print("✓ Phase 1B Partial Integration Test PASSED")

        finally:
            # Restore original publish
            event_bus.publish = original_publish
