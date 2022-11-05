from pygame.event import Event
from pygame.locals import *

from son.core.events import SHOW_CELL_INFO
from son.core.scenes import SceneBase
from son.core.ui.controller import UIController
from son.core.ui.widgets import Box, Label, Button
from son.core.utils.decorators import override
from son.gameplay.types import CellInfo


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

    def update(self, **kwargs):
        """
        Update the controller.

        :param kwargs: keyword arguments
        """
        if "focused_cell_info" in kwargs.keys():
            self._info = kwargs["focused_cell_info"]

    def _create_box(self) -> Box:
        box = Box(self._owner)
        box.pos = (5, 5)

        label_terrain_type = Label(self._owner)
        label_terrain_type.text = "Terrain: {}".format(self._info.terrain_type)
        label_terrain_type.pos = (0, 0)

        label_position = Label(self._owner)
        label_position.text = "Position: {}:{}".format(*self._info.grid_pos)
        label_position.pos = (0, label_terrain_type.rect.bottom + 5)

        button_close = Button(self._owner)
        button_close.text = "Close"
        button_close.pos = (0, label_position.rect.bottom + 5)
        button_close.register_on_click(_BoxCellInfoController._callback_close_box, self.owner, box)

        box.add_widget(label_terrain_type)
        box.add_widget(label_position)
        box.add_widget(button_close)

        return box

    def show_box(self) -> None:
        """
        Show the box on the screen.
        """
        if self.box in self.owner.widgets:
            self.owner.remove_widget(self.box)

        if self._info is not None:
            self._box = self._create_box()

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

    def __init__(self, owner: SceneBase) -> None:
        super().__init__(owner)

        self._box_cell_info_controller = _BoxCellInfoController(self)

    @override
    def update(self, mouse_pos: tuple, *args, **kwargs) -> None:
        super().update(mouse_pos, *args, **kwargs)

        self._box_cell_info_controller.update(**kwargs)

    @override
    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        if super().handle_event(event, *args, **kwargs):
            return True

        if event.type == SHOW_CELL_INFO:
            self._box_cell_info_controller.show_box()
            return True

        if event.type == MOUSEBUTTONUP and event.button == 3:
            self._box_cell_info_controller.hide_box()
            return True

        return False
