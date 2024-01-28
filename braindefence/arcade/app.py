import logging

import arcade
from pathlib import Path

from braindefence.arcade import GamePhase
from braindefence.arcade.levels import LevelOneMap, LevelTwoMap, LevelThreeMap, LevelFourMap
from braindefence.arcade.sound import SoundManager, BackgroundMusic
from constants import *

from braindefence import RESOURCE_DIR
from braindefence.arcade.HUD import RotatingIcon

import pyglet


class StoryEvent(Enum):
    E1_1 = 0
    E1_2 = 1
    E2_1 = 2
    E2_2 = 3
    E3_1 = 4
    E3_2 = 5
    E4_1 = 6
    E4_2 = 7


class BrainDefence(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__()

        self.levels = [LevelOneMap(), LevelTwoMap(), LevelThreeMap(), LevelFourMap()]
        self.current_map = None
        self.gui_camera = None
        self.imagination_score = 0
        self.increment_score = 0
        self.sound_manager = None
        self.story_events = []
        self.level = 0

        # Set up the protagonist
        image_source = RESOURCE_DIR.joinpath("images/protagonist_nobg.png").resolve()
        self.protagonist = arcade.Sprite(image_source.resolve(), 0.4)
        self.protagonist.center_x = World.Width * 0.9
        self.protagonist.center_y = self.protagonist.height / 2
        self.protagonist.visible = False
        try:
            self.sound_manager = SoundManager()
        except:
            pass

    def setup(self, level=0):
        """Set up the game here. Call this function to restart the game."""

        # hard coded for map 1 starter
        # TODO: replace with menu and scene handling
        self.current_map = self.levels[level]
        self.current_map.start_level()

        # Set up the GUI Camera
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        self.imagination_score = 0
        imagepath = RESOURCE_DIR.joinpath("icons/icon_imagination_rot0.png")
        self.score_icon = RotatingIcon(
            imagepath.resolve(),
            scale=0.1,
            center_x=World.Width * 0.25,
            center_y=World.Height * 0.9,
            change_angle=1,
            max_angle=30,
        )
        self.current_map.scene.add_sprite("Imagination_score", self.score_icon)
        self.current_map.scene.add_sprite("Protagonist", self.protagonist)
        if self.sound_manager is not None:
            self.sound_manager.play_intro_sound(1)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()
        self.current_map.render()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Imagination: {self.imagination_score:0.0f}"
        arcade.draw_text(
            score_text,
            World.Width * 0.3,
            World.Height * 0.9,
            arcade.csscolor.WHITE,
            18,
        )

        self.score_icon.update()
        # print(self.score_icon.angle, self.score_icon.change_angle)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""
        self.current_map.check_on_click(x, y, button, key_modifiers)

    def on_update(self, delta_time: float):
        if (self.current_map.game_phase is GamePhase.LevelEnded) or (self.current_map.game_phase is GamePhase.Lost):
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)
            self.level += 1
            if len(self.levels) -1 == self.level:
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)
            else:
                self.window.show_view(game_over_view)
                self.window.show_view(self)
                self.setup(self.level)
        else:
            self.current_map.update(delta_time)
            if (self.current_map._timeSinceSpawn % 1) < 1e-2:
                self.increment_score = 1
            else:
                self.increment_score = 0
            self.imagination_score += self.increment_score
            self.score_icon.update()
            match self.current_map.level:
                case 1:
                    if self.current_map.currentBrainHealth < 375 and StoryEvent.E1_1 not in self.story_events:
                        self.story_events.append(StoryEvent.E1_1)
                        self.sound_manager.play_event_sound(1, 1)
                        self.sound_manager.switch_bg_music(BackgroundMusic.Negative)
                    elif self.current_map.currentBrainHealth < 200 and StoryEvent.E1_2 not in self.story_events:
                        self.story_events.append(StoryEvent.E1_2)
                        self.sound_manager.play_event_sound(1, 2)
                        self.sound_manager.switch_bg_music(BackgroundMusic.Psycho)
                case 2:
                    if self.current_map.currentBrainHealth < 350 and StoryEvent.E2_1 not in self.story_events:
                        self.story_events.append(StoryEvent.E2_1)
                        self.sound_manager.play_event_sound(2, 1)
                        self.sound_manager.switch_bg_music(BackgroundMusic.Shocked)
                    elif self.current_map.currentBrainHealth < 200 and StoryEvent.E2_2 not in self.story_events:
                        self.story_events.append(StoryEvent.E2_2)
                        self.sound_manager.play_event_sound(2, 2)
                        self.sound_manager.switch_bg_music(BackgroundMusic.Negative)
                case 3:
                    if self.current_map.currentBrainHealth < 350 and StoryEvent.E3_1 not in self.story_events:
                        self.story_events.append(StoryEvent.E3_1)
                        self.sound_manager.play_event_sound(3, 1)
                        self.sound_manager.switch_bg_music(BackgroundMusic.Negative)
                    elif self.current_map.currentBrainHealth < 200 and StoryEvent.E3_2 not in self.story_events:
                        self.story_events.append(StoryEvent.E3_2)
                        self.sound_manager.play_event_sound(3, 2)
                        self.sound_manager.switch_bg_music(BackgroundMusic.Default)
                case 4:
                    if self.current_map.currentBrainHealth < 300 and StoryEvent.E4_1 not in self.story_events:
                        self.story_events.append(StoryEvent.E4_1)
                        self.sound_manager.play_event_sound(4, 1)
                        self.sound_manager.switch_bg_music(BackgroundMusic.Negative)
                    elif self.current_map.currentBrainHealth < 100 and StoryEvent.E4_2 not in self.story_events:
                        self.story_events.append(StoryEvent.E4_2)
                        self.sound_manager.play_event_sound(4, 2)
                        self.sound_manager.switch_bg_music(BackgroundMusic.Psycho)

        try:
            self.sound_manager.on_update(delta_time)
            self.protagonist.visible = self.sound_manager.is_sound_playing()

        except:
            pass


class MainMenu(arcade.View):
    """Class that manages the 'menu' view."""

    def on_show_view(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """Draw the menu"""
        self.clear()
        arcade.draw_text(
            "Main Menu - Click to play",
            World.Width // 2,
            World.Height // 2,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        game_view = BrainDefence()
        game_view.setup(level=0)
        self.window.show_view(game_view)


class GameOverView(arcade.View):
    """Class to manage the game overview"""

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Draw the game overview"""
        self.clear()
        arcade.draw_text(
            "Game Over - Click to restart",
            World.Width / 2,
            World.Height / 2,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        game_view = BrainDefence()
        game_view.setup()
        self.window.show_view(game_view)


def main():
    """Main function"""
    window = arcade.Window(World.Width, World.Height, "BrainDefence")
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
