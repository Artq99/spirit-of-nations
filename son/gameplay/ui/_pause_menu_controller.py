from typing import Optional

from son.core.ui.controller import UISubcontroller, UIController
from son.core.ui.widgets import Box, Label


class UIPauseMenuController(UISubcontroller):
    """
    Controller for the pause menu.
    """

    def __init__(self, owner: UIController):
        """
        Initialize UIPauseMenuController.

        :param owner: UIController that governs this subcontroller
        """
        super().__init__(owner)
        self._box: Optional[Box] = self._create_box()

    def _create_box(self) -> Box:
        box = Box()
        # TODO make it apper in a reasonable position
        box.pos = (100, 100)

        # Label: pause menu title
        label_title = Label()
        label_title.text = "Pause"
        label_title.pos = (0, 0)
        box.add_widget(label_title)

        return box

    def show_pause_menu(self) -> None:
        if self._box in self._owner.widgets:
            self._owner.remove_widget(self._box)

        self._owner.add_widget(self._box)

    def hide_pause_menu(self) -> None:
        if self._box in self._owner.widgets:
            self._owner.remove_widget(self._box)
