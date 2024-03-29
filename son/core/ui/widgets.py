import pygame
from pygame import Surface
from pygame.event import Event
from pygame.locals import *

from son.core.ui._text import create_text
from son.core.ui._widgets_base import UIWidget, UIWidgetsList
from son.core.ui.constants import *
from son.core.utils.decorators import override
from son.core.vectors import VectorInt2D


class Box(UIWidget):
    """
    Box with a background.
    """

    def __init__(self):
        super().__init__()

        self._surface_padding = Surface((0, 0))

        self._widgets: UIWidgetsList = list()
        self._padding = DEFAULT_PADDING

        self._update_surface()

    @property
    def widgets(self) -> UIWidgetsList:
        """
        Widgets in this box.

        Any operations on the list will have no effect, since it is a shallow copy. To modify the list of widgets
        use the corresponding methods.
        """
        return self._widgets.copy()

    @property
    def padding(self) -> int:
        """
        Padding around the box.
        """
        return self._padding

    @padding.setter
    def padding(self, value: int) -> None:
        self._padding = value
        self._update_surface()

    @override
    def _create_surface(self) -> Surface:
        x_sizes = [10]
        y_sizes = [10]

        for widget in self.widgets:
            x_sizes.append(widget.rect.right)
            y_sizes.append(widget.rect.bottom)

        surface = Surface((max(x_sizes), max(y_sizes)))
        surface.fill(COLOR_BACKGROUND)

        return surface

    def _create_surface_padding(self) -> Surface:
        surface_size = self.surface.get_size()
        surface_padding_size_x = surface_size[0] + (self.padding * 2)
        surface_padding_size_y = surface_size[1] + (self.padding * 2)

        surface_padding = Surface((surface_padding_size_x, surface_padding_size_y))
        surface_padding.fill(COLOR_BACKGROUND)

        return surface_padding

    @override
    def _update_surface(self) -> None:
        self._surface = self._create_surface()
        self._surface_padding = self._create_surface_padding()
        self._rect.size = self._surface_padding.get_size()

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
        event_to_process = event
        if event.type == MOUSEMOTION:
            event_to_process = Event(MOUSEMOTION, {"pos": self._calc_mouse_pos_with_delta(event.pos)})

        for widget in self.widgets:
            if widget.handle_event(event_to_process, *args, **kwargs):
                return True

        return False

    def _calc_mouse_pos_with_delta(self, mouse_pos: VectorInt2D):
        delta_x = self.rect.left + self.padding
        delta_y = self.rect.top + self.padding
        return mouse_pos[0] - delta_x, mouse_pos[1] - delta_y

    @override
    def draw(self, destination_surface: Surface, *args, **kwargs) -> None:
        surface_copy = self.surface.copy()
        for widget in self.widgets:
            widget.draw(surface_copy, *args, **kwargs)

        surface_padding_copy = self._surface_padding.copy()
        surface_padding_copy.blit(surface_copy, (self.padding, self.padding))
        destination_surface.blit(surface_padding_copy, self.rect)

    def add_widget(self, widget) -> None:
        """
        Add a widget to this box.

        :param widget: widget to add
        """
        self._widgets.append(widget)
        self._update_surface()


class Label(UIWidget):
    """
    Simple label.
    """

    def __init__(self) -> None:
        super().__init__()

        self._text = "Label text"

        self._surface = self._create_surface()
        self._rect = self._surface.get_rect()

    @property
    def text(self) -> str:
        """
        Text of the label.
        """
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value
        self._update_surface()

    @override
    def _create_surface(self) -> Surface:
        text_surface = create_text(self.text)
        text_surface_size_x, text_surface_size_y = text_surface.get_size()

        surface_size = (text_surface_size_x + 10, text_surface_size_y + 10)

        surface = Surface(surface_size)
        surface.fill(COLOR_BACKGROUND)
        surface.blit(text_surface, (5, 5))

        return surface

    @override
    def draw(self, destination_surface: Surface, *args, **kwargs) -> None:
        destination_surface.blit(self.surface, self.rect)


class Button(Label):
    """
    Button.
    """

    def __init__(self) -> None:
        super().__init__()

        self._is_focused = False

        self._on_click = None
        self._on_click_args = list()
        self._on_click_kwargs = dict()

    @property
    def is_focused(self) -> bool:
        """
        Is the button focused?
        """
        return self._is_focused

    @override
    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        if event.type == MOUSEMOTION:
            self._is_focused = self.rect.collidepoint(event.pos)
            if self._is_focused:
                return True

        elif event.type == MOUSEBUTTONUP and event.button == 1:
            if self.is_focused:
                if self._on_click is not None:
                    self._on_click(*self._on_click_args, **self._on_click_kwargs)
                return True

        return False

    @override
    def draw(self, destination_surface: Surface, *args, **kwargs) -> None:
        super().draw(destination_surface, *args, **kwargs)

        border_color = COLOR_FOCUS if self._is_focused else COLOR_BORDER
        pygame.draw.rect(destination_surface, border_color, self.rect, width=1)

    def register_on_click(self, action: object, *args, **kwargs) -> None:
        """
        Register an action that should be executed when the button is clicked.

        :param action: function to call on click
        :param args: arguments that will be passed to the method on click
        :param kwargs: keyword arguments that will be passed to the method on click
        """
        self._on_click = action
        self._on_click_args = args
        self._on_click_kwargs = kwargs
