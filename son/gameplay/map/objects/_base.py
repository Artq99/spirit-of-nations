from pygame import Surface
from pygame.event import Event
from pygame.rect import Rect

from son.core.base import Lifecycle
from son.core.events import START_TURN
from son.core.resources import ResourceManager
from son.core.utils.decorators import override
from son.core.utils.functions import check_str_empty, check_none
from son.gameplay._types import MapObjectInfo


class MapObject(Lifecycle):
    """
    Base class for all map objects.
    """

    def __init__(self, name: str, res_name: str, resource_manager: ResourceManager) -> None:
        """
        Initialize MapObject.

        :param name: in-game name of the object
        :param res_name: name of the resource that should be loaded as the surface
        :param resource_manager: resource manager for the initialization of the surface
        """
        check_str_empty(name, "name")
        check_str_empty(res_name, "res_name")
        check_none(resource_manager, "resource_manager")

        self._name: str = name
        self._surface: Surface = resource_manager.get_resource(res_name)

        self._info = MapObjectInfo(name=self._name, type="Generic Map Object")

    @property
    def info(self) -> MapObjectInfo:
        """
        Information about this map object.
        """
        return self._info

    @override
    def draw(self, destination_surface: Surface, *args, **kwargs) -> None:
        # The cell_rect must be passed by the map in the keyword arguments.
        # If it's not then someone's done a very bad job.
        try:
            cell_rect: Rect = kwargs["cell_rect"]
        except KeyError:
            raise TypeError("missing parameter 'cell_rect' when drawing the map object '{}'".format(self._name))

        rect = self._surface.get_rect()
        rect.center = cell_rect.center
        destination_surface.blit(self._surface, rect)

    def _update_info(self):
        """
        Update the MapObjectInfo.
        """
        pass


class Movable(MapObject):
    """
    Map object that can move on the map.
    """

    def __init__(self, name: str, res_name: str, resource_manager: ResourceManager) -> None:
        """
        Initialize Movable.

        :param name: in-game name of the object
        :param res_name: name of the resource that should be loaded as the surface
        :param resource_manager: resource manager for the initialization of the surface
        """
        super().__init__(name, res_name, resource_manager)

        self._max_movement_points: int = 0
        self._movement_points: int = 0

        # Set the type to unit and add the attribute movement to the info object and update it
        self._info.type = "Unit"
        self._info.attributes["movement"] = ""
        self._update_info()

    @property
    def movement_points(self) -> int:
        """
        Number of movement points of the object that are still available.
        """
        return self._movement_points

    @movement_points.setter
    def movement_points(self, value) -> None:
        self._movement_points = value
        self._update_info()  # Must be updated each time when the value changes

    @override
    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        # On the beginning of each turn the movement points are reset to the max value
        if event.type == START_TURN:
            self.movement_points = self._max_movement_points
        return False

    @override
    def _update_info(self):
        self._info.attributes["movement"] = "{}/{}".format(self._movement_points, self._max_movement_points)
