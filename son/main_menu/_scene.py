import pygame.mouse
from pygame import Surface
from pygame.event import Event

from son.core.scenes import SceneBase
from son.main_menu.ui import MainMenuUIController


class SceneMainMenu(SceneBase):

    def __init__(self):
        super().__init__()

        self._ui_controller = MainMenuUIController(self)

    def pre_update(self, *args, **kwargs) -> None:
        self._ui_controller.pre_update(*args, **kwargs)

    def update(self, *args, **kwargs) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self._ui_controller.update(mouse_pos, *args, **kwargs)

    def handle_event(self, event: Event, *args, **kwargs) -> None:
        self._ui_controller.handle_event(event, *args, **kwargs)

    def draw(self, surface: Surface, *args, **kwargs) -> None:
        surface.fill((0, 0, 0))
        self._ui_controller.draw(surface, *args, **kwargs)
