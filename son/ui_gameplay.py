import pygame
from pygame import Surface
from pygame.font import Font
from pygame.event import Event
from pygame.locals import *


COLOR_TEXT = (255, 255, 255)
COLOR_BACKGROUND = (15, 15, 15)
FONT_SIZE = 16


class UIController:

    def __init__(self) -> None:
        self.font = Font(pygame.font.get_default_font(), FONT_SIZE)

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

    def draw(self, surface: Surface, mouse_pos: tuple, cell_info: dict) -> None:
        if self._is_cell_info_visible:
            self._show_cell_info(surface, cell_info, mouse_pos)

    def _show_cell_info(self, surface, cell_info, mouse_pos):
        cell_x, cell_y = cell_info["grid_pos"]
        terrain = cell_info["type"]

        position_text = "Position: {}:{}".format(cell_x, cell_y)
        position_surface = self._render_text(position_text)

        terrain_text = "Terrain: {}".format(terrain)
        terrain_surface = self._render_text(terrain_text)

        terrain_surface_size_x, terrain_surface_size_y = terrain_surface.get_size()
        terrain_surface_x, terrain_surface_y = terrain_surface.get_size()

        size_x = max(terrain_surface_size_x, terrain_surface_x) + 20
        size_y = terrain_surface_size_y + terrain_surface_y + 25

        info_surface = pygame.Surface((size_x, size_y))
        info_surface.fill(COLOR_BACKGROUND)

        info_surface.blit(position_surface, (10, 10))
        info_surface.blit(terrain_surface, (10, 10 + terrain_surface_size_y + 5))

        surface.blit(info_surface, mouse_pos)

    def _render_text(self, text: str) -> Surface:
        return self.font.render(text, True, COLOR_TEXT, COLOR_BACKGROUND)
