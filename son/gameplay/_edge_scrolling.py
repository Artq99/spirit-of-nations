import pygame
from pygame.event import Event
from pygame.locals import *

from son.core.base import Lifecycle
from son.core.events import EDGE_SCROLL
from son.core.utils.decorators import override

SCROLL_SPEED = 5
SCROLL_BORDER_SIZE = 10
MAX_SCROLL_OUT_OF_MAP = 50


class EdgeScrollingController(Lifecycle):
    """
    Controller for edge scrolling.
    """

    def __init__(self, map_pixel_size: tuple[int, int]) -> None:
        resolution = pygame.display.get_window_size()

        self._delta: tuple[int, int] = (0, 0)
        self._delta_change: tuple[int, int] = (0, 0)

        self._right_edge = resolution[0] - SCROLL_BORDER_SIZE
        self._bottom_edge = resolution[1] - SCROLL_BORDER_SIZE

        self._max_scroll_right = map_pixel_size[0] - resolution[0] + MAX_SCROLL_OUT_OF_MAP
        self._max_scroll_bottom = map_pixel_size[1] - resolution[1] + MAX_SCROLL_OUT_OF_MAP

    @override
    def update(self, *args, **kwargs) -> None:
        # TODO apply time delta
        if self._delta_change[0] != 0 or self._delta_change[1] != 0:
            delta_x, delta_y = self._delta
            delta_change_x, delta_change_y = self._delta_change

            if delta_change_x == -1:
                delta_x = max((delta_x - SCROLL_SPEED), -MAX_SCROLL_OUT_OF_MAP)
            elif delta_change_x == 1:
                delta_x = min((delta_x + SCROLL_SPEED), self._max_scroll_right)

            if delta_change_y == -1:
                delta_y = max((delta_y - SCROLL_SPEED), -MAX_SCROLL_OUT_OF_MAP)
            elif delta_change_y == 1:
                delta_y = min((delta_y + SCROLL_SPEED), self._max_scroll_bottom)

            self._delta = delta_x, delta_y
            mouse_pos = pygame.mouse.get_pos()

            pygame.event.post(Event(EDGE_SCROLL, {"delta": self._delta, "pos": mouse_pos}))

    @override
    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        if event.type == MOUSEMOTION:
            mouse_pos_x, mouse_pos_y = event.pos
            delta_change_x = 0
            delta_change_y = 0

            if mouse_pos_x <= SCROLL_BORDER_SIZE:
                delta_change_x = -1

            elif mouse_pos_x >= self._right_edge:
                delta_change_x = 1

            if mouse_pos_y <= SCROLL_BORDER_SIZE:
                delta_change_y = -1

            elif mouse_pos_y >= self._bottom_edge:
                delta_change_y = 1

            self._delta_change = delta_change_x, delta_change_y

        return False
