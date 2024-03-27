from dataclasses import dataclass
from typing import List


@dataclass
class MapObjectInfo:
    """
    Info about a map object.
    """
    name: str


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
