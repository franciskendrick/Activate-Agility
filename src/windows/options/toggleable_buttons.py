from functions import clip_set_to_list_on_yaxis, palette_swap
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


class ToggleableButtons:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        spriteset = pygame.image.load(
            f"{resources_path}/toggleable_buttons.png")
        order = ["fullscreen", "music", "sound"]
        images = clip_set_to_list_on_yaxis(spriteset)
        enlarge = 3 * window.enlarge

        # Palette
        buttons_palettes = {
            "on": {
                "hover": {
                    (232, 193, 112): (231, 213, 179),
                    (222, 158, 65): (232, 193, 112),
                    (190, 119, 43): (222, 158, 65),
                    (9, 10, 20): (16, 20, 31),
                    (162, 62, 140): (198, 81, 151),
                    (122, 54, 123): (162, 62, 140)}
            },
            "off": {
                "up": {
                    (232, 193, 112): (57, 74, 80),
                    (222, 158, 65): (32, 46, 55),
                    (190, 119, 43): (21, 29, 40),
                    (9, 10, 20): (9, 10, 20),
                    (162, 62, 140): (64, 39, 81),
                    (122, 54, 123): (30, 29, 57)},
                "hover": {
                    (232, 193, 112): (87, 114, 119),
                    (222, 158, 65): (57, 74, 80),
                    (190, 119, 43): (32, 46, 55),
                    (9, 10, 20): (16, 20, 31),
                    (122, 54, 123): (64, 39, 81),
                    (162, 62, 140): (122, 54, 123)}
            }
        }

        # Buttons
        self.buttons = {}
        for name, img in zip(order, images):
            # Initialize Toggle Status
            toggle_status = window.gamestatus_data["options_data"][name]

            # Initialize Images
            palette_swapped_imgs = {}
            for toggle_state, palettes in buttons_palettes.items():
                palette_swapped_imgs[toggle_state] = {}
                for state, palette in palettes.items():
                    palette_swapped_imgs[toggle_state][state] = palette_swap(
                        img.convert(), palette)
            else:
                palette_swapped_imgs["on"]["up"] = img

            # Initialize Image Rectangle
            rect = pygame.Rect(
                options_data["buttons_position"][name],
                img.get_rect().size)

            # Initialize Hitbox
            hitbox = pygame.Rect(
                rect.x * enlarge, rect.y * enlarge,
                rect.width * enlarge, rect.height * enlarge)

            # Append
            button = [
                False,  # is_hovered
                toggle_status,  # toggle status
                palette_swapped_imgs,  # palette swapped images
                rect,  # image rectangle
                hitbox  # hibox
            ]
            self.buttons[name] = button

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        for button in self.buttons.values():
            is_hovered, toggle_status, palette_swapped_imgs, rect, _ = button
            toggle_imgs = palette_swapped_imgs["on"] if toggle_status else palette_swapped_imgs["off"]
            img = toggle_imgs["hover"] if is_hovered else toggle_imgs["up"]

            display.blit(img, rect)

    # Functions --------------------------------------------------- #
    def get_button_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for (name, button) in self.buttons.items():
                *_, hitbox = button

                mouse_pos = pygame.mouse.get_pos()
                if hitbox.collidepoint(mouse_pos):
                    self.buttons[name][1] = not self.buttons[name][1]
                    return name

    def handle_mousemotion(self, event):
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons.values():
                *_, hitbox = button

                mouse_pos = pygame.mouse.get_pos()
                button[0] = True if hitbox.collidepoint(mouse_pos) else False
