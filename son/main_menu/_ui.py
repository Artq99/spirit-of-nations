from son.core.scenes import finish_scene
from son.core.ui.controller import UIController
from son.core.ui.widgets import Button, Label, Box


class MainMenuUIController(UIController):
    """
    UI Controller for the scene main menu.
    """

    def __init__(self):
        super().__init__()

        box = Box()
        box.pos = (50, 50)

        label = Label()
        label.text = "Spirit of Nations"
        label.pos = (0, 0)

        button = Button()
        button.text = "New game"
        button.pos = (0, 30)
        button.register_on_click(_on_click_button_new_game)

        box.add_widget(label)
        box.add_widget(button)

        self.add_widget(box)


def _on_click_button_new_game():
    finish_scene(next_scene_name="Gameplay")
