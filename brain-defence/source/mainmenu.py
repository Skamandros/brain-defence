import pyglet
from pyglet.window import key
from pyglet import font
from pyglet.gui import PushButton
from pyglet.shapes import Rectangle
from pyglet.text import Label

pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()

depressed = pyglet.resource.image("button_up.png")
pressed = pyglet.resource.image("button_down.png")
hover = pyglet.resource.image("button_hover.png")


class BaseMenu:
    """A menu is a collection of widgets."""

    def __init__(self, window) -> None:
        self.window = window
        self.wh = window.height
        self.ww = window.width
        self.widgets = []
        self.frame = pyglet.gui.Frame(window, order=4)
        self.batch = pyglet.graphics.Batch()

    def draw(self):
        for widget in self.widgets:
            self.frame.add_widget(widget)
        self.batch.draw()

    def add_widget(self, widget: pyglet.gui.WidgetBase):
        self.widgets.append(widget)


class MainMenu(BaseMenu):
    def __init__(self, window):
        super().__init__(window)

        self.label = pyglet.text.Label(
            "Main Menu",
            font_name="Times New Roman",
            font_size=36,
            x=window.width // 2,
            y=window.height * 0.8,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
        )

        pushButton = pyglet.gui.PushButton(
            window.width // 2,
            window.height // 2,
            pressed=pressed,
            depressed=depressed,
            hover=hover,
            batch=self.batch,
        )

        self.push_label = pyglet.text.Label(
            "Push Button: False",
            x=window.width // 2,
            y=window.height // 2,
            batch=self.batch,
            color=(0, 0, 0, 255),
        )

        pushButton.set_handler("on_press", self.push_button_handler)
        pushButton.set_handler("on_release", self.release_button_handler)
        self.add_widget(pushButton)

    def push_button_handler(self):
        self.push_label.text = f"Push Button: True"

    def release_button_handler(self):
        self.push_label.text = f"Push Button: False"
