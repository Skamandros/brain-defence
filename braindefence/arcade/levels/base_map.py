import logging
from typing import Tuple

import arcade

from braindefence.arcade.constants import World, TILE_SCALING

from braindefence import RESOURCE_DIR
from braindefence.arcade.entities.towerSpot import TowerSpot
from braindefence.arcade.entities.towerOfSimpleEmotions import TowerOfSimpleEmotions
from braindefence.arcade.gamephase import GamePhase
from braindefence.arcade.entities.tower import Tower
from braindefence.arcade.entities.projectile import Projectile


class BaseMap:

    def __init__(self, level):
        self.waypoints = None
        self.tower_positions = None
        self.tile_map = None
        self.spawn_point = None
        self.destination = None

        self._timeSinceSpawn = None
        self._game_phase = None
        self._impressions_leaked = None
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
        self.impressions = arcade.SpriteList()
        self.projectiles = arcade.SpriteList()
        self.towers = arcade.SpriteList(use_spatial_hash=True)
        self.HUD_batch = arcade.SpriteList()

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

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # extract tower positions
        if self.tower_positions is None:
            self.tower_positions = []
            for tileobject in self.tile_map.object_lists["TowerSpots"]:
                coords = tileobject.shape
                x1, x2, y1, y2 = coords[0][0], coords[1][0], World.Height + coords[0][1], World.Height + coords[2][1]
                self.tower_positions.append(TowerSpot(x1, y1, x2, y2))

        # extract waypoints
        if self.waypoints is None:
            self.waypoints = [len(self.tile_map.object_lists["WayPoints"])]
            for tileobject in self.tile_map.object_lists["WayPoints"]:
                coords = tileobject.shape
                # print("Waypoint:", coords[0], World.Height - coords[1])
                self.waypoints.append([coords[0], World.Height - coords[1]])

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the spawn, specifically placing it at these coordinates.
        image_source = RESOURCE_DIR.joinpath("buildings").joinpath("startpoint-eye.png").resolve()
        self.spawn = arcade.Sprite(image_source.resolve(), 1)
        self.spawn.center_x = World.Width * 0.1
        self.spawn.center_y = World.Height * 0.1
        self.scene.add_sprite("Spawn", self.spawn)

        # Set up the spawn, specifically placing it at these coordinates.
        image_source = RESOURCE_DIR.joinpath("buildings").joinpath("endpoint-brain.png").resolve()
        self.brain = arcade.Sprite(image_source.resolve(), 1)
        self.brain.center_x = World.Width * 0.9
        self.brain.center_y = World.Height * 0.9
        self.scene.add_sprite("Brain", self.brain)

        self._impressions_leaked = 0
        self._game_phase = GamePhase.Running

        self._label = arcade.Text(
            text="",
            start_x=World.Width // 2,
            start_y=World.Height // 2,
            color=arcade.color.WHITE,
            font_size=36,
            align="left",
            font_name="Roboto",
        )
        self._label.visible = False

    def enemy_leaked(self):
        self._impressions_leaked += 1
        if self._impressions_leaked > 5:
            self._game_phase = GamePhase.Lost
            self._label.text = "Defeat!"
            self._label.visible = True

    def evaluate_win_condition(self):
        self._brain_status += 1
        if self._brain_status > 20:
            self._game_phase = GamePhase.Won
            self._label.text = "Victory!"
            self._label.visible = True

    def render(self):
        # self.update_enemies(1 / 60)
        # print(len(list(self.enemies)))
        # Draw our sprites
        # self.wall_list.draw()
        self.scene.draw()
        self.towers.draw()
        self.impressions.draw()
        self.projectiles.draw()

        if self._label.visible:
            self._label.draw()

    def spawn_minions(self, dt):
        pass

    def update(self, delta_time):
        tower: Tower
        for tower in self.towers:
            tower.attack(delta_time, self.impressions, self.projectiles)
        projectile: Projectile
        for projectile in self.projectiles:
            projectile.on_update(delta_time)
            if arcade.check_for_collision(projectile, projectile.targetEnemy):
                projectile.targetEnemy.hit_by(projectile)
                self.projectiles.remove(projectile)

    def check_on_click(self, x, y, button, key_modifiers):
        # check whether a tower spot is clicked
        if self.tower_positions is not None:
            for _, tower_spot in enumerate(self.tower_positions):
                if not tower_spot.is_used and tower_spot.is_point_in_spot(x, y):
                    print("HERE")
                    tower_spot.is_used = True
                    newtower = TowerOfSimpleEmotions(tower_spot.x1, tower_spot.y1, tower_spot.x2, tower_spot.y2)
                    # image_source = RESOURCE_DIR.joinpath("brain.png").resolve()
                    # test = arcade.Sprite(image_source.resolve(), 1)
                    newtower.center_x = (tower_spot.x1 + tower_spot.x2) / 2
                    newtower.center_y = (tower_spot.y1 + tower_spot.y2) / 2
                    self.towers.append(newtower)
