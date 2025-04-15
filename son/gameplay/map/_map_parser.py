import os.path
from typing import List
from xml.etree import ElementTree

from son.core.resources import ResourceManager
from son.gameplay.map._map_cell import MapCell
from son.gameplay.map.objects.static import Forest
from son.gameplay.map.objects.units import Tribe


def parse_map(name: str, resource_manager: ResourceManager) -> List[List[MapCell]]:
    """
    Parse a map file.

    :param name: name of the map
    :param resource_manager: resource manager
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
                    if map_object.tag == "tribe":
                        tribe = Tribe(resource_manager)
                        cell.add_object(tribe)
                    if map_object.tag == "forest":
                        forest = Forest(resource_manager)
                        cell.add_object(forest)

            row.append(cell)
        array.append(row)

    return array
