from son.core.resources import ResourceManager
from son.gameplay.map.objects import Static


class Boulders(Static):
    def __init__(self, resource_manager: ResourceManager):
        super().__init__("Boulders", "object.boulders", resource_manager)

        self._modifiers.append(("movement_cost", 1))
