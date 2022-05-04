import pygame
import json
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

# Json
with open(f"{path}/data/gameover.json") as json_file:
    menu_data = json.load(json_file)


class Buttons:
    def __init__(self):
        pass

    def draw(self, display):
        pass
