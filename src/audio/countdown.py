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
    def __init__(self):
        self.one_audio = pygame.mixer.Sound(
            f"{resources_path}/naturalreaders_1.mp3")
        self.two_audio = pygame.mixer.Sound(
            f"{resources_path}/naturalreaders_2.mp3")
        self.three_audio = pygame.mixer.Sound(
            f"{resources_path}/naturalreaders_3.mp3")
    
    # Play -------------------------------------------------------- #
    def play_one(self):
        self.one_audio.play()

    def play_two(self):
        self.two_audio.play()

    def play_three(self):
        self.three_audio.play()

    # Update ------------------------------------------------------ #
    def update(self):
        pass
