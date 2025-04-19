import random
from typing import List

from pygame import Surface
from pygame.event import Event

from son.core.events import START_TURN
from son.core.resources import ResourceManager
from son.gameplay.map.objects import MapObject, ModifiersHolder
from son.gameplay.types import TurnInfo

# Months when forests can grow
GROWTH_MONTHS = ["April", "May", "June", "July"]

# Growth stages of a forest
STAGE_YOUNG = 0
STAGE_LOW = 1
STAGE_GROWN = 2
STAGE_OLD = 3

# Max age when the growth stage should end
STAGE_MAX_AGES = {
    STAGE_YOUNG: 10,
    STAGE_LOW: 100,
    STAGE_GROWN: 600
}

# Basic growth chances per stage
GROWTH_CHANCES = {
    STAGE_YOUNG: 50,
    STAGE_LOW: 5,
    STAGE_GROWN: 2,
    STAGE_OLD: 1
}


class ForestStats:
    """
    Stats of the forest map object.
    """

    def __init__(self) -> None:
        """
        Initialize forest stats.
        """
        self._density: int = 0
        self._age_in_turns: int = 0

        # Cached
        self._cached_age = 0
        self._cached_growth_stage = STAGE_YOUNG

    @property
    def density(self) -> int:
        """
        Density of the forest in percents (0% - 100%).
        """
        return self._density

    @property
    def age(self) -> int:
        """
        Age of the forest in years.
        """
        return self._cached_age

    @property
    def growth_stage(self):
        """
        Get the growth stage of the forest.
        """
        return self._cached_growth_stage

    def update_on_new_turn(self, turn_info: TurnInfo) -> None:
        """
        Update the stats on a new turn.

        :param turn_info: Information about the current turn
        """
        # Update the age of the forest.
        self._age_in_turns += 1
        self._update_cached_age()

        # When the density is 100 it cannot grow any further.
        if self._density == 100:
            return

        month: str = turn_info.month
        if month not in GROWTH_MONTHS:
            return

        stage = self.growth_stage
        base_grow_chance = GROWTH_CHANCES[stage]

        roll = random.randint(1, 100)

        # When the forest is old, age factor doesn't matter.
        if stage == STAGE_OLD and roll == base_grow_chance:
            self._density += 1
        else:
            growth_stage_max_age = STAGE_MAX_AGES[stage]
            chance = (self.age / growth_stage_max_age) * base_grow_chance
            if roll <= chance:
                self._density += 1

        # Normalize density
        if self._density > 100:
            self._density = 100

        self._update_cached_growth_stage()

    def _update_cached_age(self):
        """
        Update the cached age in years.

        Age in years is equal to the age in turns divided by 12 months divided by 4 weeks.
        """
        self._cached_age = self._age_in_turns / 12 / 4

    def _update_cached_growth_stage(self):
        """
        Update the cached growth stage.
        """
        if self._density < 25:
            self._cached_growth_stage = STAGE_YOUNG
        elif self._density < 50:
            self._cached_growth_stage = STAGE_LOW
        elif self._density < 75:
            self._cached_growth_stage = STAGE_GROWN
        else:
            self._cached_growth_stage = STAGE_OLD


class Forest(MapObject, ModifiersHolder):
    """
    Forest game object.
    """

    def __init__(self, resource_manager: ResourceManager) -> None:
        """
        Initialize Forest.

        :param resource_manager: the resource manager
        """
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

        self._update_info()

    def _get_surface(self) -> Surface:
        return self._surfaces[self._stats.growth_stage]

    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        if event.type == START_TURN:
            self._stats.update_on_new_turn(event.info)
            self._update_info()
            print(self._stats.density)
        return False

    def _update_info(self):
        self._info.attributes["density"] = str(self._stats.density)
