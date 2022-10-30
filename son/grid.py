import pygame

from son.resources import ResourceManager


class GridCell:

    def __init__(self, pos, resource_manager: ResourceManager):
        self.pos = pos
        x = pos[0] * 50
        y = pos[1] * 50
        self.resource_manager = resource_manager
        self.rect = pygame.Rect(x, y, 50, 50)
        self.surface = self.resource_manager.get_resource("grass")

        self.focused = False

    def draw(self, destination_surface: pygame.Surface, delta):
        rect = pygame.Rect(self.rect.left - delta[0], self.rect.top - delta[1], 50, 50)
        destination_surface.blit(self.surface, rect)

        if self.focused:
            pygame.draw.rect(destination_surface, (100, 100, 0), rect, width=1)
            print(self.pos)

    def update_focus(self, mouse_pos, delta):
        rect = pygame.Rect(self.rect.left - delta[0], self.rect.top - delta[1], 50, 50)
        self.focused = rect.collidepoint(mouse_pos)


class Grid:

    def __init__(self, size, resource_manager):
        self.array = []

        for y in range(size[1]):
            row = []
            for x in range(size[0]):
                cell = GridCell((x, y), resource_manager)
                row.append(cell)

            self.array.append(row)

    def draw(self, destination_surface: pygame.Surface, delta):
        for row in self.array:
            for cell in row:
                cell.draw(destination_surface, delta)

    def update_focus(self, mouse_pos, delta):
        for row in self.array:
            for cell in row:
                cell.update_focus(mouse_pos, delta)
