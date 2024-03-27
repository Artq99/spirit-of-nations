from typing import List

from pygame import Surface
from pygame.rect import Rect

from son.core.base import Lifecycle
from son.core.resources import ResourceManager
from son.core.utils.decorators import override
from son.gameplay._types import MapObjectInfo


class MapObject(Lifecycle):
    """
    Base class for all map objects.
    """

    def __init__(self, resource_manager: ResourceManager) -> None:
        # TODO surface hardcoded for now
        self._surface = resource_manager.get_resource("tribe")

    @override
    def draw(self, destination_surface: Surface, *args, **kwargs) -> None:
        # TODO throw an exception with a meaningful info when cell_rect is not present
        cell_rect: Rect = kwargs["cell_rect"]
        rect = self._surface.get_rect()
        rect.center = cell_rect.center
        destination_surface.blit(self._surface, rect)

    def info(self):
        # TODO hardcoded for now
        return MapObjectInfo(
            name="Tribe"
        )


MapObjectsList = List[MapObject]
