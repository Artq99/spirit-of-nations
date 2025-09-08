from typing import Optional

import pygame.event
from pygame.event import Event
from pygame.locals import *

from son.core.events import UNPAUSE
from son.core.ui.controller import UISubcontroller, UIController
from son.core.ui.widgets import Box, Label, Button


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

        # Button: return
        button_return = Button()
        button_return.text = "Return"
        button_return.pos = (0, label_title.rect.bottom + 5)
        button_return.register_on_click(UIPauseMenuController._button_return_on_click)
        box.add_widget(button_return)

        # Button: exit to desktop
        button_exit = Button()
        button_exit.text = "Exit to desktop"
        button_exit.pos = (0, button_return.rect.bottom + 5)
        button_exit.register_on_click(UIPauseMenuController._button_exit_on_click)
        box.add_widget(button_exit)

        return box

    def show_pause_menu(self) -> None:
        if self._box in self._owner.widgets:
            self._owner.remove_widget(self._box)

        self._owner.add_widget(self._box)

    def hide_pause_menu(self) -> None:
        if self._box in self._owner.widgets:
            self._owner.remove_widget(self._box)

    @staticmethod
    def _button_return_on_click() -> None:
        pygame.event.post(Event(UNPAUSE))

    @staticmethod
    def _button_exit_on_click() -> None:
        pygame.event.post(Event(QUIT))
