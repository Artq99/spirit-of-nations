import sys
import pygame

from son.screen_scroll import ScreenScrollHandler
from son.resources import ResourceManager
from son.grid import Grid


class SpiritOfNationsApp:

    def __init__(self, resolution):
        pygame.init()
        pygame.display.set_caption("Spirit of Nations")
        self.resolution = resolution
        self.surface = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)

        self._is_cell_info_visible = False

    def run(self):
        screen_scroll_handler = ScreenScrollHandler(self.resolution)
        resource_manager = ResourceManager()
        resource_manager.load_resources()

        grid = Grid((20, 20), resource_manager)

        while True:
            mouse_pos = pygame.mouse.get_pos()
            screen_scroll_handler.update(mouse_pos)
            grid.update_focus(mouse_pos, screen_scroll_handler.get_delta())

            grid_info = grid.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    focused_cell_info = grid_info["focused_cell_info"]
                    if focused_cell_info is not None:
                        self._is_cell_info_visible = True

                elif event.type == pygame.MOUSEMOTION:
                    self._is_cell_info_visible = False

            self.surface.fill((0, 0, 0))
            grid.draw(self.surface, screen_scroll_handler.get_delta())

            if self._is_cell_info_visible:
                self._show_cell_info(grid_info["focused_cell_info"], mouse_pos)
            pygame.display.flip()
            self.clock.tick(30)

    def _show_cell_info(self, cell_info, mouse_pos):
        cell_x, cell_y = cell_info["grid_pos"]
        terrain = cell_info["type"]

        coords_surface = self.font.render("Coordinates: {}:{}".format(cell_x, cell_y), True, (255, 255, 255), (0, 0, 0))
        terrain_surface = self.font.render("Terrain: {}".format(terrain), True, (255, 255, 255), (0, 0, 0))

        coords_surface_x, coords_surface_y = coords_surface.get_size()
        terrain_surface_x, terrain_surface_y = terrain_surface.get_size()

        size_x = max(coords_surface_x, terrain_surface_x) + 20
        size_y = coords_surface_y + terrain_surface_y + 25

        info_surface = pygame.Surface((size_x, size_y))
        info_surface.fill((0, 0, 0))

        info_surface.blit(coords_surface, (10, 10))
        info_surface.blit(terrain_surface, (10, 10 + coords_surface_y + 5))

        self.surface.blit(info_surface, mouse_pos)
