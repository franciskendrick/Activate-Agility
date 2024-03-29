from windows.windows import window
from fonts import NumberFont
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


class Animation(NumberFont):
    # Initialize -------------------------------------------------- #
    def __init__(self, score, highscore):
        super().__init__()

        self.init_dropdown()
        self.init_status(score, highscore)

        self.idx = 0
        self.update = True
        self.frame_limit = 7

    def init_dropdown(self):
        # DropDown Image
        self.dropdown_image = pygame.image.load(
            f"{resources_path}/drop_down.png")

        # DropDown Positions
        self.dropdown_positions = []
        for pos in paused_data["dropdown_positions"]["background"]:
            # Get Position
            position = None if pos == [None, None] else pos

            # Append
            self.dropdown_positions.append(position)

    def init_status(self, score, highscore):
        # Status Text
        self.status_text = {
            "score": score,
            "highscore": highscore
        }

        # Status Positions
        self.status_positions = {}
        data_positions = paused_data["dropdown_positions"]["status"]
        for (name, positions) in data_positions.items():
            # Append Item in Status Positions Dictionary
            self.status_positions[name] = []

            # Stat Position
            for pos in positions:
                # Get Position
                position = None if pos == [None, None] else pos

                # Append
                self.status_positions[name].append(position)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Get Multiplier
        dt = round(window.delta_time)
        dt_multiplier = round(3 / dt) if dt > 0 else 0
        multiplier = dt_multiplier if dt_multiplier > 0 else 3

        # Cancel Update
        if self.idx >= self.frame_limit * multiplier:
            self.idx = (self.frame_limit * multiplier) - 1
            self.update = False

        # Draw
        self.draw_dropdown(display, multiplier)
        self.draw_status(display, multiplier)

        # Update
        if self.update:
            self.idx += 1

    def draw_dropdown(self, display, multiplier):
        position = self.dropdown_positions[self.idx // multiplier]
        if position != None:
            display.blit(self.dropdown_image, position)

    def draw_status(self, display, multiplier):
        # Variables
        texts_vls = self.status_text.values()
        positions_vls = self.status_positions.values()

        # Draw Status
        for (text, positions) in zip(texts_vls, positions_vls):
            # Get Position
            pos = positions[self.idx // multiplier]

            # Draw
            if pos != None:
                self.render_font(
                    display, text, pos, enlarge=1, color=(70, 130, 50))
