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
        self.init_speicaltiles()
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

    def init_speicaltiles(self):
        self.specialtiles_color = random.randint(0, 5)
        self.specialtiles_position = self.get_speicaltiles_position()

    def init_tiles(self):
        offset = (32, 60)
        self.tiles = []
        for x in range(36):
            for y in range(17):
                # Image
                if (x, y) in self.specialtiles_position:  # special tile
                    image = self.images["on"][self.specialtiles_color]
                else:  # normal tile
                    # toggle = random.choices(["on", "off"], weights=(75, 25))[0]
                    toggle = "off"  # !!!
                    if toggle == "on":
                        color = random.randint(
                            [i for i in range(5) if not self.specialtiles_color])
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

    # Functions --------------------------------------------------- #
    def get_speicaltiles_position(self):
        special_tiles = []
        xs = []
        ys = []
        for _ in range(3):
            x_choices = [num for num in range(36) if num not in xs]
            y_choices = [num for num in range(17) if num not in ys]
            tile_position = (
                random.choice(x_choices), 
                random.choice(y_choices))

            special_tiles.append(tile_position)

        return special_tiles


tiles = Tiles()
