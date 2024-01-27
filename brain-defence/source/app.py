import pyglet
from mainmenu import MainMenu

pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()
window = pyglet.window.Window(540, 500, caption="Widget Example")
pyglet.gl.glClearColor(0.8, 0.8, 0.8, 1.0)

mainbatch = pyglet.graphics.Batch()

# label = pyglet.text.Label(
#     "Hello, world",
#     font_name="Times New Roman",
#     font_size=36,
#     x=window.width // 2,
#     y=window.height // 2,
#     anchor_x="center",
#     anchor_y="center",
# )


@window.event
def on_draw():
    window.clear()
    mainMenu = MainMenu(window)
    mainMenu.draw()
    # label.draw()


if __name__ == "__main__":
    pyglet.app.run()
