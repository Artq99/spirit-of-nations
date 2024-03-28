from pygame import Surface
from pygame.rect import Rect

from son.core.base import Lifecycle
from son.core.utils.decorators import override
from son.core.utils.functions import check_none, check_str_empty
from son.gameplay._types import MapObjectInfo


class MapObject(Lifecycle):
    """
    Base class for all map objects.
    """

    def __init__(self, name: str = "", surface: Surface = None) -> None:
        check_none(surface, "surface")
        check_str_empty(name, "name")

        self._name: str = name
        self._surface: Surface = surface

    @property
    def info(self) -> MapObjectInfo:
        """
        Get information about this map object.
        """
        return MapObjectInfo(
            name=self._name
        )

    @override
    def draw(self, destination_surface: Surface, *args, **kwargs) -> None:
        # The cell_rect must be passed by the map in the keyword arguments.
        # If it's not then someone did a very bad job.
        try:
            cell_rect: Rect = kwargs["cell_rect"]
        except KeyError:
            raise TypeError("Missing parameter 'cell_rect' when drawing the map object '{}'".format(self._name))

        rect = self._surface.get_rect()
        rect.center = cell_rect.center
        destination_surface.blit(self._surface, rect)
