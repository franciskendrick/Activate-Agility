from functions import separate_sets_from_yaxis, clip_set_to_list_on_xaxis
import pygame
import json
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", 
        "resources", "windows", "game"
        )
    )

# Json
with open(f"{resources_path}/game.json") as json_file:
    game_data = json.load(json_file)


class PlayerGauge:
    # Initialize -------------------------------------------------- #
    def __init__(self, maximum_status):
        self.init_images(maximum_status)
        self.init_positions()

    def init_images(self, maximum_status):
        spriteset = pygame.image.load(
            f"{resources_path}/player_gauge.png")
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
            x, y = self.positions["gauge"][key]
            gauge_images = self.images["gauge"][key]
            for (toggle, img_on, img_off) in gauge_images:
                img = img_on if toggle else img_off
                display.blit(img, (x, y))
                x += game_data["playergauge_position"]["spacing"][key]

    # Update ------------------------------------------------------ #
    def update(self, player_status):
        status_items = list(player_status.items())
        for (key, stat) in status_items:
            gauge_images = self.images["gauge"][key]
            for idx, data in enumerate(gauge_images):
                data[0] = True if stat > idx else False

    # Functions --------------------------------------------------- #
    def gauge_images(self, maximum_status):
        # Gauge Images
        gauge_images = {}

        order = ["health", "mana", "stamina"]
        for idx, name in enumerate(order):
            images = []
            for _ in range(maximum_status[name]):
                gauge = [
                    True,  # toggle
                    self.images["on_gauge"][idx],  # on image 
                    self.images["off_gauge"][idx]]  # off image
                images.append(gauge)
            gauge_images[name] = images

        # Remove Old Gauge Images
        self.images.pop("on_gauge")
        self.images.pop("off_gauge")

        # Append New Gauge Images
        self.images["gauge"] = gauge_images
