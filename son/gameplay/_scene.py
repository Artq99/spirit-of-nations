from pygame import Surface
from pygame.event import Event

from son.core.resources import ResourceManager, ResourceInfo
from son.core.scenes import SceneBase
from son.core.utils.decorators import override
from son.gameplay._edge_scrolling import EdgeScrollingController
from son.gameplay._ui import UIGameplayController
from son.gameplay.map import Map

# TODO Hardcoded for now
_RESOURCE_LIST = [
    ResourceInfo(name="grass", file="grass.png"),
    ResourceInfo(name="tribe", file="tribe.png")
]


class SceneGameplay(SceneBase):
    def __init__(self) -> None:
        super().__init__()

        self._resource_manager = ResourceManager(_RESOURCE_LIST)
        self._resource_manager.load_resources()

        self._ui_controller = UIGameplayController()
        self._map = Map(self._resource_manager, (100, 100))
        self._edge_scrolling_controller = EdgeScrollingController(self._map.pixel_size)

        # TEST - remove later
        self._map.spawn((5, 5))

    @override
    def pre_update(self, *args, **kwargs) -> None:
        self._ui_controller.pre_update(*args, **kwargs)
        self._edge_scrolling_controller.pre_update(*args, **kwargs)
        self._map.pre_update(*args, **kwargs)

    @override
    def update(self, *args, **kwargs) -> None:
        self._ui_controller.update(focused_cell_info=self._map.info.focused_cell_info)
        self._edge_scrolling_controller.update(*args, **kwargs)
        self._map.update(*args, **kwargs)

    @override
    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        if self._ui_controller.handle_event(event):
            return True

        if self._edge_scrolling_controller.handle_event(event, *args, **kwargs):
            return True

        if self._map.handle_event(event, *args, **kwargs):
            return True

        return False

    def draw(self, destination_surface: Surface, *args, **kwargs) -> None:
        destination_surface.fill((0, 0, 0))
        self._map.draw(destination_surface, *args, **kwargs)
        self._edge_scrolling_controller.draw(destination_surface, *args, **kwargs)
        self._ui_controller.draw(destination_surface, *args, **kwargs)
