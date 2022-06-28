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


class SpecialColorAudioIdentifier:
    # Initialize -------------------------------------------------- #
    def __init__(self, options_toggleable_btns):
        # Audios
        self.blue_audio = pygame.mixer.Sound(
            f"{resources_path}/naturalreaders_Blue.mp3")
        self.green_audio = pygame.mixer.Sound(
            f"{resources_path}/naturalreaders_Green.mp3")
        self.purple_audio = pygame.mixer.Sound(
            f"{resources_path}/naturalreaders_Purple.mp3")
        self.red_audio = pygame.mixer.Sound(
            f"{resources_path}/naturalreaders_Red.mp3")
        self.white_audio = pygame.mixer.Sound(
            f"{resources_path}/naturalreaders_White.mp3")
        self.yellow_audio = pygame.mixer.Sound(
            f"{resources_path}/naturalreaders_Yellow.mp3")

        # Audio Switchcase
        self.audioplaying_switchcase = {
            0: self.play_red,
            1: self.play_yellow,
            2: self.play_green,
            3: self.play_blue,
            4: self.play_purple,
            5: self.play_white
        }

        # Is Playing Variable
        self.playing = options_toggleable_btns["sound"][1]

    # Play -------------------------------------------------------- #
    def play_blue(self):
        if self.playing:
            self.blue_audio.play()
    
    def play_green(self):
        if self.playing:
            self.green_audio.play()

    def play_purple(self):
        if self.playing:
            self.purple_audio.play()

    def play_red(self):
        if self.playing:
            self.red_audio.play()

    def play_white(self):
        if self.playing:
            self.white_audio.play()
    
    def play_yellow(self):
        if self.playing:
            self.yellow_audio.play()

    # Update ------------------------------------------------------ #
    def update(self, options_toggleable_btns):
        self.playing = options_toggleable_btns["sound"][1]
