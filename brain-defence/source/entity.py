import logging
import math

from constants import World
import rendering
from tower_types import *
from projectile_types import *


class EntityContainer:
    def __init__(self):
        self.enemies = []
        self.enemies.append(Enemy())
        self.towers = []
        self.towers.append(Tower(300, 300, self, BaseTower()))
        self.projectiles = []

    def update(self, dt):
        for enemy in self.enemies:
            enemy.update(dt)
            if enemy.passed():
                self.enemies.remove(enemy)
                logging.info("Enemy has reached the brain!")
        for tower in self.towers:
            tower.update(dt)
        for projectile in self.projectiles:
            projectile.update(dt)
            if projectile.passed():
                self.projectiles.remove(projectile)
                logging.debug("Projectile has reached the enemy!")


class Enemy:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.targetX = World.Width
        self.targetY = World.Height
        self.speed = World.EnemySpeed
        self.shape = shapes.Circle(x=self.x, y=self.y, radius=10, color=(0, 0, 255),
                                   batch=rendering.rendering_batches[BatchNames.Entity_Batch])

    def update(self, dt):
        delta_x = self.targetX - self.x
        delta_y = self.targetY - self.y
        self.x += (delta_x * self.speed) / abs(delta_x + delta_y)
        self.y += (delta_y * self.speed) / abs(delta_x + delta_y)
        self.shape.x = self.x
        self.shape.y = self.y

    def passed(self):
        return abs(self.x - self.targetX) < 10 and abs(self.y - self.targetY < 10)


class Tower:
    def __init__(self, x, y, container: EntityContainer, tower_type: TowerType):
        self.drawable = tower_type.drawable(x, y, rendering_batches[BatchNames.Entity_Batch])
        self.x = x
        self.y = y
        self.fireCooldown = 0
        self.targetEnemy = None
        self.container = container
        self.tower_type = tower_type

    def update(self, dt):
        if self.targetEnemy is None:
            best_distance = self.tower_type.attack_range
            for enemy in self.container.enemies:
                distance = self.calc_distance(enemy)
                if best_distance < 0 or distance < best_distance:
                    self.targetEnemy = enemy
        elif self.targetEnemy not in self.container.enemies or self.calc_distance(
                self.targetEnemy) > self.tower_type.attack_range:
            self.targetEnemy = None
        self.fireCooldown = max(0, self.fireCooldown - dt)
        if self.fireCooldown == 0 and self.targetEnemy is not None:
            self.container.projectiles.append(
                Projectile(self.x, self.y, self.targetEnemy, self.tower_type.get_projectile_type()))
            self.fireCooldown = self.tower_type.attack_rate

    def calc_distance(self, enemy):
        return math.sqrt(pow(self.x - enemy.x, 2) + pow(self.y - enemy.y, 2))


class Projectile:
    def __init__(self, x, y, target: Enemy, projectile_type: ProjectileType):
        self.x = x
        self.y = y
        self.drawable = projectile_type.drawable(x, y, batch=rendering.rendering_batches[BatchNames.Projectile_Batch])
        self.targetEnemy = target
        self.speed = World.ProjectileSpeed

    def update(self, dt):
        delta_x = self.targetEnemy.x - self.x
        delta_y = self.targetEnemy.y - self.y
        self.x += (delta_x * self.speed) / abs(delta_x + delta_y)
        self.y += (delta_y * self.speed) / abs(delta_x + delta_y)
        self.drawable.x = self.x
        self.drawable.y = self.y

    def passed(self):
        return abs(self.x - self.targetEnemy.x) < 5 and abs(self.y - self.targetEnemy.y < 5)
