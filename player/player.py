from functions import clip_set_to_list_on_xaxis
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class Player:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()

    def init_images(self):
        # Spriteset
        spriteset = pygame.image.load(
            f"{path}/assets/player.png")
        self.idx = 0

        # Images
        self.images = clip_set_to_list_on_xaxis(spriteset)

    # Draw -------------------------------------------------------- #
    def draw(self):
        pass

    # Update ------------------------------------------------------ #
    def update(self):
        pass
