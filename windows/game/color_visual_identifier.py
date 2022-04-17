from windows import tiles
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
                f"{path}/assets/speical color visual indicator/indicator_{i}.png")

            # Append
            self.indicators.append(indicator)

        # Position
        self.position = game_data["coloridentifier_position"]

        # Color Index
        self.update_colorindex(tiles.specialtile_color)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass

    # Update ------------------------------------------------------ #
    def update_colorindex(self, special_idx):
        self.specialtile_index = special_idx
        print(self.specialtile_index)


speicalcolor_visual_identifier = SpecialColorVisualIdentifier()
