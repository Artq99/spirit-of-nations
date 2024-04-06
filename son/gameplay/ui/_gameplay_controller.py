from pygame.event import Event

from son.core.events import SHOW_CELL_INFO, SHOW_MAP_OBJECT_INFO, HIDE_MAP_OBJECT_INFO, START_TURN
from son.core.ui.controller import UIController
from son.core.utils.decorators import override
from son.gameplay.ui._cell_info_controller import UICellInfoController
from son.gameplay.ui._map_object_info_controller import UIMapObjectInfoController
from son.gameplay.ui._turn_tracker_bar_controller import UITurnTrackerBarController


class UIGameplayController(UIController):
    """
    UI Controller for the gameplay scene.
    """

    def __init__(self) -> None:
        super().__init__()

        self._turn_tracker_bar_controller = UITurnTrackerBarController(self)
        self._box_cell_info_controller = UICellInfoController(self)
        self._map_object_info_controller = UIMapObjectInfoController(self)

    @override
    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        if super().handle_event(event, *args, **kwargs):
            return True

        # New turn has started - we do mark this handle this event as handled
        if event.type == START_TURN:
            # Update the turn tracker
            self._turn_tracker_bar_controller.update_info(event.info)
            return False

        # A map object has been selected - we show the info panel.
        if event.type == SHOW_MAP_OBJECT_INFO:
            self._map_object_info_controller.show_box(event.map_object_info, (10, 40))
            return True

        # No map object selected - we hide the info panel.
        if event.type == HIDE_MAP_OBJECT_INFO:
            self._map_object_info_controller.hide_box()
            return True

        # A map cell has been selected - we show the info box.
        if event.type == SHOW_CELL_INFO:
            self._box_cell_info_controller.show_box(event.cell_info, event.pos)
            return True

        return False
