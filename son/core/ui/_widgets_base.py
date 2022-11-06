from pygame import Surface, Rect

from son.core.base import Lifecycle


class UIWidget(Lifecycle):
    """
    Abstract base class for all UI widgets.

    In the inheriting classes remember to call _update_surface() in the __init__ method after the super() call.
    """

    def __init__(self) -> None:
        self._surface = Surface((0, 0))
        self._rect = self._surface.get_rect()

    def _create_surface(self) -> Surface:
        raise NotImplementedError("UIWidget is an abstract base class.")

    def _update_surface(self) -> None:
        self._surface = self._create_surface()
        self._rect.size = self._surface.get_size()

    @property
    def surface(self) -> Surface:
        """
        The surface of the widget.
        """
        return self._surface

    @property
    def rect(self) -> Rect:
        """
        Rect of the widget.
        """
        return self._rect.copy()

    @property
    def pos(self):
        """
        Position of the widget.
        """
        return self.rect.topleft

    @pos.setter
    def pos(self, value):
        self._rect.topleft = value
