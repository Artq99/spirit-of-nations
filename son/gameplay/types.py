from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class MapObjectInfo:
    """
    Info about a map object.
    """
    name: str
    type: str
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class CellInfo:
    """
    Info about a map cell.
    """
    grid_pos: tuple
    terrain_type: str
    movement_cost: str
    objects: List[MapObjectInfo]


@dataclass
class MapInfo:
    """
    Info about the current state of a map.
    """
    focused_cell_info: CellInfo


@dataclass
class TurnInfo:
    """
    Info about the current turn.
    """
    week: str
    month: str
    year: str
