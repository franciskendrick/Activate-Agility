from functions import separate_sets_from_yaxis, clip_set_to_list_on_xaxis
import pygame
import json
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

# Json
with open(f"{path}/data/game.json") as json_file:
    game_data = json.load(json_file)


class PlayerGauge:
    # Initialize -------------------------------------------------- #
    def __init__(self, maximum_status):
        self.init_images(maximum_status)
        self.init_positions()

    def init_images(self, maximum_status):
        spriteset = pygame.image.load(
            f"{path}/assets/player_gauge.png")
        order = ["bar", "icon", "on_gauge", "off_gauge"]

        # Images
        self.images = {}
        separated_sets = separate_sets_from_yaxis(spriteset, (255, 0, 0))
        for name, separated_set in zip(order, separated_sets):
            image = clip_set_to_list_on_xaxis(separated_set)
            self.images[name] = image

        # Gauge
        self.gauge_images(maximum_status)

    def init_positions(self):
        self.positions = game_data["playergauge_position"]

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        keys = ["health", "mana", "stamina"]
        for idx, key in enumerate(keys):
            # Icon
            icon = self.images["icon"][idx]
            display.blit(icon, self.positions["icon"][key])

            # Bar
            bar = self.images["bar"]
            display.blit(bar, self.positions["bar"][key])

            # Gauge

    # Update ------------------------------------------------------ #
    def update(self):
        pass

    # Functions --------------------------------------------------- #
    def gauge_images(self, maximum_status):
        # Gauge Images
        gauge_images = {}

        order = ["health", "mana", "stamina"]
        for name in order:
            images = []
            for _ in range(maximum_status[name]):
                gauge = [
                    True,  # toggle
                    self.images["on_gauge"],  # on image 
                    self.images["off_gauge"]]  # off image
                images.append(gauge)
            gauge_images[name] = images

        # Remove Old Gauge Images
        self.images.pop("on_gauge")
        self.images.pop("off_gauge")

        # Append New Gauge Images
        self.images["gauge"] = gauge_images
