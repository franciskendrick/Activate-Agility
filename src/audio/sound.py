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


class Sound:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.pause_sound = pygame.mixer.Sound(
            f"{resources_path}/envatoelements_Pause.mp3")

    # Play -------------------------------------------------------- #
    def play_pause(self):
        self.pause_sound.play()

    # Update ------------------------------------------------------ #
    def update(self):
        pass
