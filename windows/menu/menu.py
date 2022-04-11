from functions import clip_set_to_list_on_yaxis
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
        pass

    def draw(self, display):
        pass


class Menu:
    def __init__(self):
        wd, ht = window.rect.size
        self.display = pygame.Surface((wd // 2, ht // 2), pygame.SRCALPHA)
        self.display.convert_alpha()
        self.rect = pygame.Rect((0, 0), self.display.get_size())

        self.title = Title()

    def draw(self, display):
        self.display.fill((0, 0, 0, 0))

        # Menu
        self.title.draw(self.display)

        # Blit to Display
        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)


menu = Menu()
