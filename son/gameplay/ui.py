import pygame
from pygame import Surface
from pygame.event import Event
from pygame.locals import *

from son.core.scenes import SceneBase
from son.core.ui.controller import UIController
from son.gameplay.types import CellInfo

COLOR_TEXT = (255, 255, 255)
COLOR_BACKGROUND = (15, 15, 15)
FONT_SIZE = 16


# TODO Refactor
class UIGameplayController(UIController):

    def __init__(self, owner: SceneBase) -> None:
        super().__init__(owner)

        self._is_cell_info_visible = False

    def handle_event(self, event: Event) -> bool:
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 3:
                self._is_cell_info_visible = True
                return True

        elif event.type == MOUSEMOTION:
            self._is_cell_info_visible = False
            return False

        return False

    def draw(self, surface: Surface, cell_info: CellInfo, mouse_pos: tuple) -> None:
        if self._is_cell_info_visible and cell_info is not None:
            self._show_cell_info(surface, cell_info, mouse_pos)

    def _show_cell_info(self, surface: Surface, cell_info: CellInfo, mouse_pos: tuple):
        cell_x, cell_y = cell_info.grid_pos
        terrain = cell_info.terrain_type

        position_text = "Position: {}:{}".format(cell_x, cell_y)
        position_surface = self.create_text_surface(position_text)

        terrain_text = "Terrain: {}".format(terrain)
        terrain_surface = self.create_text_surface(terrain_text)

        terrain_surface_size_x, terrain_surface_size_y = terrain_surface.get_size()
        terrain_surface_x, terrain_surface_y = terrain_surface.get_size()

        size_x = max(terrain_surface_size_x, terrain_surface_x) + 20
        size_y = terrain_surface_size_y + terrain_surface_y + 25

        info_surface = pygame.Surface((size_x, size_y))
        info_surface.fill(COLOR_BACKGROUND)

        info_surface.blit(position_surface, (10, 10))
        info_surface.blit(terrain_surface, (10, 10 + terrain_surface_size_y + 5))

        surface.blit(info_surface, mouse_pos)
