import arcade
from braindefence.arcade.constants import *


class Entity(arcade.Sprite):
    def __init__(self, imagefilepath, character_scaling):
        super().__init__(imagefilepath, character_scaling)

        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        self.scale = character_scaling
        self.character_face_direction = RIGHT_FACING
        self.center_x = World.Width // 2
        self.center_y = World.Height // 2
