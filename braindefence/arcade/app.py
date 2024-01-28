import logging

import arcade
from pathlib import Path

from braindefence.arcade.levels import LevelOneMap
from constants import *

from braindefence import RESOURCE_DIR
from braindefence.arcade.entities.icons import ImaginationIcon


class BrainDefence(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(World.Width, World.Height, "BrainDefence")
        self.current_map = None
        self.gui_camera = None
        self.imagination_score = 0
        self.increment_score = 0
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

        # Set up the GUI Camera
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.imagination_score = 0
        imagepath = RESOURCE_DIR.joinpath("icons/icon_imagination_rot0.png")
        self.score_icon = ImaginationIcon(
            imagepath.resolve(),
            0.1,
            center_x=World.Width * 0.25,
            center_y=World.Height * 0.9,
            increment_score=self.increment_score,
        )
        self.current_map.scene.add_sprite("Imagination_score", self.score_icon)
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

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()
        self.current_map.render()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Imagination: {self.imagination_score:0.0f}"
        arcade.draw_text(
            score_text,
            World.Width * 0.3,
            World.Height * 0.9,
            arcade.csscolor.WHITE,
            18,
        )

        self.score_icon.update()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""
        self.current_map.check_on_click(x, y, button, key_modifiers)

    def on_update(self, delta_time: float):
        self.current_map.update(delta_time)
        if (self.current_map._timeSinceSpawn % 1) < 1e-2:
            self.increment_score = 1
        else:
            self.increment_score = 0
        self.imagination_score += self.increment_score
        self.score_icon.update()

        if self.fade_progress < 1:
            self.fade_progress += delta_time / 3
            self.bg_music[self.track_from].volume = 1 - self.fade_progress
            self.bg_music[self.track_to].volume = self.fade_progress
            logging.info("Fade progress {}".format(self.fade_progress))


def main():
    """Main function"""
    window = BrainDefence()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
