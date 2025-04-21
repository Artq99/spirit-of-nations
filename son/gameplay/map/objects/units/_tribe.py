from pygame import Surface

from son.core.resources import ResourceManager
from son.gameplay.map.objects._base import Movable


class Tribe(Movable):
    # TODO args and kwargs can be replaced with xml node argument later. see _forest.py
    # noinspection PyUnusedLocal
    def __init__(self, resource_manager: ResourceManager, *args, **kwargs) -> None:
        super().__init__("Tribe")
        self._surface = resource_manager.get_resource("unit.tribe")

        # Set the defaults for movement.
        self._max_movement_points = 5
        self._movement_points = 5

        # Update the info object with the new defaults.
        self._update_info()

    def _get_surface(self) -> Surface:
        return self._surface
