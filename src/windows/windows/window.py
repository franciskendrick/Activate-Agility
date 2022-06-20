import pygame
import json
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", 
        "resources"
        )
    )


class Window:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        # Monitor Size
        self.monitor_size = [
            pygame.display.Info().current_w, 
            pygame.display.Info().current_h]

        # Window
        self.rect = pygame.Rect(0, 0, 640, 360)
        self.enlarge = max(
            self.monitor_size[0] / self.rect.width,
            self.monitor_size[1] / self.rect.height)
        
        # Room
        self.room_rect = pygame.Rect(32, 60, 576, 272)

        # Game Status
        with open(f"{resources_path}/gamestatus.json") as json_file:
            self.gamestatus_data = json.load(json_file)

        # Framerate
        self.framerate = 30

    # Update ------------------------------------------------------ #
    def update_gameinfo(self, highscore_value):
        # Get Handle Info
        handle_gamestatus = self.gamestatus_data.copy()

        # Edit Handle Info
        handle_gamestatus["highscore"] = highscore_value

        # Append
        with open(f"{resources_path}/gamestatus.json", "w") as json_file:
            json.dump(handle_gamestatus, json_file)


window = Window()
