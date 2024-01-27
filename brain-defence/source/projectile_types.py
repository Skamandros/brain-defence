from abc import abstractmethod

from pyglet import shapes


class ProjectileType:
    def __init__(self, speed=240):
        self.speed = speed

    @abstractmethod
    def drawable(self, x, y, batch):
        """
        Draws a projectile of this type.
        :param x: The x-coordinate where to draw.
        :param y: The y-coordinate where to draw.
        :param batch: The batch into which the projectile shall be drawn.
        :return: A drawable instance at the given position.
        """
        pass


class DefaultProjectile(ProjectileType):
    def drawable(self, x, y, batch):
        return shapes.Circle(x, y, 2, color=(255, 0, 0), batch=batch)
