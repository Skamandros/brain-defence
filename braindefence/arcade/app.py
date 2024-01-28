import logging

import arcade
from pathlib import Path

from braindefence.arcade.levels import LevelOneMap
from constants import *

from braindefence import RESOURCE_DIR


class BrainDefence(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(World.Width, World.Height, "BrainDefence")
        self.current_map = None
        self.bg_music = []
        self.bg_music_playing = 0
        self.track_from = None
        self.track_to = None
        self.fade_progress = 1

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # hard coded for map 1 starter
        # TODO: replace with menu and scene handling
        self.current_map = LevelOneMap()
        self.current_map.render_map()

        # Set up the protagonist
        image_source = RESOURCE_DIR.joinpath("images/protagonist_nobg.png").resolve()
        protagonist = arcade.Sprite(image_source.resolve(), .4)
        protagonist.center_x = World.Width * 0.9
        protagonist.center_y = protagonist.height / 2
        self.current_map.scene.add_sprite("Protagonist", protagonist)

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
        self.current_map.render()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""
        self.current_map.check_on_click(x, y, button, key_modifiers)
        # object_list = self.current_map.tile_map.object_lists
        # # for strange reasons, the y coordinate of the tile corners are negative
        # # currenty key just for testing  == Level1Map
        # print(x, y)
        #
        # for tileobject in object_list["TowerSpots"]:
        #     coords = tileobject.shape
        #     x1, x2, y1, y2 = coords[0][0], coords[1][0], coords[0][1], coords[2][1]
        #     y1 = World.Height + y1
        #     y2 = World.Height + y2
        #     print(x1, x2, y1, y2)
        #     print(coords)
        #     # don't ask why coordinates are switched, I don't know
        #     in_coords = (x > x1) and (x < x2) and (y > y2) and (y < y1)
        #     if in_coords:
        #         print("HERE")
        #         image_source = RESOURCE_DIR.joinpath("brain.png").resolve()
        #         test = arcade.Sprite(image_source.resolve(), 1)
        #         test.center_x = (x1 + x2) / 2
        #         test.center_y = (y1 + y2) / 2
        #         self.current_map.scene.add_sprite("test", test)

        # print(object_list)
        # mats = arcade.get_sprites_at_point((x, y), sprite_lists)

    def on_update(self, delta_time: float):
        self.current_map.update(delta_time)

    def on_update(self, delta_time: float):
        self.current_map.update(delta_time)


def main():
    """Main function"""
    window = BrainDefence()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
