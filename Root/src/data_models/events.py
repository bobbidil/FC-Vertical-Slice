import dataclasses
import datetime

# Forward references for type annotations


@dataclasses.dataclass
class Event:
    timestamp: datetime = dataclasses.field(default_factory=datetime.datetime.now)


@dataclasses.dataclass
class ResourceUpdatedEvent(Event):
    resource_key: str
    new_quantity: float
    delta: float


@dataclasses.dataclass
class GameStartedEvent(Event):
    pass


@dataclasses.dataclass
class GamePausedEvent(Event):
    pass


@dataclasses.dataclass
class GameResumedEvent(Event):
    pass


@dataclasses.dataclass
class NewDayEvent(Event):
    day_number: int


@dataclasses.dataclass
class GameTickEvent(Event):
    delta_time: float


@dataclasses.dataclass
class FervorUpdatedEvent(Event):
    level: int
    new_value: float


@dataclasses.dataclass
class GuestArrivedEvent(Event):
    guest: "Guest"


@dataclasses.dataclass
class GuestReadyToOrderEvent(Event):
    guest: "Guest"


@dataclasses.dataclass
class OrderPlacedEvent(Event):
    guest: "Guest"


@dataclasses.dataclass
class BlendProducedEvent(Event):
    guest: "Guest"


@dataclasses.dataclass
class GuestServedEvent(Event):
    guest: "Guest"


@dataclasses.dataclass
class SatisfactionCalculatedEvent(Event):
    guest: "Guest"


@dataclasses.dataclass
class RewardGrantedEvent(Event):
    guest_id: str
    satisfaction_score: float
    rewards_granted: dict[str, float]
