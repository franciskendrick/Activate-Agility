from functions import clip_set_to_list_on_yaxis, palette_swap
from windows import window, background
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


class Title:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_board()
        self.init_title()

    def init_board(self):
        # Initialize
        img = pygame.image.load(
            f"{path}/assets/title_background.png")
        rect = pygame.Rect(
            menu_data["board_position"], img.get_rect().size)

        # Append
        self.board = [img, rect]

    def init_title(self):
        animation_set = pygame.image.load(
            f"{path}/assets/title_animation.png")
        self.idx = 0

        # Frames
        self.frames = []
        for img in clip_set_to_list_on_yaxis(animation_set):
            # Initialize
            img_rect = pygame.Rect(
                menu_data["title_position"], img.get_size())

            # Resize
            wd, ht = img.get_size()
            size = (wd * 3, ht * 3)
            img = pygame.transform.scale(img, size)

            # Append
            slide = [
                img,  # orig image
                img_rect  # image rect
            ]
            self.frames.append(slide)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        self.draw_board(display)
        self.draw_title(display)

    def draw_board(self, display):
        display.blit(*self.board)

    def draw_title(self, display):
        # Reset
        if self.idx >= len(self.frames) * 5:
            self.idx = 0

        # Draw
        img, rect = self.frames[self.idx // 5]
        display.blit(img, rect)

        # Update
        self.idx += 1


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


class Menu:
    def __init__(self):
        wd, ht = window.rect.size
        self.display = pygame.Surface((wd // 2, ht // 2), pygame.SRCALPHA)
        self.display.convert_alpha()
        self.rect = pygame.Rect((0, 0), self.display.get_size())

        self.title = Title()
        self.buttons = Buttons()

    def draw(self, display):
        # Background
        background.draw_walls(display)

        # Menu
        self.title.draw(self.display)
        self.buttons.draw(self.display)

        # Blit to Display
        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)

    def get_button_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for (name, button) in self.buttons.buttons.items():
                *_, hitbox = button
                
                mouse_pos = pygame.mouse.get_pos()
                if hitbox.collidepoint(mouse_pos):
                    return name

    def handle_mousemotion(self, event):
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons.buttons.values():
                *_, hitbox = button

                mouse_pos = pygame.mouse.get_pos()
                button[0] = True if hitbox.collidepoint(mouse_pos) else False


menu = Menu()
