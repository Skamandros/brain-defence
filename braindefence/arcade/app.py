import logging

import arcade
from pathlib import Path

from braindefence.arcade import GamePhase
from braindefence.arcade.levels import LevelOneMap
from braindefence.arcade.sound import SoundManager, BackgroundMusic
from constants import *

from braindefence import RESOURCE_DIR
from braindefence.arcade.HUD import RotatingIcon


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

        # Set up the protagonist
        image_source = RESOURCE_DIR.joinpath("images/protagonist_nobg.png").resolve()
        self.protagonist = arcade.Sprite(image_source.resolve(), 0.4)
        self.protagonist.center_x = World.Width * 0.9
        self.protagonist.center_y = self.protagonist.height / 2
        self.protagonist.visible = False
        self.sound_manager = SoundManager()

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # hard coded for map 1 starter
        # TODO: replace with menu and scene handling
        self.current_map = LevelOneMap()

        # Set up the GUI Camera
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.imagination_score = 0
        imagepath = RESOURCE_DIR.joinpath("icons/icon_imagination_rot0.png")
        self.score_icon = RotatingIcon(
            imagepath.resolve(),
            scale=0.1,
            center_x=World.Width * 0.25,
            center_y=World.Height * 0.9,
            change_angle=1,
            max_angle=30,
        )
        self.current_map.scene.add_sprite("Imagination_score", self.score_icon)
        self.current_map.scene.add_sprite("Protagonist", self.protagonist)
        self.sound_manager.play_intro_sound(1)

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
        print(self.score_icon.angle, self.score_icon.change_angle)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""
        self.current_map.check_on_click(x, y, button, key_modifiers)

    def on_update(self, delta_time: float):
        if self.current_map.game_phase is GamePhase.Won:
            pass
            # print("Winner!")
            # TODO: add Winner Screen
        elif self.current_map.game_phase is GamePhase.Lost:
            pass
            # TODO: add Loser Screen
        else:
            self.current_map.update(delta_time)
            if (self.current_map._timeSinceSpawn % 1) < 1e-2:
                self.increment_score = 1
            else:
                self.increment_score = 0
            self.imagination_score += self.increment_score
            self.score_icon.update()

        if self.increment_score == 1 and self.imagination_score == 10:
            self.sound_manager.play_event_sound(1, 1)
            self.sound_manager.switch_bg_music(BackgroundMusic.Negative)
        elif self.increment_score == 1 and self.imagination_score == 20:
            self.sound_manager.play_event_sound(1, 2)
            self.sound_manager.switch_bg_music(BackgroundMusic.Psycho)

        self.sound_manager.on_update(delta_time)
        self.protagonist.visible = self.sound_manager.is_sound_playing()


def main():
    """Main function"""
    window = BrainDefence()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
