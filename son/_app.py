import sys

import pygame
from pygame.locals import *
from pygame.time import Clock

from son.resources import ResourceManager
from son.scenes import SceneGameplay, SceneManager


class SpiritOfNationsApp:

    def __init__(self, resolution: tuple) -> None:
        pygame.init()
        pygame.display.set_caption("Spirit of Nations")
        self._surface = pygame.display.set_mode(resolution)
        self._clock = Clock()

        self._resource_manager = ResourceManager()
        self._resource_manager.load_resources()

        self._scene_manager = SceneManager(self._resource_manager)

    def run(self) -> None:
        self._scene_manager.load_scene("MainMenu")

        while True:
            self._scene_manager.active_scene.pre_update()
            self._scene_manager.active_scene.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                self._scene_manager.active_scene.handle_event(event)

            self._scene_manager.active_scene.draw(self._surface)

            pygame.display.flip()
            self._clock.tick(30)

            self._scene_manager.handle_scene_finish()
