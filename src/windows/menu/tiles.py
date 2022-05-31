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
        self.init_animation()

        self.position = paused_data["tiles_position"]
        self.animation_idx = 0
        self.frame_idx = 0

    def init_animation(self):
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
            
            # Load Frames 
            for frame in frames:
                frame_path = f"{resources_path}/tiles/{animation_folder}/{frame}"

                image = pygame.image.load(frame_path)

                animation.append(image)

            # Append Frames to Animations
            self.animations.append(animation)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        animation = self.animations[self.animation_idx]

        # Reset Frame Index
        if self.frame_idx >= len(animation) * 3:
            self.frame_idx = 0
            self.animation_idx += 1

            # Reset Animation Index
            if self.animation_idx >= len(self.animations):
                self.animation_idx = 0
        
        # Draw
        img = animation[self.frame_idx // 3]
        display.blit(img, self.position)

        # Update
        self.frame_idx += 1
