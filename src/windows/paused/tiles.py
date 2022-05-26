import pygame
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..", "..", "..", 
        "resources", "windows", "windows"
    )
)


class Tiles:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        pass

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass
