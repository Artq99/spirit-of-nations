import pygame.font
from pygame import Surface
from pygame.font import Font

from son.core.ui.constants import FONT_SIZE, COLOR_TEXT, COLOR_BACKGROUND

if __name__ != "__main__":
    pygame.font.init()

_FONT = Font(pygame.font.get_default_font(), FONT_SIZE)


def create_text(text: str) -> Surface:
    """
    Create a surface with the given text on it.
    :param text: text to render
    """
    return _FONT.render(text, True, COLOR_TEXT, COLOR_BACKGROUND)
