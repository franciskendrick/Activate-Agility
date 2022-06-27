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
        pass

    # Update ------------------------------------------------------ #
    def update(self):
        pass
