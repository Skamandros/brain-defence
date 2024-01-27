import logging
import math

from constants import World
import rendering
from tower_types import *
from projectile_types import *
from enemy_types import *
from constants import BatchNames
from rendering import rendering_batches


class EntityEventHandler:
    @abstractmethod
    def enemy_killed(self):
        pass

    @abstractmethod
    def enemy_leaked(self):
        pass


class EntityContainer:
    def __init__(self, callback: EntityEventHandler):
        self.enemies = []
        self.enemies.append(Enemy(DefaultEnemy()))
        self.towers = []
        self.towers.append(Tower(300, 300, self, BaseTower()))
        self.projectiles = []
        self._timeSinceSpawn = 0
        self._callback = callback

    def update(self, dt):
        self._timeSinceSpawn += dt
        if self._timeSinceSpawn > World.SpawnRateSeconds:
            self._timeSinceSpawn = 0
            self.enemies.append(Enemy(DefaultEnemy()))
            logging.debug("Enemy spawned")
        for enemy in self.enemies:
            if enemy.killed():
                self.enemies.remove(enemy)
                self._callback.enemy_killed()
            elif enemy.passed():
                self.enemies.remove(enemy)
                self._callback.enemy_leaked()
                logging.info("Enemy has reached the brain!")
            else:
                enemy.update(dt)
        for tower in self.towers:
            tower.update(dt)
        for projectile in self.projectiles:
            if projectile.passed():
                projectile.targetEnemy.health -= 1
                self.projectiles.remove(projectile)
                logging.debug("Projectile has reached the enemy!")
            else:
                projectile.update(dt)


class Enemy:
    def __init__(self, enemy_type: EnemyType):
        self.x = 0
        self.y = 0
        self.health = enemy_type.max_health
        self._targetX = World.Width
        self._targetY = World.Height
        self._drawable = enemy_type.drawable(self.x, self.y, batch=rendering.rendering_batches[BatchNames.Entity_Batch])
        self._enemy_type = enemy_type

    def update(self, dt):
        delta_x = self._targetX - self.x
        delta_y = self._targetY - self.y
        self.x += (delta_x * self._enemy_type.speed) / (abs(delta_x) + abs(delta_y))
        self.y += (delta_y * self._enemy_type.speed) / (abs(delta_x) + abs(delta_y))
        self._drawable.x = self.x
        self._drawable.y = self.y

    def killed(self):
        return self.health <= 0

    def passed(self):
        return abs(self.x - self._targetX) < 10 and abs(self.y - self._targetY < 10)


class Tower:
    def __init__(self, x, y, container: EntityContainer, tower_type: TowerType):
        self.drawable = tower_type.drawable(x, y, rendering_batches[BatchNames.Entity_Batch])
        self.x = x
        self.y = y
        self._fireCooldown = 0
        self._targetEnemy = None
        self._container = container
        self._tower_type = tower_type

    def update(self, dt):
        if self._targetEnemy is None:
            best_distance = self._tower_type.attack_range
            for enemy in self._container.enemies:
                distance = self.calc_distance(enemy)
                if best_distance < 0 or distance < best_distance:
                    self._targetEnemy = enemy
        elif self._targetEnemy not in self._container.enemies or self.calc_distance(
                self._targetEnemy) > self._tower_type.attack_range:
            self._targetEnemy = None
        self._fireCooldown = max(0, self._fireCooldown - dt)
        if self._fireCooldown == 0 and self._targetEnemy is not None:
            self._container.projectiles.append(
                Projectile(self.x, self.y, self._targetEnemy, self._tower_type.get_projectile_type()))
            self._fireCooldown = self._tower_type.attack_rate

    def calc_distance(self, enemy):
        return math.sqrt(pow(self.x - enemy.x, 2) + pow(self.y - enemy.y, 2))


class Projectile:
    def __init__(self, x, y, target: Enemy, projectile_type: ProjectileType):
        self.x = x
        self.y = y
        self.targetEnemy = target
        self._drawable = projectile_type.drawable(x, y,
                                                  batch=rendering.rendering_batches[BatchNames.Projectile_Batch])
        self._projectile_type = projectile_type

    def update(self, dt):
        delta_x = self.targetEnemy.x - self.x
        delta_y = self.targetEnemy.y - self.y
        self.x += (delta_x * self._projectile_type.speed) / (abs(delta_x) + abs(delta_y))
        self.y += (delta_y * self._projectile_type.speed) / (abs(delta_x) + abs(delta_y))
        self._drawable.x = self.x
        self._drawable.y = self.y

    def passed(self):
        return abs(self.x - self.targetEnemy.x) < 5 and abs(self.y - self.targetEnemy.y < 5)
