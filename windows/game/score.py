from functions import clip_set_to_list_on_xaxis
from .number_font import NumberFont
import pygame
import json
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

# Json
with open(f"{path}/data/game.json") as json_file:
    game_data = json.load(json_file)

# Titles
titles = pygame.image.load(
    f"{path}/assets/score_titles.png")
score_title, highscore_title = clip_set_to_list_on_xaxis(titles)


class Score(NumberFont):
    # Initialize -------------------------------------------------- #
    def __init__(self):
        super().__init__()

        self.init_title()
        self.init_numbers()
        self.score = 0

    def init_title(self):
        # Initialize
        wd, ht = score_title.get_rect().size
        resized_image = pygame.transform.scale(
            score_title, (wd * 2, ht * 2))
        rect = pygame.Rect(
            game_data["score"]["title"], 
            resized_image.get_rect().size)

        # Append
        self.title = [resized_image, rect]

    def init_numbers(self):
        self.number_position = game_data["score"]["numbers"]

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Title
        display.blit(*self.title)

        # Numbers
        self.render_font(
            display, str(self.score), self.number_position)
