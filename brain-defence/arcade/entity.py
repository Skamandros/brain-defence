import arcade
from constants import *


class Entity(arcade.Sprite):
    def __init__(self, imagefilepath, CHARACTER_SCALING):
        super().__init__(imagefilepath, CHARACTER_SCALING)

        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING
        self.character_face_direction = RIGHT_FACING
        self.center_x = World.Width // 2
        self.center_y = World.Height // 2


class Enemy(Entity):
    def __init__(self, imagefilepath, CHARACTER_SCALING):
        # Setup parent class
        super().__init__(imagefilepath, CHARACTER_SCALING)

        self.health = 10
        self.speed = 100
        self._targetX = World.Goal[0]
        self._targetY = World.Goal[1]
        self.center_x = World.Width * 0.15
        self.center_y = World.Height * 0.15

    def update(self, dt):
        delta_x = self._targetX - self.center_x
        delta_y = self._targetY - self.center_y
        self.center_x += (delta_x * self.speed * dt) / (abs(delta_x) + abs(delta_y))
        self.center_y += (delta_y * self.speed * dt) / (abs(delta_x) + abs(delta_y))

    def killed(self):
        return self.health <= 0

    def passed(self):
        return abs(self.center_x - self._targetX) < 10 and abs(
            self.center_y - self._targetY < 10
        )


class Tower(Entity):
    def __init__(self, imagefilepath, CHARACTER_SCALING):
        super().__init__(imagefilepath, CHARACTER_SCALING)

        self._fireCooldown = 0
        self._targetEnemy = None
        self._tower_type = None

    def attack(self, dt, enemyspritelist):
        arcade.get_closest_sprite(self, enemyspritelist)
