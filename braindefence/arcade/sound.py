import logging
from enum import Enum

import arcade

from braindefence import RESOURCE_DIR
from braindefence.arcade.constants import MUSIC_VOLUME


class BackgroundMusic(Enum):
    Default = 0
    Positive = 1
    Negative = 2
    Shocked = 3
    Psycho = 4


class SoundManager:
    def __init__(self):
        self.bg_music = []
        self.bg_music_playing = 0
        self.switch_from = None
        self.switch_to = None
        self.fade_progress = 1
        self.sound_queue = []

        track1 = arcade.load_sound(
            RESOURCE_DIR.joinpath("sound/brain_1-01.mp3").resolve(), True
        )
        self.bg_music.append(arcade.play_sound(track1, looping=True, volume=1))
        track2 = arcade.load_sound(
            RESOURCE_DIR.joinpath("sound/brain_2-01.mp3").resolve(), True
        )
        self.bg_music.append(arcade.play_sound(track2, looping=True, volume=0))
        track3 = arcade.load_sound(
            RESOURCE_DIR.joinpath("sound/brain_3-01.mp3").resolve(), True
        )
        self.bg_music.append(arcade.play_sound(track3, looping=True, volume=0))
        track4 = arcade.load_sound(
            RESOURCE_DIR.joinpath("sound/brain_4-01.mp3").resolve(), True
        )
        self.bg_music.append(arcade.play_sound(track4, looping=True, volume=0))
        track5 = arcade.load_sound(
            RESOURCE_DIR.joinpath("sound/brain_5-01.mp3").resolve(), True
        )
        self.bg_music.append(arcade.play_sound(track5, looping=True, volume=0))
        for i, track in enumerate(self.bg_music):
            if i == self.bg_music_playing:
                track.volume = MUSIC_VOLUME
            else:
                track.volume = 0

        intro_variants = [1, 4, 2, 2]
        self.intros = []
        for level, variants_in_level in enumerate(intro_variants):
            intro_music = []
            for i in range(0, variants_in_level):
                intro_music.append(
                    arcade.load_sound(
                        RESOURCE_DIR.joinpath(
                            "sound/Level{0:02d}_Intro{1:02d}.mp3".format(
                                level + 1, i + 1
                            )
                        ),
                        True,
                    )
                )
            self.intros.append(intro_music)

        events_per_level = [2, 2, 2, 2]
        self.events = []
        for level, events_in_level in enumerate(events_per_level):
            events = []
            for i in range(0, events_in_level):
                events.append(
                    arcade.load_sound(
                        RESOURCE_DIR.joinpath(
                            "sound/Level{0:02d}_Event{1:02d}.mp3".format(
                                level + 1, i + 1
                            )
                        ),
                        True,
                    )
                )
            self.events.append(events)

        self.epilogs = []
        for i in range(0, 4):
            self.epilogs.append(
                arcade.load_sound(
                    RESOURCE_DIR.joinpath("sound/Epilog{0:02d}.mp3".format(i + 1))
                )
            )

        self.current_sound = None
        logging.info(self.intros[0][0].source.audio_format)

    def is_sound_playing(self):
        return self.current_sound is not None and self.current_sound.playing

    def on_update(self, delta_time):
        if self.fade_progress < 1:
            self.fade_progress += delta_time / 3
            self.bg_music[self.switch_from].volume = max(
                0, MUSIC_VOLUME - self.fade_progress * MUSIC_VOLUME
            )

            self.bg_music[self.switch_to].volume = self.fade_progress * MUSIC_VOLUME
            logging.debug("Fade progress {}".format(self.fade_progress))
        if (
            self.current_sound is None or not self.current_sound.playing
        ) and self.sound_queue:
            self.current_sound = arcade.play_sound(self.sound_queue.pop(0))
            logging.info("Popped sound from queue")

    def play_intro_sound(self, level: int, variant: int = 1):
        self.sound_queue.append(self.intros[level - 1][variant - 1])
        logging.info(
            "Queued intro sound for level {}, variant {}".format(level, variant)
        )

    def play_event_sound(self, level: int, event_number: int):
        self.sound_queue.append(self.events[level - 1][event_number - 1])
        logging.info(
            "Queued event sound for level {}, event {}".format(level, event_number)
        )

    def play_epilog(self, epilog_number: int):
        self.sound_queue.append(self.epilogs[epilog_number - 1])
        logging.info("Queued epilog sound {}".format(epilog_number))

    def switch_bg_music(self, switch_to: BackgroundMusic):
        self.switch_from = self.bg_music_playing
        self.switch_to = switch_to.value
        self.fade_progress = 0
        logging.info("Fade from {} to {}".format(self.switch_from, self.switch_to))
