from typing import List

import pygame
from pygame import Surface
from pygame.event import Event
from pygame.locals import *

from son.core.base import Lifecycle
from son.core.events import EDGE_SCROLL, SHOW_CELL_INFO
from son.core.resources import ResourceManager
from son.core.utils.decorators import override
from son.core.vectors import VectorInt2D
from son.gameplay._types import CellInfo, MapInfo
from son.gameplay.map._constants import GRID_CELL_SIZE, GRID_CELL_SIZE_XY, COLOR_FOCUS
from son.gameplay.map._map_objects_base import MapObject, MapObjectsList


class MapCell(Lifecycle):
    """
    Single cell of a grid-based map.
    """

    @staticmethod
    def _calc_pixel_pos(grid_pos: VectorInt2D) -> VectorInt2D:
        grid_pos_x, grid_pos_y = grid_pos
        return grid_pos_x * GRID_CELL_SIZE, grid_pos_y * GRID_CELL_SIZE

    def __init__(self, grid_pos: VectorInt2D, resource_manager: ResourceManager) -> None:
        self._grid_pos = grid_pos

        self._rect = Rect(MapCell._calc_pixel_pos(grid_pos), GRID_CELL_SIZE_XY)
        self._rect_delta = self._get_rect_with_delta((0, 0))

        self._is_focused = False

        # TODO terrain type and surface are hardcoded for now
        self._terrain_type = "grass"
        self._surface = resource_manager.get_resource(self._terrain_type)

        self._map_objects: MapObjectsList = list()

    @property
    def rect(self) -> Rect:
        """
        Rect of this cell.
        """
        return self._rect.copy()

    @property
    def is_focused(self) -> bool:
        """
        Is the cell focused?
        """
        return self._is_focused

    @property
    def info(self) -> CellInfo:
        """
        Information about this cell.
        """
        return CellInfo(
            grid_pos=self._grid_pos,
            terrain_type=self._terrain_type,
            objects=[o.info() for o in self._map_objects]
        )

    @override
    def pre_update(self, *args, **kwargs) -> None:
        for map_object in self._map_objects:
            map_object.pre_update(*args, **kwargs)

    @override
    def update(self, *args, **kwargs) -> None:
        for map_object in self._map_objects:
            map_object.update(self, *args, **kwargs)

    @override
    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        for map_object in self._map_objects:
            if map_object.handle_event(event, *args, **kwargs):
                return True

        if event.type == EDGE_SCROLL:
            self._rect_delta = self._get_rect_with_delta(event.delta)
            self._is_focused = self._rect_delta.collidepoint(event.pos)
            return False

        elif event.type == MOUSEMOTION:
            self._is_focused = self._rect_delta.collidepoint(event.pos)
            return False

        if self._is_focused:
            if event.type == MOUSEBUTTONUP and event.button == 1:
                pygame.event.post(Event(SHOW_CELL_INFO, {"cell_info": self.info, "pos": self._rect_delta.center}))
                return True

        return False

    def _get_rect_with_delta(self, delta: VectorInt2D) -> Rect:
        delta_x, delta_y = delta

        rect_delta = self._rect.copy()
        rect_delta.left -= delta_x
        rect_delta.bottom -= delta_y

        return rect_delta

    @override
    def draw(self, destination_surface: Surface, *args, **kwargs) -> None:
        destination_surface.blit(self._surface, self._rect_delta)
        if self._is_focused:
            pygame.draw.rect(destination_surface, COLOR_FOCUS, self._rect_delta, width=1)

        for map_object in self._map_objects:
            map_object.draw(destination_surface, *args, **kwargs, cell_rect=self._rect_delta)

    def add_object(self, map_object: MapObject):
        self._map_objects.append(map_object)


MapCellArray = List[List[MapCell]]


class MapError(Exception):
    """
    Error raised when something wrong happens with the map.
    """


class Map(Lifecycle):

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

    def __init__(self, resource_manager: ResourceManager, size: VectorInt2D) -> None:
        # Dependencies
        self._resource_manager: ResourceManager = resource_manager

        self._size = size
        self._array = Map._create_array(size, self._resource_manager)
        self._focused_cell: MapCell or None = None

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
        result = False
        for row in self._array:
            for cell in row:
                result = cell.handle_event(event, *args, **kwargs)

        if event.type == EDGE_SCROLL:
            result = True

        return result

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
            return self._array[pos[0]][pos[1]]
        except IndexError:
            raise MapError("Accessing a cell outside of the map: {}:{}".format(*pos))

    def spawn(self, pos: VectorInt2D) -> None:
        """
        Spawn a map object into the cell under the given position.

        TODO For now there is only one kind of game object. This method will take more arguments in the future.

        :param pos: cell position
        """
        obj = MapObject(resource_manager=self._resource_manager)
        self.get_cell(pos).add_object(obj)
