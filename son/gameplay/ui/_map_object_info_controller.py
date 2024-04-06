from son.core.ui.controller import UIController
from son.core.ui.widgets import Box, Label
from son.core.vectors import VectorInt2D
from son.gameplay._types import MapObjectInfo


class UIMapObjectInfoController:
    """
    Controller for the box showing map object info.
    """

    def __init__(self, owner: UIController) -> None:
        self._owner = owner
        self._box: Box or None = None
        self._info: MapObjectInfo or None = None

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

    def show_box(self, map_object_info: MapObjectInfo, pos: VectorInt2D) -> None:
        """
        Show the box on the screen.

        :param map_object_info: map object info
        :param pos: position where the box should be drawn
        """

        self._info = map_object_info

        if self.box in self.owner.widgets:
            self.owner.remove_widget(self.box)

        if self._info is not None:
            self._box = Box()
            self.box.pos = pos

            label_map_object_name = Label()
            label_map_object_name.text = self._info.name
            label_map_object_name.pos = (0, 0)
            self.box.add_widget(label_map_object_name)

            self.owner.add_widget(self.box)

    def hide_box(self) -> None:
        """
        Hide the box.
        """
        if self._box in self.owner.widgets:
            self.owner.remove_widget(self._box)