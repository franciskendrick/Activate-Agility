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


class SpecialColorIdentifier:
    # Initialize -------------------------------------------------- #
    def __init__(self, specialtile_color):
        self.init(specialtile_color)

    def init(self, specialtile_color):
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
        self.update_colorindex(specialtile_color)

        # Visibility
        self.is_visible = False

    def init_startofgame(self, start_of_game):
        self.start_of_game = start_of_game

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        if self.is_visible:
            indicator = self.indicators[self.specialtile_index]
            display.blit(indicator, self.position)

    # Update ------------------------------------------------------ #
    def update(self, sound):
        dt = time.perf_counter() - self.start_of_game
        if not self.is_visible and dt * 1000 >= 250:
            # Update Visibility
            self.is_visible = True

            # Play Sound
            play_audio = sound.audioplaying_switchcase[self.specialtile_index]
            play_audio()

    def update_colorindex(self, special_idx):
        self.specialtile_index = special_idx
