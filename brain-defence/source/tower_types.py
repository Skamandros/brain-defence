from projectile_types import *


class TowerType:
    def __init__(self, attack_rate, attack_range):
        self.attack_rate = attack_rate
        self.attack_range = attack_range

    @abstractmethod
    def drawable(self, x, y, batch):
        """
        Draws a tower of this type.
        :param x: The x-coordinate where to draw.
        :param y: The y-coordinate where to draw.
        :param batch: The batch into which the tower shall be drawn.
        :return: A drawable instance at the given position.
        """
        pass

    @staticmethod
    def get_projectile_type():
        return DefaultProjectile()


class BaseTower(TowerType):
    def __init__(self):
        super().__init__(.65, 200)

    def drawable(self, x, y, batch):
        return shapes.Rectangle(x, y, 10, 10, batch=batch)
