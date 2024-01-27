from entity import *
import logging
import rendering


class GameScreen:
    def __init__(self):
        self.batch = rendering.rendering_batches[BatchNames.Background_Batch]
        self.spawn = shapes.Circle(x=0, y=0, radius=100, color=(255, 0, 0), batch=self.batch)
        self.brain = shapes.Circle(x=World.Width, y=World.Height, radius=100, color=(0, 225, 0), batch=self.batch)
        self.timeSinceSpawn = 0
        self.container = EntityContainer()

    def update(self, dt):
        self.timeSinceSpawn += dt
        if self.timeSinceSpawn > World.SpawnRateSeconds:
            self.timeSinceSpawn = 0
            self.container.enemies.append(Enemy())
            logging.debug("Enemy spawned")
        self.container.update(dt)
