from typing import List

import pygame.display

from son.core.ui.controller import UISubcontroller, UIController
from son.core.ui.widgets import Box, Label


class UINotificationsController(UISubcontroller):
    """
    Controller for the notifications.
    """

    def __init__(self, owner: UIController):
        """
        Initialize UINotificationsController.

        :param owner: UIController that governs this subcontroller
        """
        super().__init__(owner)

        self._notifications: List[Box] = list()

    def add_notification(self, text: str):
        box = Box()

        label = Label()
        label.text = text
        label.pos = (0, 0)
        box.add_widget(label)

        self._notifications.append(box)

        if len(self._notifications) > 5:
            self._notifications.pop(0)

        next_y = 50
        window_middle_point = pygame.display.get_window_size()[0] / 2

        for notification in self._notifications:
            notification.pos = ((window_middle_point - (notification.rect.width / 2)), next_y)
            next_y = notification.rect.bottom + 5

            if notification in self._owner.widgets:
                self._owner.remove_widget(notification)

            self._owner.add_widget(notification)
