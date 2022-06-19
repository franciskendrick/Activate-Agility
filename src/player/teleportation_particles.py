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
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_animationvariables()

    def init_images(self):
        # Spriteset
        spriteset = pygame.image.load(
            f"{resources_path}/teleportation_particles.png")

        # Separate Particle Spriteset
        separated_spriteset = clip_set_to_list_on_xaxis(spriteset)

        # Images
        self.images = {
            "disapparition": separated_spriteset,
            "apparition": [
                separated_spriteset[idx] 
                    for idx in player_data["apparition_index_order"]
                ]
        }

    def init_positions(self, from_position, destination_position):
        offset = player_data["teleportationparticles_offset"]
        self.positions = {
            "disapparation": (
                from_position[0] - offset[0],
                from_position[1] - offset[1]),
            "apparition": (
                destination_position[0] - offset[0],
                destination_position[1] - offset[1])
        }

    def init_animationvariables(self):
        # Disapparition
        self.disapparition_idx = 0
        self.has_disapparated = False
        self.disapparation_flimit = 8

        # Apparition
        self.apparated_idx = 0
        self.has_apparated = False
        self.apparated_flimit = 6

    # Draw -------------------------------------------------------- #
    def draw_disapparition(self, display):
        if not self.has_disapparated:
            images = self.images["disapparition"]
        
            # Cancel Updates
            if self.disapparition_idx >= self.disapparation_flimit * 3:
                self.disapparition_idx = (self.disapparation_flimit - 1) * 3
                self.has_disapparated = True

            # Draw
            img = images[self.disapparition_idx // 3]
            position = self.positions["disapparation"]
            display.blit(img, position)

            # Update
            self.disapparition_idx += 1

    def draw_apparition(self, display):
        if not self.has_apparated and self.disapparition_idx >= 7 * 3:
            images = self.images["apparition"]

            # Cancel Update
            if self.apparated_idx >= self.apparated_flimit * 3:
                self.apparated_idx = (self.apparated_flimit - 1) * 3
                self.has_apparated = True
            
            # Draw
            img = images[self.apparated_idx // 3]
            position = self.positions["apparition"]
            display.blit(img, position)

            # Update
            self.apparated_idx += 1
