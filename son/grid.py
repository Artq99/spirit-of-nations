import pygame
from pygame.locals import *
from pygame import Surface

from son.resources import ResourceManager
from son.types import CellInfo, GridUpdateFocusInfo

GRID_CELL_SIZE = 50
GRID_CELL_SIZE_XY = (GRID_CELL_SIZE, GRID_CELL_SIZE)
COLOR_FOCUS = (100, 100, 0)


class GridCell:

    @staticmethod
    def _calc_pixel_pos(grid_pos: tuple) -> tuple:
        grid_pos_x, grid_pos_y = grid_pos
        return grid_pos_x * GRID_CELL_SIZE, grid_pos_y * GRID_CELL_SIZE

    def __init__(self, grid_pos: tuple, resource_manager: ResourceManager) -> None:
        self.grid_pos = grid_pos

        self.terrain_type = "grass"
        self.surface = resource_manager.get_resource("grass")

        self._pixel_pos = GridCell._calc_pixel_pos(grid_pos)

    def get_rect_with_delta(self, delta: tuple) -> Rect:
        delta_x, delta_y = delta
        pixel_pos_x, pixel_pos_y = self._pixel_pos
        delta_pos = (pixel_pos_x - delta_x, pixel_pos_y - delta_y)
        return pygame.Rect(delta_pos, GRID_CELL_SIZE_XY)

    def get_cell_info(self) -> CellInfo:
        return CellInfo(
            grid_pos=self.grid_pos,
            terrain_type=self.terrain_type
        )

    def draw(self, destination_surface: Surface, delta: tuple) -> None:
        rect_delta = self.get_rect_with_delta(delta)
        destination_surface.blit(self.surface, rect_delta)

    def draw_focus_marker(self, destination_surface: Surface, delta: tuple) -> None:
        rect_delta = self.get_rect_with_delta(delta)
        pygame.draw.rect(destination_surface, COLOR_FOCUS, rect_delta, width=1)


class Grid:

    @staticmethod
    def _create_array(size, resource_manger: ResourceManager) -> list:
        size_x, size_y = size
        array = []

        for y in range(size_y):
            row = []
            for x in range(size_x):
                cell = GridCell((x, y), resource_manger)
                row.append(cell)
            array.append(row)

        return array

    def __init__(self, size: tuple, resource_manager: ResourceManager) -> None:
        self._array = Grid._create_array(size, resource_manager)
        self._focused_cell: GridCell or None = None

    def pre_update(self) -> None:
        self._focused_cell = None

    def update_focus(self, mouse_pos: tuple, delta: tuple) -> GridUpdateFocusInfo:
        for row in self._array:
            for cell in row:
                if cell.get_rect_with_delta(delta).collidepoint(mouse_pos):
                    self._focused_cell = cell

        return GridUpdateFocusInfo(
            focused_cell_info=self._focused_cell.get_cell_info() if self._focused_cell is not None else None
        )

    def draw(self, destination_surface: Surface, delta: tuple) -> None:
        for row in self._array:
            for cell in row:
                cell.draw(destination_surface, delta)

        if self._focused_cell is not None:
            self._focused_cell.draw_focus_marker(destination_surface, delta)
