import os.path
from typing import List, Dict, Type
from xml.etree import ElementTree

from son.core.resources import ResourceManager
from son.gameplay.map._map_cell import MapCell
from son.gameplay.map.objects.static import Forest, Boulders
from son.gameplay.map.objects.units import Tribe

# Tags for map objects and their corresponding types
_OBJECTS: Dict[str, Type] = {
    "tribe": Tribe,
    "forest": Forest,
    "boulders": Boulders
}


class MapParseException(Exception):
    """
    Exception raised when a map file could not be parsed.
    """
    pass


def parse_map(name: str, resource_manager: ResourceManager) -> List[List[MapCell]]:
    """
    Parse a map file.

    :param name: name of the map
    :param resource_manager: resource manager
    :raises MapParseException: when the given file could not be parsed
    """
    path = os.path.join('maps', name + '.map')
    tree = ElementTree.parse(path)
    root = tree.getroot()

    size_x = int(root.attrib["size_x"])
    size_y = int(root.attrib["size_y"])

    array: List[List[MapCell]] = list()

    for y in range(size_y):
        row: List[MapCell] = list()
        for x in range(size_x):
            cell_info = root.find("./cell[@pos_x='{}'][@pos_y='{}']".format(x, y))
            terrain = cell_info.find("./terrain").text
            surface = resource_manager.get_resource("terrain." + terrain)

            cell = MapCell((x, y), terrain, surface)

            map_objects = cell_info.find("./objects")
            if map_objects is not None:
                for map_object in map_objects:
                    try:
                        object_type = _OBJECTS[map_object.tag]
                        instance = object_type(resource_manager)
                        cell.add_object(instance)
                    except KeyError:
                        raise MapParseException("Unknown object: {}".format(map_object.tag))

            row.append(cell)
        array.append(row)

    return array
