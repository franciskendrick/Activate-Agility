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
    # Initialize -------------------------------------------------- #
    def __init__(self, score, highscore, endtime):
        super().__init__()

        self.init_dropdown()
        self.init_status(score, highscore, endtime)

        self.idx = 0
        self.update = True
        self.frame_limit = 7

    def init_dropdown(self):
        # DropDown Image
        self.dropdown_image = pygame.image.load(
            f"{resources_path}/drop_down.png")

        # DropDown Positions
        self.dropdown_positions = []
        for pos in gameover_data["dropdown_positions"]["background"]:
            # Get Position
            position = None if pos == [None, None] else pos

            # Append
            self.dropdown_positions.append(position)

    def init_status(self, score, highscore, endtime):
        # Status Text
        self.status_text = {
            "score": score,
            "highscore": highscore,
            "endtime": endtime
        }

        # Status Positions
        self.status_positions = {}
        data_positions = gameover_data["dropdown_positions"]["status"]
        for (name, positions) in data_positions.items():
            # Append Item in Status Positions Dictionary
            self.status_positions[name] = []

            # Single Status Position
            for pos in positions:
                # Get Position
                position = None if pos == [None, None] else pos

                # Append
                self.status_positions[name].append(position)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Cancel Update
        if self.idx >= self.frame_limit * 3:
            self.idx = (self.frame_limit - 1) * 3
            self.update = False

        # Draw
        self.draw_dropdown(display)

        # Update
        if self.update:
            self.idx += 1

    def draw_dropdown(self, display):
        position = self.dropdown_positions[self.idx // 3]
        if position != None:
            display.blit(self.dropdown_image, position)
