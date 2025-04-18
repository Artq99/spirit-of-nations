from pygame import Surface
from pygame.event import Event

from son.core.base import Lifecycle
from son.core.events import EDGE_SCROLL, SELECT_MAP_OBJECT, MOVE_MAP_OBJECT
from son.core.resources import ResourceManager
from son.core.utils.decorators import override
from son.core.vectors import VectorInt2D
from son.gameplay.map._map_cell import MapCell
from son.gameplay.map._map_parser import parse_map
from son.gameplay.map.objects import MapObject, Movable
from son.gameplay.types import MapInfo


class MapError(Exception):
    """
    Error raised when something wrong happens with the map.
    """


class Map(Lifecycle):

    def __init__(self, resource_manager: ResourceManager, size: VectorInt2D) -> None:
        # Dependencies
        self._resource_manager: ResourceManager = resource_manager

        self._size = size
        self._array = parse_map("test_map_1", self._resource_manager)
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
        if event.type == MOVE_MAP_OBJECT:
            if self._selected_object is not None and isinstance(self._selected_object, Movable):
                if self._selected_object.movement_points == 0:
                    # TODO Warning should be shown to the player
                    return True
                else:
                    # Calculate the new position and get the new cell object
                    new_pos = self._calc_new_position_for_movement(self._selected_object_pos, event.target)
                    new_cell = self.get_cell(new_pos)

                    # Check if the selected object has enough movement points
                    if self._selected_object.movement_points < new_cell.stats.movement_cost:
                        # TODO Warning should be shown to the player
                        return True

                    # Remove the object from the old cell
                    old_cell = self.get_cell(self._selected_object_pos)
                    old_cell.remove_object(self._selected_object)

                    # Update the movement points of the selected object
                    self._selected_object.movement_points -= new_cell.stats.movement_cost

                    # Add the object to the new cell
                    new_cell.add_object(self._selected_object)
                    # Update the position of the selected map object
                    self._selected_object_pos = new_pos
            return True

        if event.type == EDGE_SCROLL:
            return True

        return False

    @override
    def draw(self, destination_surface: Surface, *args, **kwargs) -> None:
        # There are 3 map layers to render:
        #  0: base surface
        #  1: game objects
        #  2: focus marker
        for i in range(3):
            # layer numer is passed down as a kwarg
            kwargs["layer"] = i
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

    def spawn(self, pos: VectorInt2D, map_object: MapObject) -> None:
        """
        Spawn a map object into the cell under the given position.

        :param pos: cell position
        :param map_object: map object to add
        """
        self.get_cell(pos).add_object(map_object)

    @staticmethod
    def _calc_new_position_for_movement(old_pos: VectorInt2D, target: VectorInt2D) -> VectorInt2D:
        """
        Calculate the new position after movement.

        :param old_pos: old position of an object
        :param target: target towards which the object should move
        """
        old_x, old_y = old_pos
        target_x, target_y = target

        # Calculate the direction.
        direction_x = target_x - old_x
        direction_y = target_y - old_y

        # Normalize X.
        if direction_x > 0:
            direction_x = 1
        elif direction_x < 0:
            direction_x = -1

        # Normalize Y.
        if direction_y > 0:
            direction_y = 1
        elif direction_y < 0:
            direction_y = -1

        new_x = old_x + direction_x
        nex_y = old_y + direction_y

        return new_x, nex_y
