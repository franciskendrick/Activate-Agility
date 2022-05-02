import pygame
import json
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

# Json
with open(f"{path}/data/gameover.json") as json_file:
    gameover_data = json.load(json_file)


class Background:
    def __init__(self):
        img = pygame.image.load(
            f"{path}/assets/background.png")
        rect = pygame.Rect(
            gameover_data["background_position"], 
            img.get_rect().size)

        self.background = [img, rect]

    def draw(self, display):
        pass 
