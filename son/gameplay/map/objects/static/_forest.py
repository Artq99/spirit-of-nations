from son.core.resources import ResourceManager
from son.gameplay.map.objects import MapObject


class Forest(MapObject):
    def __init__(self, resource_manager: ResourceManager):
        super().__init__("Forest", "forest_obj", resource_manager)
