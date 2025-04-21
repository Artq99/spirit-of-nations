from son.core.resources import ResourceManager
from son.gameplay.map.objects import StaticModifiersHolder


class Boulders(StaticModifiersHolder):
    # TODO args and kwargs can be replaced with xml node argument later. see _forest.py
    # noinspection PyUnusedLocal
    def __init__(self, resource_manager: ResourceManager, *args, **kwargs):
        super().__init__("Boulders", "object.boulders", resource_manager)
        self._modifiers.append(("movement_cost", 1))
