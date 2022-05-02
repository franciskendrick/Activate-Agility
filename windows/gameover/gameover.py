from windows import window
from .background import Background
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class GameOver:
    def __init__(self):
        wd, ht = window.rect.size
        self.display = pygame.Surface(
            (wd // 3, ht // 3), pygame.SRCALPHA)
        self.display.convert_alpha()
        self.rect = pygame.Rect((
            0, 0), self.display.get_size())

        self.background = Background()

    def draw(self, display):
        pass


gameover = GameOver()
