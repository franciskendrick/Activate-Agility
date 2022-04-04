from functions import separate_sets_from_yaxis, clip_set_to_list_on_xaxis
import pygame
import random
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class Tiles:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_tiles()

    def init_images(self):
        # Spriteset
        spriteset = pygame.image.load(
            f"{path}/assets/tiles.png")

        # Images
        sets = separate_sets_from_yaxis(spriteset, (255, 0, 0))
        self.images = {
            "on": clip_set_to_list_on_xaxis(sets[0]),
            "off": clip_set_to_list_on_xaxis(sets[1])
        }

    def init_tiles(self):
        offset = (32, 60)
        self.tiles = []
        for x in range(36):
            for y in range(17):
                # Image
                toggle = random.choices(["on", "off"], weights=(75, 25))[0]
                if toggle == "on":
                    color = random.randint(0, 5)
                    image = self.images[toggle][color]
                else:
                    image = self.images[toggle]

                # Position
                xpos = offset[0] + x*16
                ypos = offset[1] + y*16

                # Append
                tile = (image, (xpos, ypos))
                self.tiles.append(tile)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        for (image, pos) in self.tiles:
            display.blit(image, pos)


tiles = Tiles()
