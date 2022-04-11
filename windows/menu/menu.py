from windows import window
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

# Windows
win_size = (
    window.rect.width * window.enlarge,
    window.rect.height * window.enlarge)
win = pygame.display.set_mode(win_size)


class Title:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_board()

    def init_board(self):
        img = pygame.image.load(
            f"{path}/assets/title_background.png")
        rect = pygame.Rect(82, 37, *img.get_rect().size)
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
        wd, ht = window.rect.size
        self.display = pygame.Surface((wd // 2, ht // 2), pygame.SRCALPHA)
        self.display.convert_alpha()
        self.rect = pygame.Rect((0, 0), self.display.get_size())

        self.title = Title()

    def draw(self, display):
        self.display.fill((0, 0, 0, 0))

        # Menu
        self.title.draw(self.display)

        # Blit to Display
        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)


menu = Menu()
