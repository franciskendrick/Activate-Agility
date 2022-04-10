from functions import clip_set_to_list_on_xaxis
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
        spriteset = pygame.image.load(
            f"{path}/assets/tiles.png")
        self.images = clip_set_to_list_on_xaxis(spriteset)

    def init_speicaltiles(self):
        self.specialtiles_color = random.randint(0, 5)
        self.specialtiles_position = self.get_speicaltiles_position()

    def init_tiles(self):
        color_counter = {i:0 for i in range(7) if i != self.specialtiles_color}
        blacklisted_colors_all = [self.specialtiles_color]  # a blacklist applied to all tiles
        
        self.tiles = []
        for x in range(36):
            self.tiles.append([])  # add new row
            for y in range(17):
                # Image
                if (x, y) in self.specialtiles_position:  # special tile
                    image = self.images[self.specialtiles_color]
                else:  # normal tile
                    # (current only) Blacklist Neighboring Tiles
                    blacklisted_colors_current = []
                    self.blacklist_neighboring_tiles(
                        blacklisted_colors_current, x, y)

                    # Get Blacklist
                    blacklist = self.get_full_blacklist(
                        blacklisted_colors_all, blacklisted_colors_current)

                    # Get Choices
                    choices = self.get_choices(
                        blacklist, blacklisted_colors_current)

                    # Append Images
                    color = random.choice(choices)
                    image = self.images[color]

                    # Update Color Counter
                    color_counter[color] += 1

                    # (all) Blacklist Overpopulated Color
                    self.blacklist_overpopulated_color(
                        blacklisted_colors_all, color_counter)

                # Get Position
                position = self.get_tile_position(x, y)

                # Append
                tile = (color, image, position)
                self.tiles[x].append(tile)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        for row in self.tiles:
            for (_, image, pos) in row:
                display.blit(image, pos)

    # Functions --------------------------------------------------- #
    # Initialize Special Tiles
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

    # Initialize Tiles
    def blacklist_neighboring_tiles(self, blacklisted_colors, x, y):
        # Get Number of Neighboring Coordinates to be Blacklisted (6-8)
        limit = random.randint(6, 8)

        # Get 6-8 Neighboring Coordinates (according to the variable: limit) to Be Blacklisted
        blacklisting_coordinates = [
            (x+1, y),  # right
            (x-1, y),  # left
            (x, y+1),  # bottom
            (x, y-1),  # top
            (x+1, y-1),  # top right
            (x-1, y-1),  # top left
            (x+1, y+1),  # bottom right
            (x-1, y+1)  # bottom left
        ]
        if limit < 8:
            blacklisting_coordinates.pop(random.randint(0, limit))

        # Blacklist Tiles in Blaclisting Coordinates List
        for (x, y) in blacklisting_coordinates:
            try:
                blacklisted_colors.append(self.tiles[x][y][0])
            except IndexError:
                pass

    def get_full_blacklist(self, blacklist_all, blacklist_current):
        blacklist = blacklist_all + blacklist_current
        blacklist = list(dict.fromkeys(blacklist))

        return blacklist

    def get_choices(self, blacklist, blacklist_current):
        if len(blacklist) >= 7:
            choices = [
                i for i in range(7) 
                    if i != self.specialtiles_color
                    and i not in blacklist_current]
        else:
            choices = [i for i in range(7) if i not in blacklist]

        return choices

    def blacklist_overpopulated_color(self, blacklisted_colors, color_counter):
        for (color, length) in color_counter.items():
            if length >= 102 and color not in blacklisted_colors:
                blacklisted_colors.append(color)

    def get_tile_position(self, x, y):
        offset = (32, 60)
        return (offset[0] + x*16, offset[1] + y*16)


tiles = Tiles()
