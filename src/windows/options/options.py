from windows.windows import window
import pygame

pygame.init()


class Options:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        wd, ht = window.rect.size
        self.display = pygame.Surface(
            (wd // 2, ht // 2), pygame.SRCALPHA)
        self.display.convert_alpha()
        self.rect = pygame.Rect((
            0, 0), self.display.get_size())

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Blit to Menu Display to Original Display
        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)
