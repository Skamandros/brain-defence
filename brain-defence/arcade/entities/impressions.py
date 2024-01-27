from entity import Entity
from ..constants import World


class Impression(Entity):
    def __init__(self, imagefilepath, CHARACTER_SCALING):
        # Setup parent class
        super().__init__(imagefilepath, CHARACTER_SCALING)

        self.health = 10
        self.speed = 10
        self._targetX = World.Goal[0]
        self._targetY = World.Goal[1]
        self.center_x = World.Width * 0.15
        self.center_y = World.Height * 0.15

    def update(self, dt):
        delta_x = self._targetX - self.center_x
        delta_y = self._targetY - self.center_y
        self.center_x += (delta_x * self.speed * dt) / (abs(delta_x) + abs(delta_y))
        self.center_y += (delta_y * self.speed * dt) / (abs(delta_x) + abs(delta_y))

    def killed(self):
        return self.health <= 0

    def passed(self):
        return abs(self.center_x - self._targetX) < 10 and abs(
            self.center_y - self._targetY < 10
        )