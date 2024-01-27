import arcade
from pathlib import Path

from constants import *
from entity import Enemy


class GamePhase(Enum):
    Running = (0,)
    Won = (1,)
    Lost = 2


defaultEnemy = Enemy(
    Path("../resources/default/default.png").resolve(), CHARACTER_SCALING
)


class BrainDefence(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(World.Width, World.Height, "BrainDefence")

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.wall_list = None
        self.player_list = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.spawn_sprite = None
        self.brain_sprite = None
        self._timeSinceSpawn = 0

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.background_batche = arcade.SpriteList()
        self.entity_batch = arcade.SpriteList(use_spatial_hash=True)
        self.projectile_batch = arcade.SpriteList(use_spatial_hash=True)
        self.HUD_batch = arcade.SpriteList()

        # Set up the spawn, specifically placing it at these coordinates.
        image_source = Path("../resources/eye.png")
        self.spawn = arcade.Sprite(image_source.resolve(), 1)
        self.spawn.center_x = World.Width * 0.1
        self.spawn.center_y = World.Height * 0.1
        self.scene.add_sprite("Spawn", self.spawn)

        # Set up the spawn, specifically placing it at these coordinates.
        image_source = Path("../resources/brain.png")
        self.brain = arcade.Sprite(image_source.resolve(), 1)
        self.brain.center_x = World.Width * 0.9
        self.brain.center_y = World.Height * 0.9
        self.scene.add_sprite("Brain", self.brain)

        self.enemies = []
        self.enemies.append(defaultEnemy)
        for i, enemy in enumerate(self.enemies):
            self.scene.add_sprite(f"enemy{i:d}", enemy)

        self._enemies_killed = 0
        self._enemies_leaked = 0
        self._game_phase = GamePhase.Running

        self._label = arcade.Text(
            text="",
            start_x=World.Width // 2,
            start_y=World.Height // 2,
            color=arcade.color.WHITE,
            font_size=36,
            align="left",
            font_name="Roboto",
        )
        self._label.visible = False

    def enemy_killed(self):
        self._enemies_killed += 1
        if self._enemies_killed > 20:
            self._game_phase = GamePhase.Won
            self._label.text = "Victory!"
            self._label.visible = True

    def enemy_leaked(self):
        self._enemies_leaked += 1
        if self._enemies_leaked > 5:
            self._game_phase = GamePhase.Lost
            self._label.text = "Defeat!"
            self._label.visible = True

    def update_enemies(self, dt):
        self._timeSinceSpawn += dt
        if self._timeSinceSpawn > World.SpawnRateSeconds:
            self._timeSinceSpawn = 0
            self.enemies.append(defaultEnemy)
        for i, enemy in enumerate(self.enemies):
            enemy.update(dt)
            if enemy.killed():
                self.enemies.remove(enemy)
                self.enemy_killed()
            elif enemy.passed():
                self.enemies.remove(enemy)
                self.enemy_leaked()

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        # self.wall_list.draw()
        self.scene.draw()
        if self._label.visible:
            self._label.draw()

        self.update_enemies(1 / 60)


def main():
    """Main function"""
    window = BrainDefence()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
