from windows.windows import window
from .animation import Animation
from .tiles import Tiles
from .background import Background
from .title import Title
from .status import Status
from .buttons import Buttons
import pygame

pygame.init()


class Paused:
    # Initialize -------------------------------------------------- #
    def __init__(self, score, highscore):
        wd, ht = window.rect.size
        self.display = pygame.Surface(
            (wd // 3, ht // 3), pygame.SRCALPHA)
        self.display.convert_alpha()
        self.rect = pygame.Rect((
            0, 0), self.display.get_size())

        self.status = Status(score, highscore)
        self.animation = Animation(
            self.status.score["text"],
            self.status.high_score["text"])
        self.tiles = Tiles()
        self.background = Background()
        self.title = Title()
        self.buttons = Buttons()

    # Draw -------------------------------------------------------- #
    def draw_background(self, display):
        # Fill Pause Display with Transparent Background
        self.display.fill((0, 0, 0, 0))

        # Draw Pause Tiles on Pause Display
        self.tiles.draw(display)

    def draw_pausewindow(self, display):
        # Draw Pause Window on Pause Display
        if self.animation.update:
            self.animation.draw(self.display)
        else:
            self.background.draw(self.display)
            self.title.draw(self.display)
            self.status.draw(self.display)
            self.buttons.draw(self.display)

        # Blit to Pause Display to Original Display
        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)
