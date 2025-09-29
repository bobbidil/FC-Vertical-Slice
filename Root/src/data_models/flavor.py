import dataclasses


@dataclasses.dataclass
class Flavor:
    flavor_id: str  # P5 GDX001, unique identifier
    genre: str  # P5 GDX001, e.g., Sweet, Sour, Savory
    rarity: str  # P5 GDX001, e.g., Common, Rare, Epic
    element: str  # P5 GDX001, e.g., Fire, Water, Earth
