from functions import clip_set_to_list_on_yaxis
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


class Tiles:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        # Frames
        spriteset = pygame.image.load(
            f"{resources_path}/tiles_animation.png")
        self.frames = clip_set_to_list_on_yaxis(spriteset)

        # Position
        self.position = paused_data["tiles_position"]

        # Index
        self.idx = 0
        self.update = True
        self.frame_limit = 7

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Cancel Update
        if self.idx >= self.frame_limit * 3:
            self.idx = (self.frame_limit * 3) - 1
            self.update = False

        # Draw
        img = self.frames[self.idx // 3]
        display.blit(img, self.position)

        # Update
        if self.update:
            self.idx += 1
