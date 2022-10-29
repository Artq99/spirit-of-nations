import sys

import pygame


class GridCell:

    def __init__(self, pos):
        x = pos[0] * 50
        y = pos[1] * 50
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = (0, 200, 0)
        self.surface = pygame.surface.Surface((50, 50))
        self.surface.fill(self.color)

        self.focused = False

    def draw(self, destination_surface: pygame.Surface):
        destination_surface.blit(self.surface, self.rect.topleft)

        if self.focused:
            pygame.draw.rect(destination_surface, (100, 100, 0), (self.rect.topleft, (50, 50)), width=1)


class Grid:

    def __init__(self, size):
        self.array = []

        for y in range(size[1]):
            row = []
            for x in range(size[0]):
                cell = GridCell((x, y))
                row.append(cell)

            self.array.append(row)

    def draw(self, destination_surface: pygame.Surface):
        for row in self.array:
            for cell in row:
                cell.draw(destination_surface)

    def update(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            for row in self.array:
                for cell in row:
                    cell.focused = cell.rect.collidepoint(event.pos)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((800, 600))

    surface = pygame.display.get_surface()
    grid = Grid((10, 10))

    while True:
        grid.draw(surface)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            grid.update(event)
