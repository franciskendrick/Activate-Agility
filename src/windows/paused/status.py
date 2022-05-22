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


class Status:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_board()

    def init_board(self):
        img = pygame.image.load(
            f"{resources_path}/status_bkg.png")
        rect = pygame.Rect(
            paused_data["status_positions"]["board"],
            img.get_rect().size)

        self.status_board = [img, rect]

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass
