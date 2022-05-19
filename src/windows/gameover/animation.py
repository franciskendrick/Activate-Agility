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

        # Animation
        self.idx = 0
        self.update = True
        self.frame_limit = 7

    # Draw
    def draw(self, display):
        # Cancel Update
        if self.idx >= self.frame_limit * 3:
            self.idx = (self.frame_limit - 1) * 3
            self.update = False

        # Draw
        position = self.dropdown_positions[self.idx // 3]
        if position != None:
            display.blit(self.dropdown_image, position)

        # Update
        if self.update:
            self.idx += 1
