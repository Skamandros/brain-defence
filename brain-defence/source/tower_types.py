from abc import abstractmethod

from pyglet import shapes

from rendering import rendering_batches
from constants import BatchNames


class TowerType:
    def __init__(self, attack_rate, attack_range):
        self.attack_rate = attack_rate
        self.attack_range = attack_range

    @abstractmethod
    def draw(self, x, y):
        pass


class BaseTower(TowerType):
    def __init__(self):
        super().__init__(.5, 200)
        self.shape = None

    def draw(self, x, y):
        self.shape = shapes.Rectangle(x, y, 10, 10, batch=rendering_batches[BatchNames.Entity_Batch])
