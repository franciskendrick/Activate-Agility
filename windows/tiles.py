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
        offset = (32, 60)
        
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
                    try:
                        blacklisted_colors_current.append(self.tiles[x+1][y][0])  # right color
                    except IndexError:
                        pass
            
                    try:
                        blacklisted_colors_current.append(self.tiles[x-1][y][0])  # left color
                    except IndexError:
                        pass

                    try:
                        blacklisted_colors_current.append(self.tiles[x][y+1][0])  # bottom color
                    except IndexError:   
                        pass
                                            
                    try:                        
                        blacklisted_colors_current.append(self.tiles[x][y-1][0])  # top color
                    except IndexError:
                        pass

                    # Get Blacklist
                    blacklist = blacklisted_colors_all + blacklisted_colors_current
                    blacklist = list(dict.fromkeys(blacklist))
                    blacklist.sort()

                    # Get Choices
                    if blacklist == [i for i in range(7)]:
                        choices = [i for i in range(7) if i != self.specialtiles_color]
                    else:
                        choices = [i for i in range(7) if i not in blacklist]

                    # Append Images
                    color = random.choice(choices)
                    image = self.images[color]

                    # Update Color Counter
                    color_counter[color] += 1

                    # (all) Blacklist Overpopulated Color
                    for (blacklist_color, length) in color_counter.items():
                        if length >= 102 and blacklist_color not in blacklisted_colors_all:
                            blacklisted_colors_all.append(blacklist_color)

                # Position
                xpos = offset[0] + x*16
                ypos = offset[1] + y*16

                # Append
                tile = (color, image, (xpos, ypos))
                self.tiles[x].append(tile)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        for row in self.tiles:
            for (_, image, pos) in row:
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
