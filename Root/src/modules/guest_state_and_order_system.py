from src.core.event_bus import EventBus
from src.data_models.blend import Blend
from src.data_models.crme import Creme
from src.data_models.events import GuestReadyToOrderEvent, OrderPlacedEvent


class GuestStateAndOrderSystem:
    """
    P3 DSB-007: GuestStateAndOrderSystem
    Assign hardcoded Blend order and transition to WAITING_FOR_BLEND state.
    """

    def __init__(self):
        self.event_bus = EventBus.get_instance()
        self.event_bus.subscribe(GuestReadyToOrderEvent, self._handle_guest_ready_to_order)

    def _handle_guest_ready_to_order(self, event: GuestReadyToOrderEvent):
        """Handle GuestReadyToOrderEvent by assigning order and updating state."""
        guest = event.guest
        if guest.current_state == "ORDERING":
            guest.current_state = "WAITING_FOR_BLEND"
            # Assign hardcoded Blend order (placeholder per P5 CGE001 Blend)
            guest.order = Blend(
                blend_instance_id="order_01",
                creme=Creme(creme_id="standard_creme", base_quality=0.0),  # Placeholder
                flavors=[],  # Simplified: no flavors for slice
                final_quality_score=0.0,  # Placeholder to be set by ProductionSystem
                final_complexity_score=0.5  # Hardcoded per P4A
            )
            placed_event = OrderPlacedEvent(guest=guest)
            self.event_bus.publish(placed_event)
