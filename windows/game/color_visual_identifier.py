import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class SpecialColorVisualIdentifier:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()

    def init_images(self):
        # Images
        self.indicators = []
        for i in range(1, 7):
            # Initialize
            indicator = pygame.image.load(
                f"{path}/assets/speical color visual indicator/indicator_{i}")

            # Append
            self.indicators.append(indicator)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass
