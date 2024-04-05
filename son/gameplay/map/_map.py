from typing import List

from pygame import Surface
from pygame.event import Event

from son.core.base import Lifecycle
from son.core.events import EDGE_SCROLL, SELECT_MAP_OBJECT, MOVE_MAP_OBJECT
from son.core.resources import ResourceManager
from son.core.utils.decorators import override
from son.core.vectors import VectorInt2D
from son.gameplay._types import MapInfo
from son.gameplay.map._map_cell import MapCell
from son.gameplay.map._map_objects_base import MapObject

MapCellArray = List[List[MapCell]]


class MapError(Exception):
    """
    Error raised when something wrong happens with the map.
    """


class Map(Lifecycle):

    def __init__(self, resource_manager: ResourceManager, size: VectorInt2D) -> None:
        # Dependencies
        self._resource_manager: ResourceManager = resource_manager

        self._size = size
        self._array = Map._create_array(size, self._resource_manager)
        self._focused_cell: MapCell or None = None
        self._selected_object: MapObject or None = None
        self._selected_object_pos: VectorInt2D or None = None

    @property
    def pixel_size(self) -> VectorInt2D:
        """
        Size of the map in pixels.
        """
        return self.get_cell((self._size[0] - 1, self._size[1] - 1)).rect.bottomright

    @property
    def info(self) -> MapInfo:
        """
        Info about the current state of the map.
        """
        return MapInfo(
            focused_cell_info=self._focused_cell.info if self._focused_cell is not None else None
        )

    @override
    def pre_update(self, *args, **kwargs) -> None:
        self._focused_cell = None

        for row in self._array:
            for cell in row:
                cell.pre_update(*args, **kwargs)

    @override
    def update(self, *args, **kwargs) -> None:
        for row in self._array:
            for cell in row:
                cell.update(*args, *kwargs)

    @override
    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        for row in self._array:
            for cell in row:
                if cell.handle_event(event, *args, **kwargs):
                    return True

        if event.type == SELECT_MAP_OBJECT:
            self._selected_object = event.map_object
            self._selected_object_pos = event.pos
            return True

        # Attempt of moving the selected map object (if not none) to a different cell
        # For now it is a very simple and naive approach - the object simply moves to a new cell, and it doesn't take
        # distance, type of cell or move capabilities of the object into consideration.
        if event.type == MOVE_MAP_OBJECT:
            if self._selected_object is not None:
                # Remove the object from the old cell
                old_cell = self.get_cell(self._selected_object_pos)
                old_cell.remove_object(self._selected_object)
                # Add the object to the new cell
                new_cell = self.get_cell(event.new_pos)
                new_cell.add_object(self._selected_object)
                # Update the position of the selected map object
                self._selected_object_pos = event.new_pos
            return True

        if event.type == EDGE_SCROLL:
            return True

        return False

    @override
    def draw(self, destination_surface: Surface, *args, **kwargs) -> None:
        for row in self._array:
            for cell in row:
                cell.draw(destination_surface, *args, **kwargs)

    def get_cell(self, pos: VectorInt2D) -> MapCell:
        """
        Get the cell under the given position.
        :param pos: cell position
        """
        try:
            return self._array[pos[1]][pos[0]]
        except IndexError:
            raise MapError("Accessing a cell outside of the map: {}:{}".format(*pos))

    def spawn(self, pos: VectorInt2D) -> None:
        """
        Spawn a map object into the cell under the given position.

        TODO For now there is only one kind of game object. This method will take more arguments in the future.

        :param pos: cell position
        """
        obj = MapObject(name="Tribe", surface=self._resource_manager.get_resource("tribe"))
        self.get_cell(pos).add_object(obj)

    @staticmethod
    def _create_array(size: VectorInt2D, resource_manger: ResourceManager) -> MapCellArray:
        size_x, size_y = size
        array: MapCellArray = list()

        for y in range(size_y):
            row: List[MapCell] = list()
            for x in range(size_x):
                cell = MapCell((x, y), resource_manger)
                row.append(cell)
            array.append(row)

        return array
