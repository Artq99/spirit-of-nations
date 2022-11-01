import pygame
from pygame import Surface
from pygame.event import Event
from pygame.font import Font

from son.core.scenes import SceneBase
from son.core.ui.constants import *


class UIController:

    def __init__(self, owner: SceneBase) -> None:
        self.owner = owner
        self.font = Font(pygame.font.get_default_font(), FONT_SIZE)
        self.widgets = []

    def create_text_surface(self, text: str) -> Surface:
        return self.font.render(text, True, COLOR_TEXT, COLOR_BACKGROUND)

    def pre_update(self, *args, **kwargs) -> None:
        for widget in self.widgets:
            widget.pre_update(*args, **kwargs)

    def update(self, mouse_pos: tuple, *args, **kwargs) -> None:
        for widget in self.widgets:
            widget.update(mouse_pos, *args, **kwargs)

    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        for widget in self.widgets:
            if widget.handle_event(event, *args, **kwargs):
                return True

        return False

    def draw(self, surface: Surface, *args, **kwargs) -> None:
        for widget in self.widgets:
            widget.draw(surface, *args, **kwargs)
