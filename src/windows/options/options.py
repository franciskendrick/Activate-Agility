from windows.windows import window
from .background import Background
from .title import Title
import pygame

pygame.init()


class Options:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        wd, ht = window.rect.size
        self.display = pygame.Surface(
            (wd // 3, ht // 3), pygame.SRCALPHA)
        self.display.convert_alpha()
        self.rect = pygame.Rect((
            0, 0), self.display.get_size())

        self.background = Background()
        self.title = Title()

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Draw Options Window on Options Display
        self.background.draw(self.display)
        self.title.draw(self.display)

        # Blit to Options Display to Original Display
        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)
