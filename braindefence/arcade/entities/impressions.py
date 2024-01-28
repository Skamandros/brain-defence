from braindefence.arcade.entities import Entity
from braindefence.arcade.constants import World


class Impression(Entity):
    def __init__(self, impressionWaypoints, startPoint, imagefilepath, character_scaling):
        # Setup parent class
        super().__init__(imagefilepath, character_scaling)

        self._atDestination = False
        self.impressionWaypoints = impressionWaypoints
        self.health = 10
        self.speed = 300
        self._targetX = impressionWaypoints[0][0]
        self._targetY = impressionWaypoints[0][1]
        self.atWayPoint = 0

        self.center_x = startPoint[0]
        self.center_y = startPoint[1]

    def update(self, dt):
        #print("Current Target: ", self._targetX, self._targetY, "Position: ", self.center_x, self.center_y)
        delta_x = self._targetX - self.center_x
        delta_y = self._targetY - self.center_y
        self.center_x += (delta_x * self.speed * dt) / (abs(delta_x) + abs(delta_y))
        self.center_y += (delta_y * self.speed * dt) / (abs(delta_x) + abs(delta_y))

        if self.collides_with_point([self._targetX, self._targetY]):
            self.atWayPoint += 1
            # print(self.atWayPoint, len(self.impressionWaypoints)-1)
            if self.atWayPoint > len(self.impressionWaypoints)-1:
                self._atDestination = True
            else:
                self._targetX = self.impressionWaypoints[self.atWayPoint][0]
                self._targetY = self.impressionWaypoints[self.atWayPoint][1]


    def killed(self):
        return self.health <= 0

    def passed(self):
        return self._atDestination

