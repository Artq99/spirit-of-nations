from pygame import Surface
from pygame.event import Event

from son.core.base import Lifecycle
from son.core.ui._widgets_base import UIWidget
from son.core.utils.decorators import override


class UIController(Lifecycle):
    """
    Base class for the controller of the UI of a scene.
    """

    def __init__(self) -> None:
        self._widgets = list[UIWidget]()

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
    def update(self, *args, **kwargs) -> None:
        for widget in self.widgets:
            widget.update(*args, **kwargs)

    @override
    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        for widget in self.widgets:
            if widget.handle_event(event, *args, **kwargs):
                return True

        return False

    @override
    def draw(self, destination_surface: Surface, *args, **kwargs) -> None:
        for widget in self.widgets:
            widget.draw(destination_surface, *args, **kwargs)

    def add_widget(self, widget: UIWidget) -> None:
        """
        Add a widget to this controller.

        :param widget: widget to be added
        """
        if widget not in self.widgets:
            self._widgets.append(widget)

    def remove_widget(self, widget: UIWidget) -> None:
        """
        Remove a widget from this controller.

        :param widget: widget to be removed
        """
        if widget in self.widgets:
            self._widgets.remove(widget)
