from enum import Enum

CHARACTER_SCALING = 1
# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1
TILE_SCALING = 1
MUSIC_VOLUME = 0.3


class World:
    Width = 1920
    Height = 1080
    SpawnRateSeconds = 5
    Goal = (0.85 * Width, 0.85 * Height)


class BatchNames(Enum):
    Background_Batch = 0
    Entity_Batch = 1
    Projectile_Batch = 2
    HUD_Batch = 3
