from enum import Enum

import pyglet

from entity import *
import logging
import rendering


class GamePhase(Enum):
    Running = 0,
    Won = 1,
    Lost = 2


class GameScreen(EntityEventHandler):
    def __init__(self):
        batch = rendering.rendering_batches[BatchNames.Background_Batch]
        # self._spawn = shapes.Circle(x=0, y=0, radius=100, color=(255, 0, 0), batch=batch)
        # self._brain = shapes.Circle(x=World.Width, y=World.Height, radius=100, color=(0, 225, 0), batch=batch)
        eye_image = pyglet.resource.image("images/eye.png")
        self._spawn = pyglet.sprite.Sprite(x=0, y=0, img=eye_image, batch=batch)
        brain_image = pyglet.resource.image("images/brain.png")
        self._brain = pyglet.sprite.Sprite(x=World.Width - 256, y=World.Height - 256, img=brain_image,
                                           batch=batch)
        self._container = EntityContainer(self)
        self._enemies_killed = 0
        self._enemies_leaked = 0
        self._game_phase = GamePhase.Running
        self._label = pyglet.text.Label(
            "Hello, world",
            font_name="Roboto",
            font_size=36,
            x=500,
            y=400,
            anchor_x="center",
            anchor_y="center",
            batch=batch
        )
        self._label.visible = False

    def enemy_killed(self):
        self._enemies_killed += 1
        if self._enemies_killed > 20:
            self._game_phase = GamePhase.Won
            self._label.text = "Victory!"
            self._label.visible = True

    def enemy_leaked(self):
        self._enemies_leaked += 1
        if self._enemies_leaked > 5:
            self._game_phase = GamePhase.Lost
            self._label.text = "Defeat!"
            self._label.visible = True

    def update(self, dt):
        if self._game_phase == GamePhase.Running:
            self._container.update(dt)
