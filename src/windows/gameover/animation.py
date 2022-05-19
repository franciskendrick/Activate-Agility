from fonts import NumberFont
import pygame
import json
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", 
        "resources", "windows", "gameover"
        )
    )

# Json
with open(f"{resources_path}/gameover.json") as json_file:
    gameover_data = json.load(json_file)


class Animation(NumberFont):
    # Initialize
    def __init__(self):
        super().__init__()

        # DropDown 
        self.dropdown_image = pygame.image.load(
            f"{resources_path}/drop_down.png")
        self.dropdown_positions = []
        for pos in gameover_data["dropdown_positions"]["background"]:
            position = None if pos == [None, None] else pos
            self.dropdown_positions.append(position)

        # Index
        self.idx = 0

    # Draw
    def draw(self, display):
        pass
