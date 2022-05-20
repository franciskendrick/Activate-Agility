from functions import clip_set_to_list_on_yaxis
import pygame
import json
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", 
        "resources", "windows", "paused"
        )
    )

# Json
with open(f"{resources_path}/paused.json") as json_file:
    paused_data = json.load(json_file)


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
                paused_data["title_position"], 
                img.get_rect().size)

            # Append
            frame = [img, rect]
            self.frames.append(frame)

    def draw(self, display):
        pass
