"""
Manual Integration Debug Test
Step through the event chain manually to debug issues.
"""
import time

from src.core.event_bus import EventBus
from src.core.game_state_manager import GameStateManager
from src.core.player_inventory_service import PlayerInventoryService
from src.core.fervor_gauge_manager import FervorGaugeManager
from src.modules.guest_spawner_system import GuestSpawnerSystem
from src.modules.queue_management_system import QueueManagementSystem
from src.modules.guest_state_and_order_system import GuestStateAndOrderSystem
from src.modules.production_system import ProductionSystem
from src.modules.service_system import ServiceSystem
from src.modules.guest_satisfaction_evaluation_system import GuestSatisfactionEvaluationSystem
from src.modules.reward_system import RewardSystem
from src.data_models.events import *
from src.data_models.customer import Guest
from src.data_models.blend import Blend
from src.data_models.creme import Creme


def test_manual_integration():
    """Manual step-by-step integration test."""
    print("=== Manual Integration Debug Test ===")

    # Initialize all systems
    event_bus = EventBus.get_instance()
    game_state_manager = GameStateManager()
    inventory_service = PlayerInventoryService.get_instance()
    fervor_gauge_manager = FervorGaugeManager.get_instance()

    guest_spawner = GuestSpawnerSystem()
    queue_system = QueueManagementSystem()
    order_system = GuestStateAndOrderSystem()
    production_system = ProductionSystem()
    service_system = ServiceSystem()
    satisfaction_system = GuestSatisfactionEvaluationSystem()
    reward_system = RewardSystem()

    print("✅ All systems initialized")

    # Step 1: Publish GameStartedEvent
    print("\n--- Step 1: GameStartedEvent ---")
    game_started = GameStartedEvent()
    event_bus.publish(game_started)
    time.sleep(0.1)

    print("GameStateManager status:", game_state_manager.game_status)

    # Step 2: Check for GuestArrivedEvent
    print("\n--- Step 2: GuestArrivedEvent ---")
    guest_arrived = GuestArrivedEvent(guest=Guest(
        guest_instance_id="guest_01",
        level=0,
        current_state="ARRIVING",
        order=None,
        satisfaction_score=None
    ))
    event_bus.publish(guest_arrived)
    time.sleep(0.1)

    # Step 3: Check for GuestReadyToOrderEvent
    print("\n--- Step 3: GuestReadyToOrderEvent ---")
    ready_order = GuestReadyToOrderEvent(guest=Guest(
        guest_instance_id="guest_01",
        level=0,
        current_state="ORDERING",
        order=None,
        satisfaction_score=None
    ))
    event_bus.publish(ready_order)
    time.sleep(0.1)

    # Step 4: Check for OrderPlacedEvent (with blend)
    print("\n--- Step 4: OrderPlacedEvent ---")
    blend = Blend(
        blend_instance_id="order_01",
        creme=Creme(creme_id="standard_creme", base_quality=0.0),
        flavors=[],
        final_quality_score=0.0,
        final_complexity_score=0.5
    )
    guest_with_order = Guest(
        guest_instance_id="guest_01",
        level=0,
        current_state="WAITING_FOR_BLEND",
        order=blend,
        satisfaction_score=None
    )
    order_placed = OrderPlacedEvent(guest=guest_with_order)
    event_bus.publish(order_placed)
    time.sleep(0.1)

    # Step 5: Check for BlendProducedEvent
    print("\n--- Step 5: BlendProducedEvent ---")
    guest_produced = Guest(
        guest_instance_id="guest_01",
        level=0,
        current_state="WAITING_FOR_BLEND",
        order=Blend(
            blend_instance_id="order_01",
            creme=Creme(creme_id="standard_creme", base_quality=0.0),
            flavors=[],
            final_quality_score=0.8,
            final_complexity_score=0.5
        ),
        satisfaction_score=None
    )
    blend_produced = BlendProducedEvent(guest=guest_produced)
    event_bus.publish(blend_produced)
    time.sleep(0.1)

    # Step 6: Check for GuestServedEvent
    print("\n--- Step 6: GuestServedEvent ---")
    guest_served = GuestServedEvent(guest=Guest(
        guest_instance_id="guest_01",
        level=0,
        current_state="CONSUMING",
        order=Blend(
            blend_instance_id="order_01",
            creme=Creme(creme_id="standard_creme", base_quality=0.0),
            flavors=[],
            final_quality_score=0.8,
            final_complexity_score=0.5
        ),
        satisfaction_score=None
    ))
    event_bus.publish(guest_served)
    time.sleep(0.1)

    # Step 7: Check for SatisfactionCalculatedEvent (score should be 0.8 * 25 = 20.0)
    print("\n--- Step 7: SatisfactionCalculatedEvent ---")
    satisfaction_calculated = SatisfactionCalculatedEvent(guest=Guest(
        guest_instance_id="guest_01",
        level=0,
        current_state="CONSUMING",
        order=Blend(
            blend_instance_id="order_01",
            creme=Creme(creme_id="standard_creme", base_quality=0.0),
            flavors=[],
            final_quality_score=0.8,
            final_complexity_score=0.5
        ),
        satisfaction_score=20.0
    ))
    event_bus.publish(satisfaction_calculated)
    time.sleep(0.1)

    print("Final state check:")
    joy_notes = inventory_service.get_resource_quantity("joy_notes")
    fervor = fervor_gauge_manager.get_fervor_quantity(0)
    print(f"Joy Notes: {joy_notes}")
    print(f"Fervor: {fervor}")

    if joy_notes == 5 and fervor == 6:
        print("✓ SUCCESS: Manual integration test passed!")
        return True
    else:
        print("✗ FAILURE: Rewards not granted correctly")
        return False


if __name__ == "__main__":
    test_manual_integration()
