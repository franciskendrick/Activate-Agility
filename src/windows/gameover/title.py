from functions import clip_set_to_list_on_yaxis
from windows.windows import window
import pygame
import json
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", 
        "resources", "windows", "gameover"
        )
    )

# Json
with open(f"{resources_path}/gameover.json") as json_file:
    gameover_data = json.load(json_file)


class Title:
    def __init__(self):
        animation_set = pygame.image.load(
            f"{resources_path}/title_animation.png")
        self.idx = 0

        self.frames = []
        for img in clip_set_to_list_on_yaxis(animation_set):
            # Resize Image
            wd, ht = img.get_size()
            size = (wd * 2, ht * 2)
            img = pygame.transform.scale(img, size)

            # Initialize Rectangle
            rect = pygame.Rect(
                gameover_data["title_position"], 
                img.get_rect().size)

            # Append
            frame = [img, rect]
            self.frames.append(frame)

    def draw(self, display):
        # Get Multiplier
        dt = round(window.delta_time)
        dt_multiplier = round(5 / dt) if dt > 0 else 0
        multiplier = dt_multiplier if dt_multiplier > 0 else 5

        # Reset
        if self.idx >= len(self.frames) * multiplier:
            self.idx = 0

        # Draw
        img, rect = self.frames[self.idx // multiplier]
        display.blit(img, rect)

        # Update
        self.idx += 1
