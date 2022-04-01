import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class Background:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.color = (16, 20, 31)
        self.walls = pygame.image.load(
            f"{path}/assets/walls.png")

    # Draw -------------------------------------------------------- #
    def draw_walls(self, display):
        display.blit(self.walls, (26, 54))


background = Background()
