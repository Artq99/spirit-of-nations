from pygame import MOUSEBUTTONUP
from pygame.event import Event

from son.core.events import SHOW_CELL_INFO
from son.core.ui.controller import UIController
from son.core.utils.decorators import override
from son.gameplay.ui._cell_info_controller import UICellInfoController


class UIGameplayController(UIController):
    """
    UI Controller for the gameplay scene.
    """

    def __init__(self) -> None:
        super().__init__()

        self._box_cell_info_controller = UICellInfoController(self)

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
