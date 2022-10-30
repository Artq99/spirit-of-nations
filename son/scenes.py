import pygame.mouse
from pygame.locals import *
from pygame import Surface
from pygame.event import Event

from son.grid import Grid
from son.resources import ResourceManager
from son.screen_scroll import ScreenScrollHandler
from son.types import GridUpdateFocusInfo
from son.ui_gameplay import UIController


class SceneBase:
    def __init__(self):
        self.has_finished = False
        self.next_scene_name = None

    def pre_update(self):
        pass

    def update(self):
        pass

    def handle_event(self, event: Event):
        pass

    def draw(self, surface: Surface):
        pass


class SceneMainMenu(SceneBase):
    def handle_event(self, event: Event):
        if event.type == MOUSEBUTTONUP:
            self.has_finished = True
            self.next_scene_name = "Gameplay"

    def draw(self, surface: Surface):
        surface.fill((0, 0, 0))


class SceneGameplay(SceneBase):
    def __init__(self, resource_manager: ResourceManager):
        super().__init__()
        self._screen_scroll_handler = ScreenScrollHandler()
        self._ui_controller = UIController()

        self._grid = Grid((20, 20), resource_manager)

        self._saved_mouse_pos = (0, 0)
        self._saved_grid_update_focus_info: GridUpdateFocusInfo or None = None

    def pre_update(self):
        self._saved_mouse_pos = pygame.mouse.get_pos()
        self._grid.pre_update()

    def update(self):
        self._screen_scroll_handler.update(self._saved_mouse_pos)
        self._saved_grid_update_focus_info = self._grid.update_focus(self._saved_mouse_pos,
                                                                     self._screen_scroll_handler.get_delta())

    def handle_event(self, event: Event):
        self._ui_controller.handle_event(event)

    def draw(self, surface: Surface):
        surface.fill((0, 0, 0))
        self._grid.draw(surface, self._screen_scroll_handler.get_delta())
        self._ui_controller.draw(surface, self._saved_grid_update_focus_info.focused_cell_info, self._saved_mouse_pos)


class SceneManager:
    def __init__(self, resource_manager: ResourceManager):
        self.active_scene = SceneBase()

        self._resource_manager = resource_manager

    def load_scene(self, name: str) -> None:
        if name == "MainMenu":
            self.active_scene = SceneMainMenu()
        elif name == "Gameplay":
            self.active_scene = SceneGameplay(self._resource_manager)

    def handle_scene_finish(self):
        if self.active_scene.has_finished:
            self.load_scene(self.active_scene.next_scene_name)
