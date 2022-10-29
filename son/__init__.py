import sys
import pygame

from son.grid import Grid


class SpiritOfNationsApp:

    def __init__(self):
        pygame.init()
        pygame.display.set_mode((800, 600))

    def run(self):
        surface = pygame.display.get_surface()
        screen_rect = surface.get_rect()
        grid = Grid((20, 20))

        delta_x = 0
        delta_y = 0

        while True:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] <= 10:
                delta_x = max((delta_x - 0.1), -50)
            if mouse_pos[0] >= (screen_rect.size[0] - 10):
                delta_x = min((delta_x + 0.1), screen_rect.size[0] + 50)
            if mouse_pos[1] <= 10:
                delta_y = max((delta_y - 0.1), -50)
            if mouse_pos[1] >= (screen_rect.size[1] - 10):
                delta_y = min((delta_y + 0.1), screen_rect.size[1] + 50)

            surface.fill((0, 0, 0))
            grid.draw(surface, (delta_x, delta_y))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                grid.update(event, (delta_x, delta_y))
