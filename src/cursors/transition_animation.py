from functions import clip_set_to_list_on_xaxis
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


class TransitionAnimation:
    def __init__(self):
        pass

    def draw(self):
        pass
