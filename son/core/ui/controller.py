import pygame
from pygame import Surface
from pygame.font import Font

from son.core.ui.constants import *


class UIController:

    def __init__(self) -> None:
        self.font = Font(pygame.font.get_default_font(), FONT_SIZE)

    def create_text_surface(self, text: str) -> Surface:
        return self.font.render(text, True, COLOR_TEXT, COLOR_BACKGROUND)
