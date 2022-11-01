import pygame
from pygame import Surface
from pygame.event import Event
from pygame.locals import *

from son.core.ui.controller import UIController
from son.core.ui.constants import *


class Button:

    def __init__(self, owner: UIController) -> None:
        self.owner = owner
        self._text = "Button text"

        self._create_surface()
        self._rect = self._surface.get_rect()

        self._is_focused = False

        self._on_click = None
        self._on_click_args = list()
        self._on_click_kwargs = dict()

    def _create_surface(self) -> None:
        text_surface = self.owner.create_text_surface(self._text)
        text_surface_size_x, text_surface_size_y = text_surface.get_size()

        surface_size = (text_surface_size_x + 10, text_surface_size_y + 10)
        self._surface = Surface(surface_size)
        self._surface.fill(COLOR_BACKGROUND)
        self._surface.blit(text_surface, (5, 5))

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

        self._create_surface()
        self._rect.size = self._surface.get_size()

    @property
    def pos(self):
        return self._rect.topleft

    @pos.setter
    def pos(self, value):
        self._rect.topleft = value

    def register_on_click(self, action: object, *args, **kwargs):
        self._on_click = action
        self._on_click_args = args
        self._on_click_kwargs = kwargs

    def pre_update(self, *args, **kwargs) -> None:
        pass

    def update(self, mouse_pos: tuple) -> None:
        self._is_focused = self._rect.collidepoint(mouse_pos)

    def handle_event(self, event: Event) -> bool:
        if self._on_click is not None and self._is_focused and event.type == MOUSEBUTTONUP and event.button == 1:
            self._on_click(*self._on_click_args, **self._on_click_kwargs)

    def draw(self, surface: Surface):
        surface.blit(self._surface, self._rect)

        border_color = COLOR_FOCUS if self._is_focused else COLOR_BORDER
        pygame.draw.rect(surface, border_color, self._rect, width=1)
