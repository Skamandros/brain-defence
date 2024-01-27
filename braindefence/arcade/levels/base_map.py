import arcade

from braindefence.arcade.constants import World, TILE_SCALING

from braindefence import RESOURCE_DIR
from braindefence.arcade.gamephase import GamePhase


class BaseMap:

    def __init__(self, level):
        self.tile_map = None
        self.spawn_point = None
        self.destination = None

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
        self.impressions = arcade.SpriteList()
        self.towers = arcade.SpriteList(use_spatial_hash=True)
        self.HUD_batch = arcade.SpriteList()

        # initial map rendering
        self.render_map()

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

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

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

    def render(self):
        #self.update_enemies(1 / 60)
        # print(len(list(self.enemies)))
        # Draw our sprites
        # self.wall_list.draw()
        self.scene.add_sprite_list(
            name="enemies", use_spatial_hash=False, sprite_list=self.impressions
        )

        self.scene.draw()
        if self._label.visible:
            self._label.draw()

    def spawn_minions(self, dt):
        pass

    def update(self, delta_time):
        self.render()
        pass
