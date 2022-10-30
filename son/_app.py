import sys
import pygame

from son.screen_scroll import ScreenScrollHandler
from son.grid import Grid


class SpiritOfNationsApp:

    def __init__(self, resolution):
        pygame.init()
        pygame.display.set_caption("Spirit of Nations")
        self.resolution = resolution
        self.surface = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()

    def run(self):
        screen_scroll_handler = ScreenScrollHandler(self.resolution)
        grid = Grid((20, 20))

        while True:
            mouse_pos = pygame.mouse.get_pos()
            screen_scroll_handler.update(mouse_pos)
            grid.update_focus(mouse_pos, screen_scroll_handler.get_delta())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.surface.fill((0, 0, 0))
            grid.draw(self.surface, screen_scroll_handler.get_delta())
            pygame.display.flip()
            self.clock.tick(30)
