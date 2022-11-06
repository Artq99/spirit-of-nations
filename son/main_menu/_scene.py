from pygame import Surface
from pygame.event import Event

from son.core.scenes import SceneBase
from son.core.utils.decorators import override
from son.main_menu._ui import MainMenuUIController


class SceneMainMenu(SceneBase):
    """
    Scene: Main menu.
    """

    def __init__(self) -> None:
        super().__init__()

        self._ui_controller = MainMenuUIController()

    @override
    def pre_update(self, *args, **kwargs) -> None:
        self._ui_controller.pre_update(*args, **kwargs)

    @override
    def update(self, *args, **kwargs) -> None:
        self._ui_controller.update(*args, **kwargs)

    @override
    def handle_event(self, event: Event, *args, **kwargs) -> None:
        self._ui_controller.handle_event(event, *args, **kwargs)

    @override
    def draw(self, destination_surface: Surface, *args, **kwargs) -> None:
        destination_surface.fill((0, 0, 0))
        self._ui_controller.draw(destination_surface, *args, **kwargs)
