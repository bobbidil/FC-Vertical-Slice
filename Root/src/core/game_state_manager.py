from src.core.event_bus import EventBus
from src.data_models.events import GameStartedEvent, GamePausedEvent, GameResumedEvent, NewDayEvent


class GameStateManager:
    _instance = None

    game_status: str
    current_day: int
    current_rally: int

    def __init__(self):
        if self._instance is not None:
            raise ValueError("GameStateManager is a singleton. Use get_instance() instead.")
        self.game_status = "INITIALIZING"
        self.current_day = 1
        self.current_rally = 1
        # After initialization, set to RUNNING and publish GameStartedEvent
        self.set_game_status("RUNNING")

    @staticmethod
    def get_instance() -> 'GameStateManager':
        if GameStateManager._instance is None:
            GameStateManager._instance = GameStateManager()
        return GameStateManager._instance

    def set_game_status(self, new_status: str):
        old_status = self.game_status
        self.game_status = new_status
        event_bus = EventBus.get_instance()
        if new_status == "RUNNING" and old_status != "RUNNING":
            if old_status == "PAUSED":
                event = GameResumedEvent()
            else:
                event = GameStartedEvent()
            event_bus.publish(event)
        elif new_status == "PAUSED":
            event = GamePausedEvent()
            event_bus.publish(event)

    def advance_to_next_day(self):
        self.current_day += 1
        event_bus = EventBus.get_instance()
        event = NewDayEvent(day_number=self.current_day)
        event_bus.publish(event)
