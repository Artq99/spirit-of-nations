import pygame
from pygame import Surface
from pygame.event import Event
from pygame.font import Font

from son.core.base import Lifecycle
from son.core.scenes import SceneBase
from son.core.ui._widgets_base import UIWidget
from son.core.ui.constants import *
from son.core.utils.decorators import override


class UIController(Lifecycle):
    """
    Base class for the controller of the UI of a scene.
    """

    def __init__(self, owner: SceneBase) -> None:
        self._owner = owner
        self._widgets = list[UIWidget]()

        self._font = Font(pygame.font.get_default_font(), FONT_SIZE)

    @property
    def owner(self) -> SceneBase:
        """
        The scene that owns this controller.
        """
        return self._owner

    @property
    def widgets(self) -> list[UIWidget]:
        """
        List of widgets owned by this controller.

        Any operations on the list will have no effect, since it is a shallow copy. To modify the list of widgets
        use the corresponding methods.
        """
        return self._widgets.copy()

    @override
    def pre_update(self, *args, **kwargs) -> None:
        for widget in self.widgets:
            widget.pre_update(*args, **kwargs)

    @override
    def update(self, mouse_pos: tuple, *args, **kwargs) -> None:
        for widget in self.widgets:
            widget.update(mouse_pos, *args, **kwargs)

    @override
    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        for widget in self.widgets:
            if widget.handle_event(event, *args, **kwargs):
                return True

        return False

    @override
    def draw(self, surface: Surface, *args, **kwargs) -> None:
        for widget in self.widgets:
            widget.draw(surface, *args, **kwargs)

    def add_widget(self, widget: UIWidget) -> None:
        """
        Add a widget to this controller.

        :param widget: widget to be added
        """
        self._widgets.append(widget)

    def remove_widget(self, widget: UIWidget) -> None:
        """
        Remove a widget from this controller.

        :param widget: widget to be removed
        """
        self._widgets.remove(widget)

    # TODO The method should be refactored into a function outside of this class
    def create_text_surface(self, text: str) -> Surface:
        return self._font.render(text, True, COLOR_TEXT, COLOR_BACKGROUND)
