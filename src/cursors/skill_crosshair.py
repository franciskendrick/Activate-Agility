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


class SkillCrosshair:
    def __init__(self):
        # Image
        self.img = pygame.image.load(
            f"{resources_path}/skill_crosshair.png")

        # Rectangle
        mouse_x, mouse_y = pygame.mouse.get_pos()
        wd, ht = self.img.get_rect().size
        self.rect = pygame.Rect(
            mouse_x - (wd / 2), mouse_y - (wd / 2),
            wd, ht)

    def draw(self, display):
        if pygame.mouse.get_focused():  # checks if mouse is in the window
            display.blit(self.img, self.rect)

    def update(self):
        # Updates Crosshair's Position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.center = (
            mouse_x / window.enlarge, 
            mouse_y / window.enlarge)
