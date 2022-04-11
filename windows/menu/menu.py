import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class Title:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_board()

    def init_board(self):
        img = pygame.image.load(
            f"{path}/assets/title_background.png")
        rect = pygame.Rect(164, 74, *img.get_rect())
        self.board = [img, rect]

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        self.draw_board(display)

    def draw_board(self, display):
        display.blit(*self.board)


class Buttons:
    def __init__(self):
        pass

    def draw(self, display):
        pass


class Menu:
    def __init__(self):
        pass

    def draw(self, display):
        pass


menu = Menu()
