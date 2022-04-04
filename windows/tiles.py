from functions import separate_sets_from_yaxis, clip_set_to_list_on_xaxis
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class Tiles:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_tiles()

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

    def init_tiles(self):
        self.tiles = [
            [("on", 0) for x in range(36)] for y in range(17)
        ]

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass


tiles = Tiles()
