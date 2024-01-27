import arcade

from braindefence.arcade.constants import World, TILE_SCALING

from braindefence import RESOURCE_DIR
from braindefence.arcade.entities.impressions import Impression
from braindefence.arcade.gamephase import GamePhase


class BaseMap:
    def __init__(self, level):
        self._timeSinceSpawn = None
        self._game_phase = None
        self._enemies_leaked = None
        self.active_impressions = []
        self.tower_spots = []
        self.level = level
        impressions_spawn_plan = []
        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.wall_list = None
        self.player_list = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.spawn_sprite = None
        self.brain_sprite = None
        self._timeSinceSpawn = 0

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # Create the Sprite lists
        self.enemies = arcade.SpriteList()
        self.towers = arcade.SpriteList(use_spatial_hash=True)
        self.HUD_batch = arcade.SpriteList()

        # initial map rendering
        self.render_map()

    def enemy_leaked(self):
        self._enemies_leaked += 1
        if self._enemies_leaked > 5:
            self._game_phase = GamePhase.Lost
            self._label.text = "Defeat!"
            self._label.visible = True

    def update_enemies(self, dt):
        self._timeSinceSpawn += dt
        if self._timeSinceSpawn > World.SpawnRateSeconds:
            self._timeSinceSpawn = 0
            enemy = Impression(
                RESOURCE_DIR.joinpath("minion-template.png").resolve(), 0.1
            )
            self.enemies.append(enemy)
        for i, enemy in enumerate(self.enemies):
            enemy.update(dt)
            if enemy.killed():
                self.enemy_killed()
                self.enemies.remove(enemy)
            elif enemy.passed():
                self.enemy_leaked()
                self.enemies.remove(enemy)

    def enemy_killed(self):
        self._enemies_killed += 1
        if self._enemies_killed > 20:
            self._game_phase = GamePhase.Won
            self._label.text = "Victory!"
            self._label.visible = True

    def update(self, dt):
        super()

    def render_map(self):
        # Name of map file to load
        map_name = RESOURCE_DIR.joinpath("maps/Level-one.tmx").resolve()

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }

#
# class BaseMap():
#
#     def __init__(self):
#         self.active_impressions = []
#         #impressions_spawn_plan
