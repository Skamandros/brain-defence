import logging

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
        self.bg_music = []
        self.bg_music_playing = 0
        self.track_from = None
        self.track_to = None
        self.fade_progress = 1

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

        # Set up the protagonist
        image_source = RESOURCE_DIR.joinpath("images/protagonist_nobg.png").resolve()
        protagonist = arcade.Sprite(image_source.resolve(), .4)
        protagonist.center_x = World.Width * 0.9
        protagonist.center_y = protagonist.height / 2
        self.scene.add_sprite("Protagonist", protagonist)

        track1 = arcade.load_sound(RESOURCE_DIR.joinpath("sound/brain_1-01.wav"), True)
        self.bg_music.append(arcade.play_sound(track1, looping=True, volume=1))
        track2 = arcade.load_sound(RESOURCE_DIR.joinpath("sound/brain_2-01.wav"), True)
        self.bg_music.append(arcade.play_sound(track2, looping=True, volume=0))
        track3 = arcade.load_sound(RESOURCE_DIR.joinpath("sound/brain_3-01.wav"), True)
        self.bg_music.append(arcade.play_sound(track3, looping=True, volume=0))
        track4 = arcade.load_sound(RESOURCE_DIR.joinpath("sound/brain_4-01.wav"), True)
        self.bg_music.append(arcade.play_sound(track4, looping=True, volume=0))
        track5 = arcade.load_sound(RESOURCE_DIR.joinpath("sound/brain_5-01.wav"), True)
        self.bg_music.append(arcade.play_sound(track5, looping=True, volume=0))
        for i, track in enumerate(self.bg_music):
            if i == self.bg_music_playing:
                track.volume = 1
            else:
                track.volume = 0
        arcade.schedule(self._switch_music, 10)

        level01intro = arcade.load_sound(RESOURCE_DIR.joinpath("sound/Level01_Intro.mp3"), True)
        arcade.play_sound(level01intro)

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

    def _switch_music(self, delta_time: float):
        self.track_from = self.bg_music_playing
        self.bg_music_playing = (self.bg_music_playing + 1) % len(self.bg_music)
        self.track_to = self.bg_music_playing
        self.fade_progress = 0
        logging.info("Fade from {} to {}".format(self.track_from, self.track_to))

    def on_update(self, delta_time: float):
        self.update_enemies(delta_time)
        if self.fade_progress < 1:
            self.fade_progress += delta_time / 3
            self.bg_music[self.track_from].volume = 1 - self.fade_progress
            self.bg_music[self.track_to].volume = self.fade_progress
            logging.info("Fade progress {}".format(self.fade_progress))

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()
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
