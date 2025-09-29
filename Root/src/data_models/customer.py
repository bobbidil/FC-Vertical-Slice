import dataclasses

from .blend import Blend


@dataclasses.dataclass
class Guest:
    guest_instance_id: str
    level: int  # P5 IC001, level 0 for "Greys"
    current_state: str  # "ARRIVING", "QUEUING", "ORDERING", "WAITING_FOR_BLEND", "CONSUMING", "LEAVING"
    order: Blend | None = None  # P5 CGE001 Blend order for guest
    satisfaction_score: float | None = None  # Calculated after service per CA001
