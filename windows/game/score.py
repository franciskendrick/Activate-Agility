from functions import clip_set_to_list_on_xaxis
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

titles = pygame.image.load(
    f"{path}/assets/score_titles.png")
score_title, highscore_title = clip_set_to_list_on_xaxis(titles)


class Score:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        pass

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass


class HighScore:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        pass

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass
