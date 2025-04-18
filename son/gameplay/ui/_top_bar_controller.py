import pygame
from pygame.event import Event

from son.core.events import END_TURN, START_TURN
from son.core.ui.controller import UIController, UISubcontroller
from son.core.ui.widgets import Box, Label, Button
from son.core.utils.decorators import override
from son.gameplay.types import TurnInfo


class UITopBarController(UISubcontroller):
    """
    Controller of the bar showing the current turn info and a button that ends the turn.
    """

    def __init__(self, owner: UIController):
        """
        Initialize UITopBarController.

        :param owner: UIController that governs this subcontroller
        """
        super().__init__(owner)
        self._box: Box = Box()

        # Label - week
        self._label_week = Label()
        self._label_week.pos = (0, 0)
        self._box.add_widget(self._label_week)

        # Label - month
        self._label_month = Label()
        self._label_month.pos = (100, 0)
        self._box.add_widget(self._label_month)

        # Label - year
        self._label_year = Label()
        self._label_year.pos = (300, 0)
        self._box.add_widget(self._label_year)

        # Button ending the turn
        self._button_end_turn = Button()
        self._button_end_turn.text = "End Turn"
        self._button_end_turn.pos = (400, 0)
        self._button_end_turn.register_on_click(UITopBarController._button_end_turn_on_click)
        self._box.add_widget(self._button_end_turn)

        self.update_info(TurnInfo(week="1", month="January", year="1"))

        self._owner.add_widget(self._box)

    @override
    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        # When a new turn starts, we have to update the info.
        if event.type == START_TURN:
            self.update_info(event.info)
        return False

    def update_info(self, info: TurnInfo) -> None:
        """
        Update the turn info shown by the tracker.

        :param info: info about the new turn
        """
        self._label_week.text = "Week: {}".format(info.week)
        self._label_month.text = "Month: {}".format(info.month)
        self._label_year.text = "Year: {}".format(info.year)

    @staticmethod
    def _button_end_turn_on_click():
        """
        Callback method for the button 'end turn'.
        """
        pygame.event.post(Event(END_TURN))
