from functions import clip_set_to_list_on_xaxis
from windows.windows import window
import pygame
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", 
        "resources", "cursors"
        )
    )


class TransitionAnimation:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_animationvariables()
        self.init_images()
        self.init_rect()
        
    def init_images(self):
        spriteset = pygame.image.load(
            f"{resources_path}/cursortocrosshair.png")

        # Images
        self.images = clip_set_to_list_on_xaxis(spriteset)

    def init_rect(self):
        # Offset
        self.offset = (-7, -7)

        # Rectangle
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_offset, y_offset = self.offset
        wd, ht = self.images[self.idx].get_rect().size
        self.rect = pygame.Rect(
            (mouse_x - x_offset) - (wd / 2), 
            (mouse_y - y_offset) - (wd / 2),
            wd, ht)

    def init_animationvariables(self):
        self.idx = 0
        self.frame_limit = 25
        self.is_finished = False

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        if pygame.mouse.get_focused():  # checks if mouse is in the window
            # Animation is Finished
            if self.idx >= self.frame_limit:
                self.idx = self.frame_limit - 1
                self.is_finished = True

            # Draw
            img = self.images[self.idx]
            display.blit(img, self.rect)

        # Update
        if not self.is_finished:
            self.idx += 1

    # Update ------------------------------------------------------ #
    def update(self, player):
        # Updates Crosshair's Position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_offset, y_offset = self.offset
        self.rect.center = (
            (mouse_x - x_offset) / window.enlarge, 
            (mouse_y - y_offset) / window.enlarge)

        # Reset Animation Variables
        if player.stats["mana"] != player.maximum_stats["mana"] and self.is_finished:
            self.init_animationvariables()
