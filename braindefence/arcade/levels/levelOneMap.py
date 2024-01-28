import arcade

from braindefence import RESOURCE_DIR
from braindefence.arcade import GamePhase
from braindefence.arcade.entities import Impression
from braindefence.arcade.levels import BaseMap


class LevelOneMap(BaseMap):
    def __init__(self):
        super().__init__(RESOURCE_DIR.joinpath("maps/Level-one.tmx").resolve(), maxBrainHealth=100)
        arcade.schedule(self.spawn_minions, 2)
        arcade.schedule(self.spawn_minions, 3.1)

    def spawn_minions(self, dt):
        # in the first level we spawn basic minions with very general durability and attributes
        impression = Impression(
            self.waypoints,
            self.spawn_point,
            RESOURCE_DIR.joinpath("impressions/impression-1.png").resolve(),
            0.75,
        )
        self.impressions.append(impression)

    def update(self, delta_time):
        super().update(delta_time)
        self._timeSinceSpawn += delta_time
        for i, impression in enumerate(self.impressions):
            impression.update(delta_time)
            if impression.passed():
                self.currentBrainHealth += impression.currentHealth
                self.impressions.remove(impression)

    def check_on_click(self, x, y, button, key_modifiers):
        super().check_on_click(x, y, button, key_modifiers)

    def evaluate_win_condition(self):
        if self.maxBrainHealth < self.currentBrainHealth:
            self.game_phase = GamePhase.Won
            print("YOU WON!!!")
        elif self.minBrainHealth > self.currentBrainHealth:
            self.game_phase = GamePhase.Lost
            print("YOU LOSE...")
