from braindefence import RESOURCE_DIR
from braindefence.arcade.entities.projectile import BaseProjectile
from braindefence.arcade.entities.tower import Tower


class TowerOfSimpleEmotions(Tower):

    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2, 1, 10, 400, RESOURCE_DIR.joinpath("buildings").joinpath("tower-base.png").resolve())


    def get_projectile(self, center_x, center_y, _targetEnemy):
        return BaseProjectile(center_x, center_y, _targetEnemy, self.damage)

