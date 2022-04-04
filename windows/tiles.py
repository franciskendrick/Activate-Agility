from functions import separate_sets_from_yaxis, clip_set_to_list_on_xaxis
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class Tiles:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()

    def init_images(self):
        # Spriteset
        spriteset = pygame.image.load(
            f"{path}/assets/tiles.png")

        # Images
        sets = separate_sets_from_yaxis(spriteset, (255, 0, 0))
        self.images = {
            "on": clip_set_to_list_on_xaxis(sets[0]),
            "off": clip_set_to_list_on_xaxis(sets[1])
        }

        # Types
        self.toggle = "on"
        self.color = 0

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass


tiles = Tiles()
