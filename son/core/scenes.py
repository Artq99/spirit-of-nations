from typing import Type, Dict

import pygame.event
from pygame import Surface
from pygame.event import Event

from son.core.base import Lifecycle
from son.core.events import SCENE_FINISHED
from son.core.utils.decorators import override


def finish_scene(next_scene_name: str = "") -> None:
    """
    Finish the current scene.

    :param next_scene_name: name of a scene that should be loaded as next
    """
    pygame.event.post(Event(SCENE_FINISHED, {"next_scene_name": next_scene_name}))


class SceneBase(Lifecycle):
    """
    Base class for all scenes.
    """
    pass


class SceneNotRegisteredError(Exception):
    """
    Error raised on attempt of loading a scene that has not been registered.
    """

    def __init__(self, scene_name: str) -> None:
        super().__init__("The scene has not been registered: {}".format(scene_name))


class SceneManager(Lifecycle):
    """
    Scene Manager.
    """

    def __init__(self, initial_scene_name: str = ""):
        self._registered_scenes: Dict[str, Type[SceneBase]] = dict()
        self._active_scene: SceneBase
        self._next_scene_name: str or None = initial_scene_name

    @override
    def pre_update(self, *args, **kwargs) -> None:
        if self._next_scene_name is not None:
            self._load_scene(self._next_scene_name)
            self._next_scene_name = None

        self._active_scene.pre_update(*args, **kwargs)

    def _load_scene(self, name: str) -> None:
        if name not in self._registered_scenes.keys():
            raise SceneNotRegisteredError(name)

        scene_class = self._registered_scenes[name]
        self._active_scene = scene_class()

    @override
    def update(self, *args, **kwargs) -> None:
        self._active_scene.update(*args, **kwargs)

    @override
    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        if event.type == SCENE_FINISHED:
            self._next_scene_name = event.next_scene_name
            return True

        return self._active_scene.handle_event(event, *args, **kwargs)

    @override
    def draw(self, destination_surface: Surface, *args, **kwargs) -> None:
        self._active_scene.draw(destination_surface, *args, **kwargs)

    def register_scene(self, name: str, scene_class: Type[SceneBase]) -> None:
        """
        Register a scene.

        :param name: name for a new scene
        :param scene_class: class of a new scene
        """
        self._registered_scenes[name] = scene_class
