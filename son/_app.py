import sys
import pygame
from pygame.locals import *
from pygame.time import Clock

from son.screen_scroll import ScreenScrollHandler
from son.resources import ResourceManager
from son.grid import Grid
from son.ui_gameplay import UIController


class SpiritOfNationsApp:

    def __init__(self, resolution: tuple) -> None:
        pygame.init()
        pygame.display.set_caption("Spirit of Nations")
        self.resolution = resolution
        self.surface = pygame.display.set_mode(resolution)
        self.clock = Clock()

        self._is_cell_info_visible = False

    def run(self) -> None:
        resource_manager = ResourceManager()
        resource_manager.load_resources()

        screen_scroll_handler = ScreenScrollHandler(self.resolution)
        ui_controller = UIController()

        grid = Grid((20, 20), resource_manager)

        while True:
            # Pre-update
            grid.pre_update()

            # Update
            mouse_pos = pygame.mouse.get_pos()

            screen_scroll_handler.update(mouse_pos)
            grid_update_focus_info = grid.update_focus(mouse_pos, screen_scroll_handler.get_delta())

            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                ui_controller.handle_event(event)

            # Draw
            self.surface.fill((0, 0, 0))
            grid.draw(self.surface, screen_scroll_handler.get_delta())
            ui_controller.draw(self.surface, grid_update_focus_info.focused_cell_info, mouse_pos)

            pygame.display.flip()
            self.clock.tick(30)
