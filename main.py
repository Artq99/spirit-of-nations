import sys

import pygame


class GridCell:

    def __init__(self, pos):
        self.pos = pos
        x = pos[0] * 50
        y = pos[1] * 50
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = (0, 200, 0)
        self.surface = pygame.surface.Surface((50, 50))
        self.surface.fill(self.color)

        self.focused = False

    def draw(self, destination_surface: pygame.Surface, delta):
        rect = pygame.Rect(self.rect.left - delta[0], self.rect.top - delta[1], 50, 50)
        destination_surface.blit(self.surface, rect)

        if self.focused:
            pygame.draw.rect(destination_surface, (100, 100, 0), rect, width=1)
            print(self.pos)

    def update(self, event: pygame.event.Event, delta):
        rect = pygame.Rect(self.rect.left - delta[0], self.rect.top - delta[1], 50, 50)
        self.focused = rect.collidepoint(event.pos)


class Grid:

    def __init__(self, size):
        self.array = []

        for y in range(size[1]):
            row = []
            for x in range(size[0]):
                cell = GridCell((x, y))
                row.append(cell)

            self.array.append(row)

    def draw(self, destination_surface: pygame.Surface, delta):
        for row in self.array:
            for cell in row:
                cell.draw(destination_surface, delta)

    def update(self, event: pygame.event.Event, delta):
        if event.type == pygame.MOUSEMOTION:
            for row in self.array:
                for cell in row:
                    cell.update(event, delta)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((800, 600))

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
