import dataclasses
from typing import List

from .creme import Creme
from .flavor import Flavor


@dataclasses.dataclass
class Blend:
    blend_instance_id: str  # P5 CGE001, unique identifier
    creme: Creme  # P5 CGE001, base creme used
    flavors: List[Flavor]  # P5 CGE001, flavors included
    final_quality_score: float  # P5 CA025, quality after PS008 calculation
    final_complexity_score: float  # P5 MP004, complexity score
