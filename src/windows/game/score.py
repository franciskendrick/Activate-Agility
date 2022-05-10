from .number_font import NumberFont
import pygame
import json
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


class Score(NumberFont):
    # Initialize -------------------------------------------------- #
    def __init__(self):
        super().__init__()

        self.init_title()
        self.init_numbers()
        self.value = 0

    def init_title(self):
        # Image
        title = pygame.image.load(
            f"{resources_path}/score.png")

        # Initialize
        wd, ht = title.get_rect().size
        resized_image = pygame.transform.scale(
            title, (wd * 2, ht * 2))
        rect = pygame.Rect(
            game_data["score_positions"]["title"], 
            resized_image.get_rect().size)

        # Append
        self.title = [resized_image, rect]

    def init_numbers(self):
        self.number_position = game_data["score_positions"]["numbers"]

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Title
        display.blit(*self.title)

        # Numbers
        self.render_font(
            display, str(self.value), self.number_position)
