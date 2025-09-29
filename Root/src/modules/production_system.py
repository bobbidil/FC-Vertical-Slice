from src.core.event_bus import EventBus
from src.data_models.events import OrderPlacedEvent, BlendProducedEvent


class ProductionSystem:
    """
    P3 DSB-008: ProductionSystem
    Instantly "produce" Blend with hardcoded quality=0.8 and complexity=0.5.
    """

    def __init__(self):
        self.event_bus = EventBus.get_instance()
        self.event_bus.subscribe(OrderPlacedEvent, self._handle_order_placed)

    def _handle_order_placed(self, event: OrderPlacedEvent):
        """Handle OrderPlacedEvent by producing Blend with hardcoded stats."""
        guest = event.guest
        if guest.order is not None:
            # Produce Blend with hardcoded final scores (per P4A, PS008)
            guest.order.final_quality_score = 0.8  # Hardcoded per P4A
            guest.order.final_complexity_score = 0.5  # Hardcoded per P4A
            produced_event = BlendProducedEvent(guest=guest)
            self.event_bus.publish(produced_event)
