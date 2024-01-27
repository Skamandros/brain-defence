import arcade
from pathlib import Path

from constants import *
from braindefence.arcade.entities import Impression
from braindefence import RESOURCE_DIR


class GamePhase(Enum):
    Running = (0,)
    Won = (1,)
    Lost = 2


class BrainDefence(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(World.Width, World.Height, "BrainDefence")

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

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Create the Sprite lists
        self.enemies = arcade.SpriteList()
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

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the spawn, specifically placing it at these coordinates.
        image_source = RESOURCE_DIR.joinpath("eye.png").resolve()
        self.spawn = arcade.Sprite(image_source.resolve(), 1)
        self.spawn.center_x = World.Width * 0.1
        self.spawn.center_y = World.Height * 0.1
        self.scene.add_sprite("Spawn", self.spawn)

        # Set up the spawn, specifically placing it at these coordinates.
        image_source = RESOURCE_DIR.joinpath("brain.png").resolve()
        self.brain = arcade.Sprite(image_source.resolve(), 1)
        self.brain.center_x = World.Width * 0.9
        self.brain.center_y = World.Height * 0.9
        self.scene.add_sprite("Brain", self.brain)

        self._enemies_killed = 0
        self._enemies_leaked = 0
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

    def enemy_killed(self):
        self._enemies_killed += 1
        if self._enemies_killed > 20:
            self._game_phase = GamePhase.Won
            self._label.text = "Victory!"
            self._label.visible = True

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

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()
        self.update_enemies(1 / 60)
        print(len(list(self.enemies)))
        # Draw our sprites
        # self.wall_list.draw()
        self.scene.add_sprite_list(
            name="enemies", use_spatial_hash=False, sprite_list=self.enemies
        )
        self.scene.draw()
        if self._label.visible:
            self._label.draw()


def main():
    """Main function"""
    window = BrainDefence()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
