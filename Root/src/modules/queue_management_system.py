from src.core.event_bus import EventBus
from src.data_models.events import GuestArrivedEvent, GuestReadyToOrderEvent


class QueueManagementSystem:
    """
    P3 DSB-006: QueueManagementSystem (CQMS)
    Process arriving guest to ORDERING state on GuestArrivedEvent.
    """

    def __init__(self):
        self.event_bus = EventBus.get_instance()
        self.event_bus.subscribe(GuestArrivedEvent, self._handle_guest_arrived)

    def _handle_guest_arrived(self, event: GuestArrivedEvent):
        """Handle GuestArrivedEvent by transitioning to ORDERING state."""
        guest = event.guest
        if guest.current_state == "ARRIVING":
            guest.current_state = "ORDERING"
            ready_event = GuestReadyToOrderEvent(guest=guest)
            self.event_bus.publish(ready_event)
