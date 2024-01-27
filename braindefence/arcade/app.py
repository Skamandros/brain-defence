import arcade
from pathlib import Path

from braindefence.arcade.levels.level1map import Level1Map
from constants import *


class BrainDefence(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(World.Width, World.Height, "BrainDefence")
        self.current_map = None

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # hard coded for map 1 starter
        # TODO: replace with menue and scene handling
        self.current_map = Level1Map()
        self.current_map.render_map()

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()
        self.current_map.render()


    def on_update(self, delta_time: float):
        self.current_map.update(delta_time)


def main():
    """Main function"""
    window = BrainDefence()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
