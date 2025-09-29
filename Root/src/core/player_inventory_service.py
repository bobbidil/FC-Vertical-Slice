from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .event_bus import EventBus

from src.core.event_bus import EventBus
from src.data_models.events import ResourceUpdatedEvent


class PlayerInventoryService:
    _instance = None

    def __init__(self):
        if self._instance is not None:
            raise ValueError("PlayerInventoryService is a singleton. Use get_instance() instead.")
        self._resources: dict[str, float] = {}

    @staticmethod
    def get_instance() -> 'PlayerInventoryService':
        if PlayerInventoryService._instance is None:
            PlayerInventoryService._instance = PlayerInventoryService()
        return PlayerInventoryService._instance

    def add_resource(self, resource_key: str, quantity: float):
        if quantity < 0:
            raise ValueError("Quantity must be non-negative")
        current = self._resources.get(resource_key, 0.0)
        new_quantity = current + quantity
        self._resources[resource_key] = new_quantity
        event_bus = EventBus.get_instance()
        event = ResourceUpdatedEvent(
            resource_key=resource_key,
            new_quantity=new_quantity,
            delta=quantity
        )
        event_bus.publish(event)

    def get_resource_quantity(self, resource_key: str) -> float:
        return self._resources.get(resource_key, 0.0)

    def has_sufficient_resources(self, resource_key: str, quantity: float) -> bool:
        return self.get_resource_quantity(resource_key) >= quantity

    def spend_resource(self, resource_key: str, quantity: float) -> bool:
        if not self.has_sufficient_resources(resource_key, quantity):
            return False
        current = self._resources[resource_key]
        new_quantity = current - quantity
        self._resources[resource_key] = new_quantity
        event_bus = EventBus.get_instance()
        event = ResourceUpdatedEvent(
            resource_key=resource_key,
            new_quantity=new_quantity,
            delta=-quantity
        )
        event_bus.publish(event)
        return True
