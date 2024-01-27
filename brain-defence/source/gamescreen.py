from pyglet import shapes
from constants import World
import logging


class GameScreen:
    def __init__(self, batch):
        self.batch = batch
        self.spawn = shapes.Circle(x=0, y=0, radius=100, color=(255, 0, 0), batch=batch)
        self.brain = shapes.Circle(x=World.Width, y=World.Height, radius=100, color=(0, 225, 0), batch=batch)
        self.timeSinceSpawn = 0
        self.enemies = []
        self.enemies.append(Enemy(batch))

    def update(self, dt):
        self.timeSinceSpawn += dt
        if self.timeSinceSpawn > World.SpawnRateSeconds:
            self.timeSinceSpawn = 0
            self.enemies.append(Enemy(self.batch))
            logging.info("Enemy spawned")
        for enemy in self.enemies:
            enemy.update(dt)
            if enemy.passed():
                self.enemies.remove(enemy)
                logging.info("Enemy has reached the brain!")


class Enemy:
    def __init__(self, batch):
        self.x = 0
        self.y = 0
        self.targetX = World.Width
        self.targetY = World.Height
        self.speed = World.EnemySpeed
        self.shape = shapes.Circle(x=self.x, y=self.y, radius=10, color=(0, 0, 255), batch=batch)

    def update(self, dt):
        delta_x = self.targetX - self.x
        delta_y = self.targetY - self.y
        h_speed = (delta_x * self.speed) / (delta_x + delta_y)
        v_speed = (delta_y * self.speed) / (delta_x + delta_y)
        self.x = self.x + min(h_speed, delta_x)
        self.y = self.y + min(v_speed, delta_y)
        self.shape.x = self.x
        self.shape.y = self.y

    def passed(self):
        return abs(self.x - self.targetX) < 10 and abs(self.y - self.targetY < 10)
