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
        order = ["animation", "music", "sound"]
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
                    (162, 62, 140): (122, 54, 123),
                    (122, 54, 123): (64, 39, 81)}
            }
        }

        # Buttons
        self.buttons = {}
        for name, img in zip(order, images):
            # Initialize Images
            palette_swapped_imgs = {}
            for toggle_state, palettes in buttons_palettes.items():
                palette_swapped_imgs[toggle_state] = {}
                for state, palette in palettes.items():
                    palette_swapped_imgs[toggle_state][state] = palette_swap(
                        img.convert(), palette)
            else:
                palette_swapped_imgs["on"]["orig"] = img

            # Initialize Image Rectangle
            img_rect = pygame.Rect(
                options_data["buttons_position"][name],
                img.get_rect().size)

            # Initialize Hitbox
            hitbox = pygame.Rect(
                img_rect.x * enlarge, img_rect.y * enlarge,
                img_rect.width * enlarge, img_rect.height * enlarge)

            # Append
            button = [
                False,  # is_hovered
                True,  # toggle status
                palette_swapped_imgs,  # palette swapped images
                img_rect,  # image rectangle
                hitbox  # hibox
            ]
            self.buttons[name] = button

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass

    # Functions --------------------------------------------------- #
    def get_button_pressed(self, event):
        pass

    def handle_mousemotion(self, event):
        pass
