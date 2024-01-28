import arcade

from braindefence import RESOURCE_DIR
from braindefence.arcade.constants import World
from braindefence.arcade.entities import Impression
from braindefence.arcade.levels import BaseMap


class LevelOneMap(BaseMap):
    def __init__(self):
        super().__init__(self)
        arcade.schedule(self.spawn_minions, 1)
        # arcade.schedule(self.spawn_minions, 5)

    def spawn_minions(self, dt):
        # in the first level we spawn basic minions with very general durability and attributes
        impression = Impression(
            self.waypoints,
            self.spawn_point,
            RESOURCE_DIR.joinpath("impressions/impression-1.png").resolve(),
            0.3,
        )
        self.impressions.append(impression)

    def update(self, delta_time):
        super().update(delta_time)
        self._timeSinceSpawn += delta_time
        for i, impression in enumerate(self.impressions):
            impression.update(delta_time)
            if impression.killed():
                # self.enemy_killed()
                self.impressions.remove(impression)
            elif impression.passed():
                # self.enemy_leaked()
                self.impressions.remove(impression)

    def check_on_click(self, x, y, button, key_modifiers):
        super().check_on_click(x, y, button, key_modifiers)
