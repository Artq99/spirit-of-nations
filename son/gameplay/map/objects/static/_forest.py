from son.core.resources import ResourceManager
from son.gameplay.map.objects._base import Static


class Forest(Static):
    def __init__(self, resource_manager: ResourceManager) -> None:
        super().__init__("Forest", "forest_obj", resource_manager)

        self._modifiers.append(("movement_cost", 2))
