from src.core.event_bus import EventBus
from src.data_models.events import GuestServedEvent, SatisfactionCalculatedEvent


class GuestSatisfactionEvaluationSystem:
    """
    P3 DSB-010: GuestSatisfactionEvaluationSystem
    Calculate satisfaction score = final_quality_score * 25 (simplified per P4A).
    """

    def __init__(self):
        self.event_bus = EventBus.get_instance()
        self.event_bus.subscribe(GuestServedEvent, self._handle_guest_served)

    def _handle_guest_served(self, event: GuestServedEvent):
        """Handle GuestServedEvent by calculating satisfaction score."""
        guest = event.guest

        if guest.order is None:
            raise ValueError("Guest order data is missing")

        # Simplified calculation: score = final_quality_score * 25
        # Per P4A notes and P5 CA001 simplifications
        satisfaction_score = guest.order.final_quality_score * 25
        guest.satisfaction_score = satisfaction_score

        calculated_event = SatisfactionCalculatedEvent(guest=guest)
        self.event_bus.publish(calculated_event)
