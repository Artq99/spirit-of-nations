from dataclasses import dataclass


@dataclass
class CellInfo:
    """
    Info about a map cell.
    """
    grid_pos: tuple
    terrain_type: str


@dataclass
class MapInfo:
    """
    Info about the current state of a map.
    """
    focused_cell_info: CellInfo
