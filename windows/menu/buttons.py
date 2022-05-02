from functions import clip_set_to_list_on_yaxis, palette_swap
from windows import window
import pygame
import json
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

# Windows
win_size = (
    window.rect.width * window.enlarge,
    window.rect.height * window.enlarge)
win = pygame.display.set_mode(win_size)

# Json
with open(f"{path}/data/menu.json") as json_file:
    menu_data = json.load(json_file)


class Buttons:
    def __init__(self):
        spriteset = pygame.image.load(
            f"{path}/assets/buttons.png")
        order = ["play", "options"]
        images = clip_set_to_list_on_yaxis(spriteset)
        enlarge = 2 * window.enlarge

        # Palette
        hover_palette = {
            (232, 193, 112): (231, 213, 179),
            (222, 158, 65): (232, 193, 112),
            (190, 119, 43): (222, 158, 65),
            (9, 10, 20): (16, 20, 31)}

        # Buttons
        self.buttons = {}
        for name, img in zip(order, images):
            # Initialize
            hover_img = palette_swap(img.convert(), hover_palette)
            img_rect = pygame.Rect(
                menu_data["buttons_position"][name], img.get_rect().size)
            hitbox = pygame.Rect(
                img_rect.x * enlarge, img_rect.y * enlarge,
                img_rect.width * 2 * enlarge, img_rect.height * 2 * enlarge)

            # Resize
            wd, ht = img.get_size()
            size = (wd * 2, ht * 2)
            img = pygame.transform.scale(img, size)
            hover_img = pygame.transform.scale(hover_img, size)

            # Append
            button = [
                False,  # is hovered
                img,  # orig image
                hover_img,  # hover image
                img_rect,  # image rect
                hitbox  # hitbox
            ]
            self.buttons[name] = button

    def draw(self, display):
        for button in self.buttons.values():
            is_hovered, orig_img, hover_img, img_rect, _ = button
            img = hover_img if is_hovered else orig_img

            display.blit(img, img_rect)  # image