import pygame
import json
import time
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", 
        "resources", "windows", "game"
        )
    )

# Json
with open(f"{resources_path}/game.json") as json_file:
    game_data = json.load(json_file)


class SpecialColorVisualIdentifier:
    # Initialize -------------------------------------------------- #
    def __init__(self, speicaltile_color):
        # Game
        self.start_of_game = None

        # Images
        self.indicators = []
        for i in range(1, 7):
            # Initialize
            indicator = pygame.image.load(
                f"{resources_path}/speical color visual indicator/indicator_{i}.png")

            # Append
            self.indicators.append(indicator)

        # Position
        self.position = game_data["coloridentifier_position"]

        # Color Index
        self.update_colorindex(speicaltile_color)

        # Visibility
        self.is_visible = False

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        if self.is_visible:
            indicator = self.indicators[self.specialtile_index]
            display.blit(indicator, self.position)

    # Update ------------------------------------------------------ #
    def update(self, start_of_game):
        self.update_visibility(start_of_game)

    def update_visibility(self, start_of_game):
        dt = time.perf_counter() - start_of_game
        if not self.is_visible and dt * 1000 >= 500:
            self.is_visible = True

    def update_colorindex(self, special_idx):
        self.specialtile_index = special_idx