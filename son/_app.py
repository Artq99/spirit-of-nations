import sys

import pygame
from pygame.locals import *
from pygame.time import Clock

from son.core.scenes import SceneManager
from son.core.vectors import VectorInt2D
from son.gameplay import SceneGameplay
from son.main_menu import SceneMainMenu


class SpiritOfNationsApp:
    """
    Application: Spirit of Nations.
    """

    def __init__(self, resolution: VectorInt2D) -> None:
        pygame.init()
        pygame.display.set_caption("Spirit of Nations")

        self._surface = pygame.display.set_mode(resolution, flags=SCALED)
        self._clock = Clock()

        self._scene_manager = SceneManager(initial_scene_name="MainMenu")
        self._scene_manager.register_scene("MainMenu", SceneMainMenu)
        self._scene_manager.register_scene("Gameplay", SceneGameplay)

    def run(self) -> None:
        while True:
            time_delta = self._clock.tick(30) * 0.001

            self._scene_manager.pre_update()
            self._scene_manager.update(time_delta=time_delta)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                self._scene_manager.handle_event(event)

            self._scene_manager.draw(self._surface)

            pygame.display.flip()
