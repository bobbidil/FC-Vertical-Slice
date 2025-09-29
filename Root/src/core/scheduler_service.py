import threading
import time

from src.core.event_bus import EventBus
from src.data_models.events import GameTickEvent


class SchedulerService:
    _instance = None

    tick_interval: float = 1.0
    _running = False
    _thread = None

    def __init__(self):
        if self._instance is not None:
            raise ValueError("SchedulerService is a singleton. Use get_instance() instead.")
        self._running = False

    @staticmethod
    def get_instance() -> 'SchedulerService':
        if SchedulerService._instance is None:
            SchedulerService._instance = SchedulerService()
        return SchedulerService._instance

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._tick_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)

    def _tick_loop(self):
        while self._running:
            time.sleep(self.tick_interval)
            if not self._running:
                break
            event = GameTickEvent(delta_time=self.tick_interval)
            EventBus.get_instance().publish(event)
