from functions import separate_sets_from_yaxis, clip_set_to_list_on_xaxis
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class PlayerGauge:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        pass

    def init_images(self):
        spriteset = pygame.image.load(
            f"{path}/assets/player_gauge.png")
        order = ["bar", "icon", "on_gauge", "off_gauge"]

        # Images
        self.images = {}
        separated_sets = separate_sets_from_yaxis(spriteset, (255, 0, 0))
        for name, separated_set in zip(order, separated_sets):
            image = clip_set_to_list_on_xaxis(separated_set)
            self.images[name] = image

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass

    # Update ------------------------------------------------------ #
    def update(self):
        pass
