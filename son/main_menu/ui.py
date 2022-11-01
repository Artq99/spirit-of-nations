from son.core.scenes import SceneBase
from son.core.ui.controller import UIController
from son.core.ui.widgets import Button


class MainMenuUIController(UIController):

    def __init__(self, owner: SceneBase):
        super().__init__(owner)

        button = Button(self)
        button.text = "New game"
        button.pos = (50, 50)
        button.register_on_click(callback_button_new_game_on_click, owner)

        self.widgets.append(button)


def callback_button_new_game_on_click(scene: SceneBase):
    scene.has_finished = True
    scene.next_scene_name = "Gameplay"
