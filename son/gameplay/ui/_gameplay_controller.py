from pygame.event import Event

from son.core.events import SHOW_CELL_INFO, SHOW_MAP_OBJECT_INFO, HIDE_MAP_OBJECT_INFO
from son.core.ui.controller import UIController
from son.core.utils.decorators import override
from son.gameplay.ui._cell_info_controller import UICellInfoController
from son.gameplay.ui._top_bar_controller import UITopBarController
from son.gameplay.ui._unit_info_controller import UIUnitInfoController


class UIGameplayController(UIController):
    """
    UI Controller for the gameplay scene.
    """

    def __init__(self) -> None:
        """
        Initialize UIGameplayController.
        """
        super().__init__()

        # Subcontrollers
        self._top_bar_controller = UITopBarController(self)
        self._cell_info_controller = UICellInfoController(self)
        self._unit_info_controller = UIUnitInfoController(self)

        # Add subcontrollers to the list
        self._subcontrollers.append(self._top_bar_controller)
        self._subcontrollers.append(self._cell_info_controller)
        self._subcontrollers.append(self._unit_info_controller)

    @override
    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        if super().handle_event(event, *args, **kwargs):
            return True

        # A map object has been selected - we show the info panel.
        # TODO For now only one kind of info box can be shown - unit info.
        #  When more map object come, the appropriate info box should be shown according to the type of the object.
        if event.type == SHOW_MAP_OBJECT_INFO:
            map_object_type = event.map_object_info.type
            if map_object_type == "Unit":
                self._unit_info_controller.show_box(event.map_object_info)
            return True

        # No map object selected - we hide the info panel.
        if event.type == HIDE_MAP_OBJECT_INFO:
            self._unit_info_controller.hide_box()
            return True

        # A map cell has been selected - we show the info box.
        if event.type == SHOW_CELL_INFO:
            self._cell_info_controller.show_box(event.cell_info, event.pos)
            return True

        return False
