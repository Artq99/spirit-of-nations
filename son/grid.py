import pygame

from son.resources import ResourceManager


GRID_CELL_SIZE = 50
GRID_CELL_SIZE_XY = (GRID_CELL_SIZE, GRID_CELL_SIZE)
COLOR_FOCUS = (100, 100, 0)


class GridCell:

    @staticmethod
    def _calc_pixel_pos(grid_pos):
        grid_pos_x, grid_pos_y = grid_pos
        return grid_pos_x * GRID_CELL_SIZE, grid_pos_y * GRID_CELL_SIZE

    def __init__(self, grid_pos, resource_manager: ResourceManager):
        self.grid_pos = grid_pos
        self.pixel_pos = GridCell._calc_pixel_pos(grid_pos)

        self.surface = resource_manager.get_resource("grass")
        self.rect = pygame.Rect(self.pixel_pos, GRID_CELL_SIZE_XY)

        self.focused = False

    def draw(self, destination_surface: pygame.Surface, delta):
        rect_delta = self._get_rect_with_delta(delta)
        destination_surface.blit(self.surface, rect_delta)

        if self.focused:
            pygame.draw.rect(destination_surface, COLOR_FOCUS, rect_delta, width=1)

    def update_focus(self, mouse_pos, delta):
        rect_delta = self._get_rect_with_delta(delta)
        self.focused = rect_delta.collidepoint(mouse_pos)

    def _get_rect_with_delta(self, delta):
        delta_x, delta_y = delta
        delta_pos = (self.rect.left - delta_x, self.rect.top - delta_y)
        return pygame.Rect(delta_pos, GRID_CELL_SIZE_XY)


class Grid:

    @staticmethod
    def _create_array(size, resource_manger):
        size_x, size_y = size
        array = []

        for y in range(size_y):
            row = []
            for x in range(size_x):
                cell = GridCell((x, y), resource_manger)
                row.append(cell)
            array.append(row)

        return array

    def __init__(self, size, resource_manager):
        self._array = Grid._create_array(size, resource_manager)

    def draw(self, destination_surface: pygame.Surface, delta):
        for row in self._array:
            for cell in row:
                cell.draw(destination_surface, delta)

    def update_focus(self, mouse_pos, delta):
        for row in self._array:
            for cell in row:
                cell.update_focus(mouse_pos, delta)
