from functions import clip_set_to_list_on_yaxis
import pygame
import json
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..", "..", "..",
        "resources", "windows", "menu"
        )
    )

# Json
with open(f"{resources_path}/menu.json") as json_file:
    menu_data = json.load(json_file)


class Animation:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        spriteset = pygame.image.load(
            f"{resources_path}/drop_down.png")
        title, buttons = clip_set_to_list_on_yaxis(spriteset)

        self.init_title(title)
        self.init_buttons(buttons)

        self.idx = 0
        self.update = True
        self.frame_limit = 9

    def init_title(self, image):
        # Title Image
        self.title_image = image

        # Title Positions
        self.title_positions = []
        for pos in menu_data["dropdown_positions"]["title"]:
            # Get Position
            position = None if pos == [None, None] else pos

            # Append
            self.title_positions.append(position)

    def init_buttons(self, image):
        # Buttons Image
        self.buttons_image = image

        # Buttons Positions
        self.buttons_positions = []
        for pos in menu_data["dropdown_positions"]["buttons"]:
            # Get Position
            position = None if pos == [None, None] else pos

            # Append
            self.buttons_positions.append(position)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Cancel Update
        if self.idx >= self.frame_limit * 3:
            self.idx = (self.frame_limit * 3) - 1
            self.update = False

        # Draw
        self.draw_title(display)
        self.draw_buttons(display)

        # Update
        if self.update:
            self.idx += 1

    def draw_title(self, display):
        position = self.title_positions[self.idx // 3]
        if position != None:
            display.blit(self.title_image, position)

    def draw_buttons(self, display):
        position = self.buttons_positions[self.idx // 3]
        if position != None:
            display.blit(self.buttons_image, position)
