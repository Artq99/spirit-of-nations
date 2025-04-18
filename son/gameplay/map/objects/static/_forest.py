import random
from typing import List

from pygame import Surface
from pygame.event import Event

from son.core.events import START_TURN
from son.core.resources import ResourceManager
from son.gameplay.map.objects import MapObject, ModifiersHolder
from son.gameplay.types import TurnInfo


class ForestStats:
    """
    Stats of the forest map object.
    """

    def __init__(self) -> None:
        self._density = 0

    @property
    def density(self) -> int:
        """
        Density of the forest in percents (0% - 100%).
        """
        return self._density

    def grow(self, turn_info: TurnInfo) -> None:
        """
        Make the forest grow.

        It depends on the current month how much the forest is going to grow.

        :param turn_info: Information about the current turn
        """
        if self._density == 100:
            return

        month: str = turn_info.month
        grow_value: int = 0
        if month == "April":
            grow_value = random.randint(0, 1)
        elif month == "May":
            grow_value = random.randint(0, 2)
        elif month == "June":
            grow_value = random.randint(0, 2)
        elif month == "July":
            grow_value = random.randint(0, 1)

        self._density += grow_value
        if self._density > 100:
            self._density = 100


class Forest(MapObject, ModifiersHolder):

    def __init__(self, resource_manager: ResourceManager) -> None:
        MapObject.__init__(self, "Forest")
        ModifiersHolder.__init__(self)

        self._modifiers.append(("movement_cost", 2))

        self._stats = ForestStats()

        self._surfaces: List[Surface] = [
            resource_manager.get_resource("object.forest_01.stage_1"),
            resource_manager.get_resource("object.forest_01.stage_2"),
            resource_manager.get_resource("object.forest_01.stage_3"),
            resource_manager.get_resource("object.forest_01.stage_4")
        ]

    def _get_surface(self) -> Surface:
        if self._stats.density < 25:
            return self._surfaces[0]
        elif self._stats.density < 50:
            return self._surfaces[1]
        elif self._stats.density < 75:
            return self._surfaces[2]
        else:
            return self._surfaces[3]

    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        if event.type == START_TURN:
            self._stats.grow(event.info)
        return False
