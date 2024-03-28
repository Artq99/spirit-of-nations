from son.core.ui.controller import UIController
from son.core.ui.widgets import Box, Label, Button
from son.core.vectors import VectorInt2D
from son.gameplay._types import CellInfo


class UICellInfoController:
    """
    Controller for the box showing cell info.

    TODO Refactoring
      - Should it inherit from UIController?
    """

    def __init__(self, owner: UIController):
        self._owner = owner
        self._box: Box or None = None
        self._info: CellInfo or None = None

    @property
    def owner(self) -> UIController:
        """
        The owner of this controller.
        """
        return self._owner

    @property
    def box(self) -> Box:
        """
        The box.
        """
        return self._box

    def _create_box(self, pos: VectorInt2D) -> Box:
        box = Box()
        box.pos = pos

        next_position_y = 0

        # Terrain type
        label_terrain_type = Label()
        label_terrain_type.text = "Terrain: {}".format(self._info.terrain_type)
        label_terrain_type.pos = (0, next_position_y)
        box.add_widget(label_terrain_type)

        next_position_y = label_terrain_type.rect.bottom + 5

        # Position
        label_position = Label()
        label_position.text = "Position: {}:{}".format(*self._info.grid_pos)
        label_position.pos = (0, next_position_y)
        box.add_widget(label_position)

        next_position_y = label_position.rect.bottom + 5

        # Objects
        if len(self._info.objects) > 0:
            label_objects_title = Label()
            label_objects_title.text = "Objects:"
            label_objects_title.pos = (0, next_position_y)
            box.add_widget(label_objects_title)

            next_position_y = label_objects_title.rect.bottom + 5

            for map_object in self._info.objects:
                label_map_object = Button()
                label_map_object.text = map_object.name
                label_map_object.pos = (10, next_position_y)
                box.add_widget(label_map_object)

                next_position_y = label_map_object.rect.bottom + 5

        # Button: close
        button_close = Button()
        button_close.text = "Close"
        button_close.pos = (0, next_position_y)
        button_close.register_on_click(UICellInfoController._callback_close_box, self.owner, box)
        box.add_widget(button_close)

        return box

    def show_box(self, cell_info: CellInfo, pos: VectorInt2D) -> None:
        """
        Show the box on the screen.
        """
        self._info = cell_info

        if self.box in self.owner.widgets:
            self.owner.remove_widget(self.box)

        if self._info is not None:
            self._box = self._create_box(pos)
            self.owner.add_widget(self.box)

    def hide_box(self) -> None:
        """
        Hide the box.
        """
        if self._box in self.owner.widgets:
            self.owner.remove_widget(self._box)

    @staticmethod
    def _callback_close_box(controller: UIController, box: Box):
        controller.remove_widget(box)
