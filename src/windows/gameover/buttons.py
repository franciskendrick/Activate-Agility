from functions import clip_set_to_list_on_xaxis
from functions.color_palette_swap import palette_swap
from windows.windows import window
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


class Buttons:
    def __init__(self):
        spriteset = pygame.image.load(
            f"{resources_path}/buttons.png")
        order = ["play", "options", "menu"]
        images = clip_set_to_list_on_xaxis(spriteset)
        enlarge = 3 * window.enlarge

        # Palette
        hover_palette = {
            (232, 193, 112): (231, 213, 179),
            (222, 158, 65): (232, 193, 112),
            (190, 119, 43): (222, 158, 65),
            (32, 46, 55): (57, 74, 80),
            (21, 29, 40): (32, 46, 55),
            (9, 10, 20): (16, 20, 31),
            (162, 62, 140): (198, 81, 151),
            (122, 54, 123): (162, 62, 140)}
        
        # Buttons
        self.buttons = {}
        for name, img in zip(order, images):
            # Initialize
            hover_img = palette_swap(
                img.convert(), hover_palette)
            rect = pygame.Rect(
                gameover_data["buttons_position"][name],
                img.get_rect().size)
            hitbox = pygame.Rect(
                rect.x * enlarge, rect.y * enlarge,
                rect.width * enlarge, rect.height * enlarge)

            # Append
            button = [
                False,  # is_hovered
                img,  # orig image
                hover_img,  # hover image
                rect,  # rect
                hitbox  # hitbox
            ]
            self.buttons[name] = button

    def draw(self, display):
        for button in self.buttons.values():
            is_hovered, orig_img, hover_img, rect, _ = button
            img = hover_img if is_hovered else orig_img

            display.blit(img, rect)
