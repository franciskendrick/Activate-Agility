import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class Tiles:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        spriteset = pygame.image.load(
            f"{path}/assets/tiles.png")

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass


tiles = Tiles()
