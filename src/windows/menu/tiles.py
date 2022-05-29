import pygame
import json
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", 
        "resources", "windows", "menu"
        )
    )

# Json
with open(f"{resources_path}/menu.json") as json_file:
    paused_data = json.load(json_file)


class Tiles:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.animations = []
        
        # Get Animation Folders List
        animation_folders = os.listdir(
            f"{resources_path}/tiles")

        # Loop through Animation Folders
        for animation_folder in animation_folders:
            # Initialize an Animation List
            animation = []

            # Get Frames from Animation Folder
            frames = os.listdir(
                f"{resources_path}/tiles/{animation_folder}")
            
            # Append Frames to Animations
            animation.append(frames)
            self.animations.append(animation)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass
