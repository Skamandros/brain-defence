import arcade

from braindefence import RESOURCE_DIR
from braindefence.arcade.constants import World
from braindefence.arcade.entities import Impression
from braindefence.arcade.levels import BaseMap


class Level1Map(BaseMap):

    def __init__(self):
        super(Level1Map, self).__init__(1)
        arcade.schedule(self.spawn_minions, 3)
        arcade.schedule(self.spawn_minions, 5)

    def spawn_minions(self, dt):
        # in the first level we spawn basic minions with very general durability and attributes
        impression = Impression(
            RESOURCE_DIR.joinpath("minion-template.png").resolve(), 0.1
        )
        self.impressions.append(impression)

        # for i, impression in enumerate(self.impressions):
        #     impression.update(dt)
        #     if impression.killed():
        #         self.enemy_killed()
        #         self.impressions.remove(impression)
        #     elif impression.passed():
        #         self.enemy_leaked()
        #         self.impressions.remove(impression)

    def update(self, delta_time):
        super()

    def check_on_click(self, x, y, button, key_modifiers):
        super().check_on_click(x, y, button, key_modifiers)
