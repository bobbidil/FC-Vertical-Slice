from src.core.event_bus import EventBus
from src.data_models.events import BlendProducedEvent, GuestServedEvent


class ServiceSystem:
    """
    P3 DSB-009: ServiceSystem
    Transition guest to CONSUMING state and publish GuestServedEvent.
    """

    def __init__(self):
        self.event_bus = EventBus.get_instance()
        self.event_bus.subscribe(BlendProducedEvent, self._handle_blend_produced)

    def _handle_blend_produced(self, event: BlendProducedEvent):
        """Handle BlendProducedEvent by transitioning to service complete."""
        guest = event.guest
        guest.current_state = "CONSUMING"
        served_event = GuestServedEvent(guest=guest)
        self.event_bus.publish(served_event)
