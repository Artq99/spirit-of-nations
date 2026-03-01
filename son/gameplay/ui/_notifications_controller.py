from dataclasses import dataclass
from typing import List

import pygame.display

from son.core.ui.controller import UISubcontroller, UIController
from son.core.ui.widgets import Box, Label
from son.core.vectors import VectorInt2D
from son.gameplay.ui.constants import NOTIFICATION_DISPLAY_TIME


@dataclass
class _Notification:
    box: Box
    time_passed: float


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

        self._notifications: List[_Notification] = list()

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        time_delta = kwargs["time_delta"]

        notification_removed = False
        new_notifications: List[_Notification] = list()

        for notification in self._notifications:
            self._owner.remove_widget(notification.box)

        for notification in self._notifications:
            notification.time_passed += time_delta
            if notification.time_passed < NOTIFICATION_DISPLAY_TIME:
                new_notifications.append(notification)
            else:
                notification_removed = True
        self._notifications = new_notifications

        if notification_removed:
            next_y = 50
            for notification in self._notifications:
                notification.box.pos = (notification.box.pos[0], next_y)
                next_y = notification.box.rect.bottom + 5

        for notification in self._notifications:
            self._owner.add_widget(notification.box)

    def add_notification(self, text: str) -> None:
        notification = self._create_notification(text)
        self._notifications.append(notification)
        self._owner.add_widget(notification.box)

    def _create_notification(self, text: str) -> _Notification:
        label = Label()
        label.text = text
        label.pos = (0, 0)

        box = Box()
        box.add_widget(label)
        box.pos = self._calculate_notification_position(box.rect.width)

        return _Notification(box=box, time_passed=0)

    def _calculate_notification_position(self, width: int) -> VectorInt2D:
        window_middle_point = pygame.display.get_window_size()[0] / 2
        x = int(((window_middle_point - (width / 2))))

        y = 50
        if len(self._notifications) > 0:
            y = self._notifications[-1].box.rect.bottom + 5

        return (x, y)
