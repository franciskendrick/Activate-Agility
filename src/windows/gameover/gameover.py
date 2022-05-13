from windows.windows import window
from .background import Background
from .title import Title
from .status import Status
from .buttons import Buttons
import pygame

pygame.init()


class GameOver:
    # Initialize
    def __init__(self, score, highscore, endtime):
        wd, ht = window.rect.size
        self.display = pygame.Surface(
            (wd // 3, ht // 3), pygame.SRCALPHA)
        self.display.convert_alpha()
        self.rect = pygame.Rect((
            0, 0), self.display.get_size())

        self.background = Background()
        self.title = Title()
        self.status = Status(score, highscore, endtime)
        self.buttons = Buttons()

    # Draw
    def draw(self, display):
        # Background
        self.background.draw(self.display)
        self.title.draw(self.display)
        self.status.draw(self.display)
        self.buttons.draw(self.display)

        # Blit to Display
        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)

    # Functions
    def get_button_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for (name, button) in self.buttons.buttons.items():
                *_, hitbox = button

                mouse_pos = pygame.mouse.get_pos()
                if hitbox.collidepoint(mouse_pos):
                    return name

    def handle_mousemotion(self, event):
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons.buttons.values():
                *_, hitbox = button

                mouse_pos = pygame.mouse.get_pos()
                button[0] = True if hitbox.collidepoint(mouse_pos) else False
