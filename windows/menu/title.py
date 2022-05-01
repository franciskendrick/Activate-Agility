from functions import clip_set_to_list_on_yaxis
import pygame
import json
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

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
