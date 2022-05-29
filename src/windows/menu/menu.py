from windows.windows import window
from .tiles import Tiles
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

        self.tiles = Tiles()
        self.title = Title()
        self.buttons = Buttons()

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Draw Tiles on Original Display
        self.tiles.draw(display)

        # Draw Menu Window on Menu Display
        self.title.draw(self.display)
        self.buttons.draw(self.display)

        # Blit to Menu Display to Original Display
        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)
