import dataclasses


@dataclasses.dataclass
class Creme:
    creme_id: str  # P5 TF005, unique identifier
    base_quality: float  # P5 PS008, base quality for blend calculation
