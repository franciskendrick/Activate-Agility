from windows.windows import window
from .animation import Animation
from .background import Background
from .title import Title
from .status import Status
from .buttons import Buttons
import pygame
import time

pygame.init()


class GameOver:
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
        self.buttons = Buttons()

    def init_status(self, score, highscore, start_of_game):
        self.status = Status(
            score, 
            highscore, 
            time.perf_counter() - start_of_game)
        self.animation = Animation(
            self.status.score["text"],
            self.status.high_score["text"],
            self.status.end_time["text"])

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Fill GameOver Display with Transparent Background
        self.display.fill((0, 0, 0, 0))

        # Draw GameOver Window on GameOver Display
        if self.animation.update:
            self.animation.draw(self.display)
        else:
            self.background.draw(self.display)
            self.title.draw(self.display)
            self.status.draw(self.display)
            self.buttons.draw(self.display)

        # Blit GameOver Display to Original Display
        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)
