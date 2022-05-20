from windows.windows import window
from .background import Background
import pygame

pygame.init()


class Paused:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        wd, ht = window.rect.size
        self.display = pygame.Surface(
            (wd // 3, ht // 3), pygame.SRCALPHA)
        self.display.convert_alpha()
        self.rect = pygame.Rect((
            0, 0), self.display.get_size())

        self.background = Background()

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Fill with Transparent Background
        self.display.fill((0, 0, 0, 0))

        # Draw GameOver
        self.background.draw(self.display)

        # Blit to Display
        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)
