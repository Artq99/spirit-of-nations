from typing import Optional

from son.core.ui.controller import UIController, UISubcontroller
from son.core.ui.widgets import Box, Label
from son.core.utils.decorators import override
from son.gameplay._types import MapObjectInfo


class UIUnitInfoController(UISubcontroller):
    """
    Controller for the box showing map object info.
    """

    def __init__(self, owner: UIController) -> None:
        """
        Initialize UIUnitInfoController.

        :param owner: UIController that governs this subcontroller
        """
        super().__init__(owner)
        self._info: Optional[MapObjectInfo] = None

        self._box: Optional[Box] = None
        self._label_movement: Optional[Label] = None

    @override
    def update(self, *args, **kwargs) -> None:
        if self._info is not None:
            self._label_movement.text = self._info.attributes["movement"]

    def show_box(self, map_object_info: MapObjectInfo) -> None:
        """
        Show the box on the screen.

        :param map_object_info: map object info
        """

        self._info = map_object_info

        if self._box in self._owner.widgets:
            self._owner.remove_widget(self._box)

        if self._info is not None:
            self._create_box()
            self._owner.add_widget(self._box)

    def _create_box(self):
        """
        Create the box.
        """
        self._box = Box()
        self._box.pos = (10, 40)

        # Label: unit name
        label_unit_name = Label()
        label_unit_name.text = self._info.name
        label_unit_name.pos = (0, 0)
        self._box.add_widget(label_unit_name)

        next_pos_y = label_unit_name.rect.bottom + 5

        # Label: movement - text
        label_movement_text = Label()
        label_movement_text.text = "Movement:"
        label_movement_text.pos = (0, next_pos_y)
        self._box.add_widget(label_movement_text)

        # Label: movement - value
        self._label_movement = Label()
        self._label_movement.text = self._info.attributes["movement"]
        self._label_movement.pos = (100, next_pos_y)
        self._box.add_widget(self._label_movement)

    def hide_box(self) -> None:
        """
        Hide the box.
        """
        if self._box in self._owner.widgets:
            self._owner.remove_widget(self._box)
