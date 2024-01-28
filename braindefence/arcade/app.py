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

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # hard coded for map 1 starter
        # TODO: replace with menu and scene handling
        self.current_map = LevelOneMap()
        self.current_map.render_map()



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
