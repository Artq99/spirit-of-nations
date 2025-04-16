from son.core.resources import ResourceManager
from son.gameplay.map.objects import StaticModifiersHolder


class Forest(StaticModifiersHolder):
    def __init__(self, resource_manager: ResourceManager) -> None:
        super().__init__("Forest", "object.forest", resource_manager)
        self._modifiers.append(("movement_cost", 2))
