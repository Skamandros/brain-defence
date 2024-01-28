import arcade

from braindefence import RESOURCE_DIR
from braindefence.arcade.entities import Impression


class Projectile(arcade.Sprite):
    def __init__(self, x, y, target: Impression, image_filepath, image_scaling=1, speed=100):
        super().__init__(image_filepath, image_scaling)
        self.speed = speed
        self.center_x = x
        self.center_y = y
        self.targetEnemy = target

    def on_update(self, dt: float = 1 / 60):
        delta_x = self.targetEnemy.center_x - self.center_x
        delta_y = self.targetEnemy.center_y - self.center_y
        self.center_x += (delta_x * self.speed * dt) / (abs(delta_x) + abs(delta_y))
        self.center_y += (delta_y * self.speed * dt) / (abs(delta_x) + abs(delta_y))


class BaseProjectile(Projectile):
    def __init__(self, x, y, target):
        super().__init__(x, y, target, RESOURCE_DIR.joinpath("buildings").joinpath("tower-base-projectile.png").resolve())
