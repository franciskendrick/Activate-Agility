import pygame
import json
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", 
        "resources", "windows", "options"
        )
    )

# Json
with open(f"{resources_path}/options.json") as json_file:
    options_data = json.load(json_file)


class Title:
    def __init__(self):
        pass

    def draw(self, display):
        pass
