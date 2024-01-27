import sys

import pyglet
import logging

from gamescreen import GameScreen
from constants import World

pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

batch = pyglet.graphics.Batch()

window = pyglet.window.Window(width=World.Width, height=World.Height)
label = pyglet.text.Label(
    "Hello, world",
    font_name="Times New Roman",
    font_size=36,
    x=window.width // 2,
    y=window.height // 2,
    anchor_x="center",
    anchor_y="center",
)
gamescreen = GameScreen(batch)

def update(dt):
    gamescreen.update(dt)

@window.event
def on_draw():
    window.clear()
    # label.draw()
    batch.draw()


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0 / 60)
    pyglet.app.run()
