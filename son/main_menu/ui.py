from son.core.scenes import SceneBase, finish_scene
from son.core.ui.controller import UIController
from son.core.ui.widgets import Button, Label, Box


class MainMenuUIController(UIController):

    def __init__(self, owner: SceneBase):
        super().__init__(owner)

        box = Box(self)
        box.pos = (50, 50)

        label = Label(self)
        label.text = "Spirit of Nations"
        label.pos = (0, 0)

        button = Button(self)
        button.text = "New game"
        button.pos = (0, 30)
        button.register_on_click(callback_button_new_game_on_click, owner)

        box.add_widget(label)
        box.add_widget(button)

        self.add_widget(box)


def callback_button_new_game_on_click(scene: SceneBase):
    finish_scene(next_scene_name="Gameplay")
