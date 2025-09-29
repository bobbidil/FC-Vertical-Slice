from src.core.event_bus import EventBus
from src.data_models.customer import Guest
from src.data_models.events import GameStartedEvent, GuestArrivedEvent


class GuestSpawnerSystem:
    """
    P3 DSB-005: GuestSpawnerSystem
    Spawn hardcoded Level 0 guest on game start.
    """

    def __init__(self):
        self.event_bus = EventBus.get_instance()
        self.event_bus.subscribe(GameStartedEvent, self._handle_game_started)
        self.has_spawned = False  # Track if we've spawned for vertical slice

    def _handle_game_started(self, event: GameStartedEvent):
        """Handle GameStartedEvent by spawning guest."""
        if not self.has_spawned:
            guest = Guest(
                guest_instance_id="guest_01",  # Hardcoded for slice
                level=0,  # Level 0 "Greys" per P5 T011
                current_state="ARRIVING",
                order=None,
                satisfaction_score=None
            )
            arrived_event = GuestArrivedEvent(guest=guest)
            self.event_bus.publish(arrived_event)
            self.has_spawned = True  # Only spawn one for vertical slice
