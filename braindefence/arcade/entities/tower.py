import arcade
from braindefence.arcade.entities import Entity


class Tower(Entity):
    def __init__(self, imagefilepath, CHARACTER_SCALING):
        super().__init__(imagefilepath, CHARACTER_SCALING)

        self._fireCooldown = 0
        self._targetEnemy = None
        self._tower_type = None

    def attack(self, dt, impression_sprite_list):
        arcade.get_closest_sprite(self, impression_sprite_list)
