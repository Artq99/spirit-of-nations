from typing import List

from pygame import Surface
from pygame.event import Event

from son.core.events import START_TURN
from son.core.resources import ResourceManager
from son.gameplay.map.objects import MapObject, ModifiersHolder


class Forest(MapObject, ModifiersHolder):

    def __init__(self, resource_manager: ResourceManager) -> None:
        MapObject.__init__(self, "Forest")
        ModifiersHolder.__init__(self)

        self._modifiers.append(("movement_cost", 2))

        self._density = 0

        self._surfaces: List[Surface] = [
            resource_manager.get_resource("object.forest_01.stage_1"),
            resource_manager.get_resource("object.forest_01.stage_2"),
            resource_manager.get_resource("object.forest_01.stage_3"),
            resource_manager.get_resource("object.forest_01.stage_4")
        ]

    def _get_surface(self) -> Surface:
        if self._density < 25:
            return self._surfaces[0]
        elif self._density < 50:
            return self._surfaces[1]
        elif self._density < 75:
            return self._surfaces[2]
        else:
            return self._surfaces[3]

    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        if event.type == START_TURN:
            if self._density < 100:
                self._density += 1
