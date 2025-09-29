from src.core.event_bus import EventBus
from src.data_models.events import FervorUpdatedEvent


class FervorGaugeManager:
    _instance = None
    MAX_FERVOR = 100.0

    def __init__(self):
        if self._instance is not None:
            raise ValueError("FervorGaugeManager is a singleton. Use get_instance() instead.")
        self._fervor_gauges: dict[int, float] = {}

    @staticmethod
    def get_instance() -> 'FervorGaugeManager':
        if FervorGaugeManager._instance is None:
            FervorGaugeManager._instance = FervorGaugeManager()
        return FervorGaugeManager._instance

    def add_fervor(self, level: int, amount: float):
        if level not in self._fervor_gauges:
            self._fervor_gauges[level] = 0.0
        new_value = min(self.MAX_FERVOR, self._fervor_gauges[level] + amount)
        self._fervor_gauges[level] = new_value
        # Publish the update
        event = FervorUpdatedEvent(level=level, new_value=new_value)
        EventBus.get_instance().publish(event)

    def get_fervor(self, level: int) -> float:
        return self._fervor_gauges.get(level, 0.0)
