from pygame import Surface
from pygame.event import Event
from pygame.locals import *

from son.core.scenes import SceneBase


class SceneMainMenu(SceneBase):

    def handle_event(self, event: Event) -> None:
        if event.type == MOUSEBUTTONUP:
            self.has_finished = True
            self.next_scene_name = "Gameplay"

    def draw(self, surface: Surface) -> None:
        surface.fill((0, 0, 0))
