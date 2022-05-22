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
    gameover_data = json.load(json_file)


class Status:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        pass

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass
