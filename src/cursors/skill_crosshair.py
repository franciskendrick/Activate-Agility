import pygame
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", 
        "resources", "cursors"
        )
    )   


class SkillCrosshair:
    def __init__(self):
        pass

    def draw(self, display):
        pass

    def update(self):
        pass
