from abc import ABC, abstractmethod
from typing import List, Tuple

from pygame import Surface
from pygame.event import Event
from pygame.rect import Rect

from son.core.base import Lifecycle
from son.core.events import START_TURN
from son.core.resources import ResourceManager
from son.core.utils.decorators import override
from son.gameplay.types import MapObjectInfo


class MapObject(Lifecycle, ABC):
    """
    Abstract base class for all map objects.

    Defines the in-game name for the object, provides basic information that can be displayed and implements
    the rendering.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize MapObject.

        :param name: in-game name of the object
        """

        self._name: str = name
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

        surface = self._get_surface()
        rect = surface.get_rect()
        rect.center = cell_rect.center
        destination_surface.blit(surface, rect)

    @abstractmethod
    def _get_surface(self) -> Surface:
        """
        Get the surface that should be rendered as the representation of the object on the map.

        This is an abstract method. By overriding it the inheriting classes can define logic what surface
        is rendered at the moment.
        """
        pass

    def _update_info(self):
        """
        Update the MapObjectInfo.
        """
        pass


class ModifiersHolder:
    """
    Class that adds the cell modifiers to an inheriting object.
    """

    def __init__(self) -> None:
        """
        Initialize Modifiers Holder
        """
        self._modifiers: List[Tuple[str, int]] = list()

    @property
    def modifiers(self) -> List[Tuple[str, int]]:
        """
        List of the modifiers this map object applies to the map cell where it is placed.
        """
        return self._modifiers.copy()


class Static(MapObject):
    """
    Simple map object that does not move and is not animated.

    It always renders the resource specified on creation.
    """

    def __init__(self, name: str, resource: str, resource_manager: ResourceManager) -> None:
        """
        Initialize Static.

        :param name: in-game name of the object
        :param resource: resource name that should be loaded as the surface
        :param resource_manager: the resource manager
        """
        super().__init__(name)
        self._surface = resource_manager.get_resource(resource)

    def _get_surface(self) -> Surface:
        return self._surface


class StaticModifiersHolder(Static, ModifiersHolder):
    """
    Map object that does not move and is not animated but modifies the cell where it is.
    """

    def __init__(self, name: str, resource: str, resource_manager: ResourceManager) -> None:
        """
        Initialize StaticModifiersHolder.

        :param name: in-game name of the object
        :param resource: resource name that should be loaded as the surface
        :param resource_manager: the resource manager
        """
        Static.__init__(self, name, resource, resource_manager)
        ModifiersHolder.__init__(self)


class Movable(MapObject, ABC):
    """
    Map object that can move on the map.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize Movable.

        :param name: in-game name of the object
        """
        super().__init__(name)

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

    # noinspection PyUnusedLocal
    @override
    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        # On the beginning of each turn the movement points are reset to the max value
        if event.type == START_TURN:
            self.movement_points = self._max_movement_points
        return False

    @override
    def _update_info(self):
        self._info.attributes["movement"] = "{}/{}".format(self._movement_points, self._max_movement_points)
