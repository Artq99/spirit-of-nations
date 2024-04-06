from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class TextValuePair:
    """
    A pair of a label text and a value.
    """
    text: str
    value: str


@dataclass
class MapObjectInfo:
    """
    Info about a map object.
    """
    name: str
    attributes: Dict[str, TextValuePair] = field(default_factory=dict)


@dataclass
class CellInfo:
    """
    Info about a map cell.
    """
    grid_pos: tuple
    terrain_type: str
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
