from windows.windows import window
from .animation import Animation
from .background import Background
from .title import Title
from .redirect_buttons import RedirectButtons
from .toggleable_buttons import ToggleableButtons
import pygame

pygame.init()


class Options:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        wd, ht = window.rect.size
        self.display = pygame.Surface(
            (wd // 3, ht // 3), pygame.SRCALPHA)
        self.display.convert_alpha()
        self.rect = pygame.Rect(
            (0, 0), self.display.get_size())

        self.background = Background()
        self.title = Title()
        self.redirect_buttons = RedirectButtons()
        self.toggleable_buttons = ToggleableButtons()

    def init_animation(self):
        self.animation = Animation(
            self.toggleable_buttons.buttons)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Fill Pause Display with Transparent Background
        self.display.fill((0, 0, 0, 0))
        
        # Draw Options Window on Options Display
        if self.animation.update:
            self.animation.draw(self.display)
        else:
            self.background.draw(self.display)
            self.title.draw(self.display)
            self.redirect_buttons.draw(self.display)
            self.toggleable_buttons.draw(self.display)

        # Blit to Options Display to Original Display
        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)
