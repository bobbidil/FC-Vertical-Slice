from typing import Callable, Type


class EventBus:
    _instance = None
    _listener_registry: dict[Type, list[Callable]] = {}

    def __init__(self):
        if self._instance is not None:
            raise ValueError("EventBus is a singleton. Use get_instance() instead.")
        self._listener_registry = {}

    @staticmethod
    def get_instance() -> 'EventBus':
        if EventBus._instance is None:
            EventBus._instance = EventBus()
        return EventBus._instance

    def subscribe(self, event_type: Type, callback: Callable):
        if not isinstance(event_type, type):
            raise ValueError("Invalid event type")
        if not callable(callback):
            raise ValueError("Callback must be callable")
        if event_type not in self._listener_registry:
            self._listener_registry[event_type] = []
        self._listener_registry[event_type].append(callback)

    def publish(self, event):
        from src.data_models.events import Event
        if not isinstance(event, Event):
            raise ValueError("Event must be an instance of Event")
        event_type = type(event)
        if event_type in self._listener_registry:
            for callback in self._listener_registry[event_type]:
                callback(event)
