from typing import Optional

from son.core.ui.controller import UIController, UISubcontroller
from son.core.ui.widgets import Box, Label, Button
from son.core.vectors import VectorInt2D
from son.gameplay.types import CellInfo


class UICellInfoController(UISubcontroller):
    """
    Controller for the box showing cell info.
    """

    def __init__(self, owner: UIController):
        """
        Initialize UICellInfoController.

        :param owner: UIController that governs this subcontroller
        """
        super().__init__(owner)
        self._box: Optional[Box] = None
        self._info: Optional[CellInfo] = None

    def _create_box(self, pos: VectorInt2D) -> Box:
        box = Box()
        box.pos = pos

        next_position_y = 0

        # Terrain type
        label_terrain_type = Label()
        label_terrain_type.text = "Terrain: {}".format(self._info.terrain_type)
        label_terrain_type.pos = (0, next_position_y)
        box.add_widget(label_terrain_type)

        # Button: close
        button_close = Button()
        button_close.text = "X"
        button_close.pos = (label_terrain_type.rect.right + 50, 0)
        button_close.register_on_click(UICellInfoController._button_close_on_click, self._owner, box)
        box.add_widget(button_close)

        next_position_y = label_terrain_type.rect.bottom + 5

        # Position
        label_position = Label()
        label_position.text = "Position: {}:{}".format(*self._info.grid_pos)
        label_position.pos = (0, next_position_y)
        box.add_widget(label_position)

        next_position_y = label_position.rect.bottom + 5

        # Movement cost
        label_movement_cost = Label()
        label_movement_cost.text = "Movement cost: {}".format(self._info.movement_cost)
        label_movement_cost.pos = (0, next_position_y)
        box.add_widget(label_movement_cost)

        next_position_y = label_movement_cost.rect.bottom + 5

        # Objects
        if len(self._info.objects) > 0:
            label_objects_title = Label()
            label_objects_title.text = "Objects:"
            label_objects_title.pos = (0, next_position_y)
            box.add_widget(label_objects_title)

            next_position_y = label_objects_title.rect.bottom + 5

            for map_object in self._info.objects:
                label_map_object = Label()
                label_map_object.text = map_object.name
                label_map_object.pos = (50, next_position_y)
                box.add_widget(label_map_object)

                next_position_y = label_map_object.rect.bottom + 5

        return box

    def show_box(self, cell_info: CellInfo, pos: VectorInt2D) -> None:
        """
        Show the box on the screen.

        :param cell_info: cell info to show
        :param pos: position where the box should be shown
        """
        self._info = cell_info

        if self._box in self._owner.widgets:
            self._owner.remove_widget(self._box)

        if self._info is not None:
            self._box = self._create_box(pos)
            self._owner.add_widget(self._box)

    def hide_box(self) -> None:
        """
        Hide the box.
        """
        if self._box in self._owner.widgets:
            self._owner.remove_widget(self._box)

    @staticmethod
    def _button_close_on_click(controller: UIController, box: Box):
        """
        Callback method for the button 'close'.
        :param controller: parent controller
        :param box: box to close (remove from the screen)
        """
        controller.remove_widget(box)
