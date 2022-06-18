from functions import clip_set_to_list_on_xaxis, separate_sets_from_yaxis
import pygame
import json
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", 
        "resources", "player"
        )
    )

# Json
with open(f"{resources_path}/player.json") as json_file:
    player_data = json.load(json_file)


class TeleportSizeDecrease:
    def __init__(self):
        # Get Size Decreasing Images
        spriteset = pygame.image.load(
            f"{resources_path}/player_sizedecreasing.png")

        # Separate Size Decreasing Spriteset to their Directions
        separated_spriteset = separate_sets_from_yaxis(
            spriteset, (255, 0, 0))

        # Put Size Decreasing Images into a Dictionary
        self.images = {
            name: clip_set_to_list_on_xaxis(spriteset) 
                for name, spriteset in zip(
                    player_data["direction_order"], separated_spriteset)
            }

    def draw(self, display):
        pass
