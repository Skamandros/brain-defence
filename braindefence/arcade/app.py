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
        self.gui_camera = None
        self.imagination_score = 0

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # hard coded for map 1 starter
        # TODO: replace with menu and scene handling
        self.current_map = LevelOneMap()
        self.current_map.render_map()

        # Set up the GUI Camera
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.imagination_score = 0

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()
        self.current_map.render()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.imagination_score}"
        arcade.draw_text(
            score_text,
            World.Width * 0.25,
            World.Height * 0.9,
            arcade.csscolor.WHITE,
            18,
        )

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""
        self.current_map.check_on_click(x, y, button, key_modifiers)

    def on_update(self, delta_time: float):
        self.current_map.update(delta_time)

        self.imagination_score += delta_time


def main():
    """Main function"""
    window = BrainDefence()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
