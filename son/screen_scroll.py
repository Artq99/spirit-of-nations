import pygame.display

SCROLL_SPEED = 5
SCROLL_BORDER_SIZE = 10
MAX_SCROLL_OUT_OF_MAP = 50


class ScreenScrollHandler:
    # TODO Something's not right with scrolling right and down

    def __init__(self) -> None:
        self.resolution_x, self.resolution_y = pygame.display.get_window_size()
        self.delta_x = 0
        self.delta_y = 0

    def get_delta(self) -> tuple:
        return self.delta_x, self.delta_y

    def update(self, mouse_pos: tuple) -> None:
        mouse_pos_x, mouse_pos_y = mouse_pos
        # Scrolling left
        if mouse_pos_x <= SCROLL_BORDER_SIZE:
            self.delta_x = max((self.delta_x - SCROLL_SPEED), -MAX_SCROLL_OUT_OF_MAP)

        # Scrolling right
        elif mouse_pos_x >= (self.resolution_x - SCROLL_BORDER_SIZE):
            self.delta_x = min((self.delta_x + SCROLL_SPEED), self.resolution_x + MAX_SCROLL_OUT_OF_MAP)

        # Scrolling up
        if mouse_pos_y <= SCROLL_BORDER_SIZE:
            self.delta_y = max((self.delta_y - SCROLL_SPEED), -MAX_SCROLL_OUT_OF_MAP)

        # Scrolling down
        elif mouse_pos_y >= (self.resolution_y - SCROLL_BORDER_SIZE):
            self.delta_y = min((self.delta_y + SCROLL_SPEED), self.resolution_y + MAX_SCROLL_OUT_OF_MAP)
