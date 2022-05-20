import pygame
import json
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", 
        "resources", "windows", "paused"
        )
    )

# Json
with open(f"{resources_path}/paused.json") as json_file:
    paused_data = json.load(json_file)


class Background:
    def __init__(self):
        img = pygame.image.load(
            f"{resources_path}/background.png")
        rect = pygame.Rect(
            paused_data["background_position"], 
            img.get_rect().size)

        self.background = [img, rect]

    def draw(self, display):
        display.blit(*self.background)
