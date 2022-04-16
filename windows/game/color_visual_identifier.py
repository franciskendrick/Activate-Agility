import pygame
import json
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

# Json
with open(f"{path}/data/game.json") as json_file:
    game_data = json.load(json_file)


class SpecialColorVisualIdentifier:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        # Images
        self.indicators = []
        for i in range(1, 7):
            # Initialize
            indicator = pygame.image.load(
                f"{path}/assets/speical color visual indicator/indicator_{i}")

            # Append
            self.indicators.append(indicator)

        # Position
        self.position = game_data["coloridentifier_position"]

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass
