import pygame
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", 
        "resources", "audio"
        )
    )


class Music:
    def __init__(self):
        pygame.mixer.music.load(
            f"{resources_path}/ES_Bozz - William Benckert.mp3")
        
        pygame.mixer.music.play(-1)

    def update(self):
        pass
