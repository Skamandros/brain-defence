import arcade
from braindefence.arcade.constants import *


class Entity(arcade.Sprite):
    def __init__(self, imagefilepath, character_scaling, **kwargs):
        super().__init__(imagefilepath, character_scaling, **kwargs)

        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        self.scale = character_scaling
        self.character_face_direction = RIGHT_FACING
        self.center_x = kwargs.get("center_x", World.Width // 2)
        self.center_y = kwargs.get("center_y", World.Height // 2)
