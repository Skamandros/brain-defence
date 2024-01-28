import logging
import math

import arcade
from arcade import SpriteList

from braindefence.arcade.entities import Entity, Impression
from braindefence.arcade.entities.projectile import BaseProjectile


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

    def attack(self, dt: float, impressions: SpriteList, projectiles: SpriteList):
        if self._targetEnemy is None:
            best_distance = self.tower_range
            for impression in impressions:
                distance = self.calc_distance(impression)
                if best_distance < 0 or distance < best_distance:
                    self._targetEnemy = impression
        elif self._targetEnemy not in impressions or self.calc_distance(
                self._targetEnemy) > self.tower_range:
            self._targetEnemy = None
        self._fireCooldown = max(0, self._fireCooldown - dt)
        if self._fireCooldown == 0 and self._targetEnemy is not None:
            projectiles.append(BaseProjectile(self.center_x, self.center_y, self._targetEnemy))
            self._fireCooldown = self.fire_rate

    def calc_distance(self, impression):
        return math.sqrt(pow(self.center_x - impression.center_x, 2) + pow(self.center_y - impression.center_y, 2))

    def is_point_in_tower(self, x, y):
        return (x > self.x1) and (x < self.x2) and (y > self.y2) and (y < self.y1)
