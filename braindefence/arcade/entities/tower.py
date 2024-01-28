import arcade
from braindefence.arcade.entities import Entity


class Tower(Entity):

    def __init__(self, x1, y1, x2, y2, fire_rate, damage, tower_range, imagefilepath, image_scaling=1):
        super().__init__(imagefilepath, image_scaling)

        self._fireCooldown = 0
        self._targetEnemy = None
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.fire_rate = fire_rate
        self.damage = damage
        self.tower_range = tower_range

    def attack(self, dt, impression_sprite_list):
        arcade.get_closest_sprite(self, impression_sprite_list)

    def is_point_in_tower(self, x, y):
        return (x > self.x1) and (x < self.x2) and (y > self.y2) and (y < self.y1)
