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
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_animationvariables()

    def init_images(self):
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

    def init_positions(self, from_position, destination_position):
        self.positions = {
            "disapparation": from_position,
            "apparition": destination_position
        }

    def init_animationvariables(self):
        # Disapparition
        self.disapparition_idx = 0
        self.has_disapparated = False
        self.disapparation_flimit = 3

        # Apparition
        self.apparated_idx = 0
        self.has_apparated = False
        self.apparated_flimit = 3

    # Draw -------------------------------------------------------- #
    def draw_dispparition(self, display, direction):
        if not self.has_disapparated:
            images = self.images[direction]

            # Cancel Update
            if self.disapparition_idx >= self.disapparation_flimit * 3:
                self.disapparition_idx = (self.disapparation_flimit - 1) * 3
                self.has_disapparated = True
            
            # Draw
            img = images[self.disapparition_idx // 3]
            position = self.positions["disapparation"]
            display.blit(img, position)

            # Update
            self.disapparition_idx += 1
