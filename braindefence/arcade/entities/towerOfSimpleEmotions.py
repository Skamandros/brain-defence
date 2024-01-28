from braindefence import RESOURCE_DIR
from braindefence.arcade.entities.tower import Tower


class TowerOfSimpleEmotions(Tower):

    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2, 1, 10, 80, RESOURCE_DIR.joinpath("buildings").joinpath("tower-base.png").resolve())

