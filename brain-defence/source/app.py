import pyglet

pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()

window = pyglet.window.Window(2160, 1440, fullscreen=True)
label = pyglet.text.Label(
    "Hello, world",
    font_name="Times New Roman",
    font_size=36,
    x=window.width // 2,
    y=window.height // 2,
    anchor_x="center",
    anchor_y="center",
)


@window.event
def on_draw():
    window.clear()
    label.draw()


if __name__ == "__main__":
    pyglet.app.run()
