from typing import List, Tuple

import pygame
from pygame import Rect, MOUSEMOTION, MOUSEBUTTONUP, Surface
from pygame.event import Event

from son.core.base import Lifecycle
from son.core.events import (EDGE_SCROLL, SELECT_MAP_OBJECT, SHOW_MAP_OBJECT_INFO, HIDE_MAP_OBJECT_INFO,
                             SHOW_CELL_INFO, MOVE_MAP_OBJECT, START_TURN)
from son.core.utils.decorators import override
from son.core.vectors import VectorInt2D
from son.gameplay._types import CellInfo
from son.gameplay.map._constants import GRID_CELL_SIZE, GRID_CELL_SIZE_XY, COLOR_FOCUS
from son.gameplay.map.objects import MapObject, Static


class MapCellStats:
    """
    Stats of the map cell.
    """

    def __init__(self) -> None:
        self._movement_cost_base: int = 0
        self._movement_cost: int = 0

        self._set_defaults()

    @property
    def movement_cost(self) -> int:
        """
        Movement cost for units to stand on this cell.
        """
        return self._movement_cost

    def update(self, modifiers: List[Tuple[str, int]]) -> None:
        """
        Update the cell stats with the modifiers values.
        """
        self._set_defaults()
        for modifier in modifiers:
            if modifier[0] == "movement_cost":
                self._movement_cost += modifier[1]

    def _set_defaults(self) -> None:
        self._movement_cost_base = 1
        self._movement_cost = self._movement_cost_base


class MapCell(Lifecycle):
    """
    Single cell of a grid-based map.
    """

    @staticmethod
    def _calc_pixel_pos(grid_pos: VectorInt2D) -> VectorInt2D:
        grid_pos_x, grid_pos_y = grid_pos
        return grid_pos_x * GRID_CELL_SIZE, grid_pos_y * GRID_CELL_SIZE

    def __init__(self, grid_pos: VectorInt2D, terrain_type: str, surface: Surface) -> None:
        self._grid_pos: VectorInt2D = grid_pos

        self._rect: Rect = Rect(MapCell._calc_pixel_pos(grid_pos), GRID_CELL_SIZE_XY)
        self._rect_delta: Rect = self._get_rect_with_delta((0, 0))

        self._is_focused: bool = False

        self._terrain_type: str = terrain_type
        self._surface: Surface = surface

        self._map_objects: List[MapObject] = list()

        self._stats: MapCellStats = MapCellStats()

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
    def stats(self) -> MapCellStats:
        """
        Stats of the cell.
        """
        return self._stats

    @property
    def info(self) -> CellInfo:
        """
        Information about this cell.
        """
        return CellInfo(
            grid_pos=self._grid_pos,
            terrain_type=self._terrain_type,
            movement_cost=str(self._stats.movement_cost),
            objects=[o.info for o in self._map_objects]
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

        elif event.type == START_TURN:
            all_modifiers: List[Tuple[str, int]] = list()
            for map_object in self._map_objects:
                if isinstance(map_object, Static):
                    all_modifiers.extend(map_object.modifiers)
            self._stats.update(all_modifiers)

        if self._is_focused:
            if event.type == MOUSEBUTTONUP:

                # Left mouse click - selecting an object on the map
                if event.button == 1:
                    # If there is an object in the cell:
                    if len(self.info.objects) > 0:
                        # - we notify the map about the new selected object and its position
                        # TODO for now only the selection of the last object is possible (index -1)
                        pygame.event.post(Event(SELECT_MAP_OBJECT, {
                            "map_object": self._map_objects[-1],
                            "pos": self._grid_pos
                        }))
                        # - we notify the UI that the info window should be shown
                        pygame.event.post(Event(SHOW_MAP_OBJECT_INFO, {"map_object_info": self.info.objects[-1]}))
                    # If there are no objects in the cell, i.e. it is empty, we must deselect an object:
                    else:
                        # - we notify the map and tell it that the selected object is None
                        pygame.event.post(Event(SELECT_MAP_OBJECT, {"map_object": None, "pos": None}))
                        # - we notify the UI that the info panel should be hidden
                        pygame.event.post(Event(HIDE_MAP_OBJECT_INFO))

                # Middle mouse click - viewing the cell info
                if event.button == 2:
                    pygame.event.post(Event(SHOW_CELL_INFO, {"cell_info": self.info, "pos": self._rect_delta.center}))
                    return True

                # Right mouse click - moving the selected map object
                if event.button == 3:
                    pygame.event.post(Event(MOVE_MAP_OBJECT, {"target": self._grid_pos}))
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
        layer = kwargs["layer"]

        # Layer 0 = base surface
        if layer == 0:
            destination_surface.blit(self._surface, self._rect_delta)
        # Layer 1 = map objects
        elif layer == 1:
            for map_object in self._map_objects:
                map_object.draw(destination_surface, *args, **kwargs, cell_rect=self._rect_delta)
        # Layer 2 = focus marker
        elif layer == 2:
            if self._is_focused:
                pygame.draw.rect(destination_surface, COLOR_FOCUS, self._rect_delta, width=1)

    def add_object(self, map_object: MapObject) -> None:
        """
        Add a map object to this cell.
        :param map_object: map object to add
        """
        self._map_objects.append(map_object)

    def remove_object(self, map_object: MapObject) -> None:
        """
        Remove a map object from this cell.
        :param map_object: map object to remove
        """
        self._map_objects.remove(map_object)
