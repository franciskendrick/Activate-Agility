import pygame
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", 
        "resources", "audio"
        )
    )


class CountdownAudio:
    # Initialize -------------------------------------------------- #
    def __init__(self, options_toggleable_btns):
        # Audios
        self.one_audio = pygame.mixer.Sound(
            f"{resources_path}/naturalreaders_1.mp3")
        self.two_audio = pygame.mixer.Sound(
            f"{resources_path}/naturalreaders_2.mp3")
        self.three_audio = pygame.mixer.Sound(
            f"{resources_path}/naturalreaders_3.mp3")
    
        # Audio Switchcase
        self.audioplaying_switchcase = {
            1: self.play_one,
            2: self.play_two,
            3: self.play_three
        }

        # Audio Played Variables
        self.audio_played = {
            1: False,
            2: False,
            3: False
        }
        
        # Is Playing Variable
        self.playing = options_toggleable_btns["sound"][1]

    # Play -------------------------------------------------------- #
    def play_one(self):
        if self.playing:
            self.one_audio.play()

    def play_two(self):
        if self.playing:
            self.two_audio.play()

    def play_three(self):
        if self.playing:
            self.three_audio.play()

    # Update ------------------------------------------------------ #
    def update(self, options_toggleable_btns):
        self.playing = options_toggleable_btns["sound"][1]

    # Reset ------------------------------------------------------- #
    def reset_audioplayed(self):
        self.audio_played = {
            1: False,
            2: False,
            3: False
        }
