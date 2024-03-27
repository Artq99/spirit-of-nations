from pygame.event import Event
from pygame.locals import *

from son.core.events import SHOW_CELL_INFO
from son.core.ui.controller import UIController
from son.core.ui.widgets import Box, Label, Button
from son.core.utils.decorators import override
from son.core.vectors import VectorInt2D
from son.gameplay._types import CellInfo


class _BoxCellInfoController:
    """
    Controller for the box showing cell info.
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

        label_terrain_type = Label()
        label_terrain_type.text = "Terrain: {}".format(self._info.terrain_type)
        label_terrain_type.pos = (0, 0)

        label_position = Label()
        label_position.text = "Position: {}:{}".format(*self._info.grid_pos)
        label_position.pos = (0, label_terrain_type.rect.bottom + 5)

        button_close = Button()
        button_close.text = "Close"
        button_close.pos = (0, label_position.rect.bottom + 5)
        button_close.register_on_click(_BoxCellInfoController._callback_close_box, self.owner, box)

        box.add_widget(label_terrain_type)
        box.add_widget(label_position)
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


class UIGameplayController(UIController):
    """
    UI Controller for the gameplay scene.
    """

    def __init__(self) -> None:
        super().__init__()

        self._box_cell_info_controller = _BoxCellInfoController(self)

    @override
    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        if super().handle_event(event, *args, **kwargs):
            return True

        if event.type == SHOW_CELL_INFO:
            self._box_cell_info_controller.show_box(event.cell_info, event.pos)
            return True

        if event.type == MOUSEBUTTONUP and event.button == 3:
            self._box_cell_info_controller.hide_box()
            return True

        return False
