import pyglet
import logging
import rendering

from ingame import GameScreen
from constants import *
import arcade

pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()
pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')
pyglet.options['search_local_libs'] = True
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
rendering.rendering_batches[BatchNames.Background_Batch] = pyglet.graphics.Batch()
rendering.rendering_batches[BatchNames.Entity_Batch] = pyglet.graphics.Batch()
rendering.rendering_batches[BatchNames.Projectile_Batch] = pyglet.graphics.Batch()
rendering.rendering_batches[BatchNames.HUD_Batch] = pyglet.graphics.Batch()

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
gamescreen = GameScreen()


def update(dt):
    gamescreen.update(dt)


@window.event
def on_draw():
    window.clear()
    # label.draw()
    for key, batch in rendering.rendering_batches.items():
        batch.draw()


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0 / 60)
    pyglet.app.run()
