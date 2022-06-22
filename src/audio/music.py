import pygame
import json
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
        # Get Background Music
        pygame.mixer.music.load(
            f"{resources_path}/ES_Bozz - William Benckert.mp3")
        pygame.mixer.music.set_volume(0.5)

        # Get GameStatus Data
        gamestatus_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), 
                "..", "..", 
                "resources", "gamestatus.json"
                )
            )
        with open(gamestatus_path) as json_file:
            gamestatus_data = json.load(json_file)

        # Play Background Music According to GameStatus Data
        if gamestatus_data["options_data"]["music"]:
            pygame.mixer.music.play(-1)
            self.played = True
        else:
            self.played = False

    def update(self):
        pass
