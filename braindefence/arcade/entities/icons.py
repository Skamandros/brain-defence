from braindefence.arcade.entities import Entity
from braindefence.arcade.constants import World


class ImaginationIcon(Entity):
    def __init__(self, imagefilepath, scale, **kwargs):
        # Setup parent class
        self.increment_score = kwargs.pop("increment_score", 0)
        super().__init__(imagefilepath, scale, **kwargs)
        self.scale = scale
        self.change_angle = 1

    def update(self):
        """
        Update the sprite.
        """
        self.position = [
            self._position[0] + self.change_x,
            self._position[1] + self.change_y,
        ]
        if (abs(self.angle) % 360) > 30:
            self.change_angle *= -1
        self.angle += self.change_angle
