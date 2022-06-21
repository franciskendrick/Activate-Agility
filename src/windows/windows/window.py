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
    def update_gameinfo(self, highscore_value, options_toggleable_btns):
        # Get Handle Info
        handle_gamestatus = self.gamestatus_data.copy()

        # Edit Highscore Value
        handle_gamestatus["highscore"] = highscore_value

        # Edit Options
        handle_gamestatus["options_data"]["fullscreen"] = options_toggleable_btns["fullscreen"][1]
        handle_gamestatus["options_data"]["music"] = options_toggleable_btns["music"][1]
        handle_gamestatus["options_data"]["sound"] = options_toggleable_btns["sound"][1]

        # Append
        with open(f"{resources_path}/gamestatus.json", "w") as json_file:
            json.dump(handle_gamestatus, json_file)


window = Window()
