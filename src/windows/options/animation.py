from windows.windows import window
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


class Animation:
    # Initialize -------------------------------------------------- #
    def __init__(self, toggleable_buttons):
        self.init_dropdown()
        self.init_toggleablebuttons(toggleable_buttons)

        self.idx = 0
        self.update = True
        self.frame_limit = 7

    def init_dropdown(self):
        # DropDown Image
        self.dropdown_image = pygame.image.load(
            f"{resources_path}/drop_down.png")

        # DropDown Positions
        self.dropdown_positions = []
        for pos in options_data["dropdown_positions"]["background"]:
            # Get Position
            position = None if pos == [None, None] else pos

            # Append
            self.dropdown_positions.append(position)

    def init_toggleablebuttons(self, toggleable_buttons):
        # Toggleable Buttons Images
        self.toggleable_btns_images = {}
        for (name, button) in toggleable_buttons.items():
            # Get Toggleable Button Image
            is_hovered, toggle_status, palette_swapped_imgs, *_ = button
            toggle_imgs = palette_swapped_imgs["on"] if toggle_status else palette_swapped_imgs["off"]
            img = toggle_imgs["hover"] if is_hovered else toggle_imgs["up"]

            # Append Image
            self.toggleable_btns_images[name] = img

        # Toggleable Buttons Positions
        self.toggleable_btns_positions = {}
        data_positions = options_data["dropdown_positions"]["toggleable_buttons"]
        for (name, positions) in data_positions.items():
            # Append Item in Status Positions Dictionary
            self.toggleable_btns_positions[name] = []

            # Toggleable Button Position
            for pos in positions:
                # Get Position
                position = None if pos == [None, None] else pos 

                # Append
                self.toggleable_btns_positions[name].append(position)
        
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
        self.draw_toggleablebuttons(display, multiplier)

        # Update
        if self.update:
            self.idx += 1

    def draw_dropdown(self, display, multiplier):
        position = self.dropdown_positions[self.idx // multiplier]
        if position != None:
            display.blit(self.dropdown_image, position)

    def draw_toggleablebuttons(self, display, multiplier):
        for (img, positions) in zip(
                self.toggleable_btns_images.values(), 
                self.toggleable_btns_positions.values()):
            # Get Position
            pos = positions[self.idx // multiplier]

            # Draw
            if pos != None:
                display.blit(img, pos)
