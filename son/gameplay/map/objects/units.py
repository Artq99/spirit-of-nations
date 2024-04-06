"""
Module with definitions of the units.
"""
from son.core.resources import ResourceManager
from son.gameplay.map.objects._base import Movable


class Tribe(Movable):
    def __init__(self, resource_manager: ResourceManager) -> None:
        """
        Initialize Tribe.

        :param resource_manager: resource manager for the initialization of the surface
        """
        name = "Tribe"
        res_name = "tribe"

        super().__init__(name, res_name, resource_manager)

        self._max_movement_points = 5
        self._movement_points = 5
