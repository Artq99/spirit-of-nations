import pygame
from pygame import Surface
from pygame.event import Event

from son.core.resources import ResourceManager, ResourceInfo
from son.core.scenes import SceneBase
from son.gameplay._grid import Grid
from son.gameplay.screen_scroll import ScreenScrollHandler
from son.gameplay.types import GridUpdateFocusInfo
from son.gameplay.ui import UIGameplayController


RESOURCE_LIST = [
    ResourceInfo(name="grass", file="grass.png"),
    ResourceInfo(name="tribe", file="tribe.png")
]


class SceneGameplay(SceneBase):
    def __init__(self) -> None:
        super().__init__()
        self._resource_manager = ResourceManager(RESOURCE_LIST)
        self._resource_manager.load_resources()

        self._screen_scroll_handler = ScreenScrollHandler()
        self._ui_controller = UIGameplayController(self)

        self._grid = Grid((20, 20), self._resource_manager)

        self._saved_mouse_pos = (0, 0)
        self._saved_grid_update_focus_info: GridUpdateFocusInfo or None = None

    def pre_update(self, *args, **kwargs) -> None:
        self._saved_mouse_pos = pygame.mouse.get_pos()
        self._grid.pre_update()

    def update(self, *args, **kwargs) -> None:
        self._screen_scroll_handler.update(self._saved_mouse_pos)
        self._saved_grid_update_focus_info = self._grid.update_focus(self._saved_mouse_pos,
                                                                     self._screen_scroll_handler.get_delta())

    def handle_event(self, event: Event, *args, **kwargs) -> None:
        self._ui_controller.handle_event(event)

    def draw(self, surface: Surface, *args, **kwargs) -> None:
        surface.fill((0, 0, 0))
        self._grid.draw(surface, self._screen_scroll_handler.get_delta())
        self._ui_controller.draw(surface, self._saved_grid_update_focus_info.focused_cell_info, self._saved_mouse_pos)
