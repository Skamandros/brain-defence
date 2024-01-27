from enum import Enum


class World:
    Width = 1080
    Height = 760
    SpawnRateSeconds = 3


class BatchNames(Enum):
    Background_Batch = 0
    Entity_Batch = 1
    Projectile_Batch = 2
    HUD_Batch = 3
