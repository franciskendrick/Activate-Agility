from windows.windows import window
from .title import Title
from .buttons import Buttons
import pygame

pygame.init()


class Menu:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        wd, ht = window.rect.size
        self.display = pygame.Surface(
            (wd // 2, ht // 2), pygame.SRCALPHA)
        self.display.convert_alpha()
        self.rect = pygame.Rect((
            0, 0), self.display.get_size())

        self.title = Title()
        self.buttons = Buttons()

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Menu
        self.title.draw(self.display)
        self.buttons.draw(self.display)

        # Blit to Display
        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)
