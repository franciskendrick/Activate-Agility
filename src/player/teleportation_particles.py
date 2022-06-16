from functions import clip_set_to_list_on_xaxis
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


class TeleportationParticles:
    def __init__(self):
        # Spriteset
        spriteset = pygame.image.load(
            f"{resources_path}/teleportation_particles.png")

        # Seperate Particle Spriteset
        seperated_spriteset = clip_set_to_list_on_xaxis(spriteset)

        # Images
        self.images = {
            "disapparition": seperated_spriteset,
            "apparition": [
                seperated_spriteset[idx] 
                    for idx in player_data["apparition_index_order"]
                ]
        }

    def draw(self, display):
        pass
