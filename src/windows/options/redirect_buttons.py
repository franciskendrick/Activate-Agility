from functions import clip_set_to_list_on_xaxis, palette_swap
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


class RedirectButtons:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        spriteset = pygame.image.load(
            f"{resources_path}/redirect_buttons.png")
        order = ["back", "play", "menu"]
        images = clip_set_to_list_on_xaxis(spriteset)
        enlarge = 3 * window.enlarge

        # Palette
        hover_palette = {
            (232, 193, 112): (231, 213, 179),
            (222, 158, 65): (232, 193, 112),
            (190, 119, 43): (222, 158, 65),
            (32, 46, 55): (57, 74, 80),
            (21, 29, 40): (32, 46, 55),
            (16, 20, 31): (21, 29, 40),
            (9, 10, 20): (16, 20, 31),
            (162, 62, 140): (198, 81, 151),
            (122, 54, 123): (162, 62, 140)}

        # Buttons
        self.buttons = {}
        for name, img in zip(order, images):
            # Intialize
            hover_img = palette_swap(
                img.convert(), hover_palette)
            rect = pygame.Rect(
                options_data["buttons_position"][name],
                img.get_rect().size)
            hitbox = pygame.Rect(
                rect.x * enlarge, rect.y * enlarge,
                rect.width * enlarge, rect.height * enlarge)

            # Append
            button = [
                False,  # is_hovered
                img,  # orig image
                hover_img,  # hover image
                rect,  # rectangle
                hitbox  # hitbox
            ]
            self.buttons[name] = button

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        for button in self.buttons.values():
            is_hovered, orig_img, hover_img, rect, _ = button
            img = hover_img if is_hovered else orig_img

            display.blit(img, rect)

    # Functions --------------------------------------------------- #
    def get_button_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for (name, button) in self.buttons.items():
                *_, hitbox = button

                mouse_pos = pygame.mouse.get_pos()
                if hitbox.collidepoint(mouse_pos):
                    return name

    def handle_mousemotion(self, event):
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons.values():
                *_, hitbox = button

                mouse_pos = pygame.mouse.get_pos()
                button[0] = True if hitbox.collidepoint(mouse_pos) else False
