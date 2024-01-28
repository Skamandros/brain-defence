import arcade

from braindefence import RESOURCE_DIR
from braindefence.arcade import GamePhase
from braindefence.arcade.entities import Impression
from braindefence.arcade.levels import BaseMap
from braindefence.arcade.HUD.hud import IndicatorBar
from braindefence.arcade.constants import *


class LevelOneMap(BaseMap):
    def __init__(self):
        super().__init__(
            RESOURCE_DIR.joinpath("maps/Level-one.tmx").resolve(), maxBrainHealth=200
        )
        self.impressions_spawned = 0
        self._max_spawned_impressions = 35
        arcade.schedule(self.spawn_minions, 2)
        arcade.schedule(self.spawn_minions, 3.1)

    def spawn_minions(self, dt):
        if self.impressions_spawned >= self._max_spawned_impressions:
            pass
        else:
            self.impressions_spawned += 1
            # in the first level we spawn basic minions with very general durability and attributes
            impression = Impression(
                self.waypoints,
                self.spawn_point,
                RESOURCE_DIR.joinpath("impressions/impression-1.png").resolve(),
                0.75,
            )
            impression.indicator_bar: IndicatorBar = IndicatorBar(
                impression,
                self.bar_list,
                (self.brain.center_x, self.brain.center_y + World.Height * 0.1),
                full_color=arcade.color.RED,
                background_color=arcade.color.WHITE,
            )
            self.impressions.append(impression)

    def update(self, delta_time):
        super().update(delta_time)
        self._timeSinceSpawn += delta_time
        for i, impression in enumerate(self.impressions):
            impression.update(delta_time)
            impression.indicator_bar.fullness = min(
                1,
                (impression.currentHealth - impression.maxNegativeHealth)
                / (
                    abs(impression.maxNegativeHealth)
                    + abs(impression.maxPositiveHealth)
                ),
            )
            # Update the player's indicator bar position
            impression.indicator_bar.position = (
                impression.center_x,
                impression.center_y + World.Height * 0.1,
            )
            if impression.passed():
                self.currentBrainHealth += impression.currentHealth
                self.impressions.remove(impression)
                self.bar_list.remove(impression.indicator_bar._background_box)
                self.bar_list.remove(impression.indicator_bar._full_box)

                if len(self.impressions) <= 0:
                    self.game_phase = GamePhase.LevelEnded

    def check_on_click(self, x, y, button, key_modifiers):
        super().check_on_click(x, y, button, key_modifiers)

    def evaluate_win_condition(self):
        if self.game_phase is GamePhase.LevelEnded:
            print("Level ended with ", self.currentBrainHealth, " Brainhealth")
        elif self.maxBrainHealth <= self.currentBrainHealth:
            self.game_phase = GamePhase.Won
            print("YOU WON!!!")
        elif self.minBrainHealth >= self.currentBrainHealth:
            self.game_phase = GamePhase.Lost
            print("YOU LOSE...")
