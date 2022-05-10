import pygame
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", 
        "resources", "windows", "windows"
        )
    )


class Background:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.color = (16, 20, 31)
        self.walls = pygame.image.load(
            f"{resources_path}/walls.png")

    # Draw -------------------------------------------------------- #
    def draw_walls(self, display):
        display.blit(self.walls, (26, 54))


background = Background()
