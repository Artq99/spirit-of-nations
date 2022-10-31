from pygame import Surface
from pygame.event import Event


class SceneBase:

    def __init__(self) -> None:
        self.has_finished = False
        self.next_scene_name = None

    def pre_update(self, *args, **kwargs) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass

    def handle_event(self, event: Event, *args, **kwargs) -> None:
        pass

    def draw(self, surface: Surface, *args, **kwargs) -> None:
        pass


class SceneNotRegisteredError(Exception):

    def __init__(self, scene_name: str) -> None:
        super().__init__("The scene has not been registered: {}".format(scene_name))


class SceneManager:
    def __init__(self):
        self._registered_scenes = dict()
        self.active_scene = SceneBase()

    def register_scene(self, name: str, scene: object) -> None:
        self._registered_scenes[name] = scene

    def load_scene(self, name: str) -> None:
        if name not in self._registered_scenes.keys():
            raise SceneNotRegisteredError(name)

        scene_cls = self._registered_scenes[name]
        self.active_scene = scene_cls()

    def handle_scene_finish(self) -> None:
        if self.active_scene.has_finished:
            self.load_scene(self.active_scene.next_scene_name)
