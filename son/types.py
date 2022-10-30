from dataclasses import dataclass


@dataclass
class CellInfo:
    grid_pos: tuple
    terrain_type: str


@dataclass
class GridUpdateFocusInfo:
    focused_cell_info: CellInfo
