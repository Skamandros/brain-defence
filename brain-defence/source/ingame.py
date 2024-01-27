from entity import *
import logging
import rendering


class GameScreen:
    def __init__(self):
        batch = rendering.rendering_batches[BatchNames.Background_Batch]
        self.spawn = shapes.Circle(x=0, y=0, radius=100, color=(255, 0, 0), batch=batch)
        self.brain = shapes.Circle(x=World.Width, y=World.Height, radius=100, color=(0, 225, 0), batch=batch)
        self.container = EntityContainer()

    def update(self, dt):
        self.container.update(dt)
