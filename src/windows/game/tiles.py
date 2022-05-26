from functions import clip_set_to_list_on_xaxis
import pygame
import random
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", 
        "resources", "windows", "windows"
        )
    )


class Tiles:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init()

    def init(self):
        self.init_images()
        self.init_speicaltiles()
        self.init_tiles()
        self.init_winlossstates()

    def init_images(self):
        spriteset = pygame.image.load(
            f"{resources_path}/tiles.png")
        self.images = clip_set_to_list_on_xaxis(spriteset)

    def init_speicaltiles(self):
        self.specialtile_color = random.randint(0, 5)
        self.specialtile_position = self.get_speicaltiles_position()
        self.speicaltile_rects = []

    def init_tiles(self):
        color_counter = {i:0 for i in range(7) if i != self.specialtile_color}
        blacklisted_colors_all = [self.specialtile_color]  # a blacklist applied to all tiles
        
        self.tiles = []
        for x in range(36):
            self.tiles.append([])  # add new row
            for y in range(17):
                # Get Rectangle
                rect = self.get_tile_rect(x, y)

                # Image
                if (x, y) in self.specialtile_position:  # special tile
                    color = self.specialtile_color
                    image = self.images[self.specialtile_color]
                    self.speicaltile_rects.append(rect)
                else:  # normal tile
                    # (current only) Blacklist Neighboring Tiles
                    blacklisted_colors_current = []
                    self.blacklist_neighboring_tiles(
                        blacklisted_colors_current, x, y)

                    # Get Blacklist
                    blacklist = self.get_full_blacklist(
                        blacklisted_colors_all, blacklisted_colors_current)

                    # Get Choices
                    choices = self.get_choices(blacklist)

                    # Append Images
                    color = random.choice(choices)
                    image = self.images[color]

                    # Update Color Counter
                    color_counter[color] += 1

                    # (all) Blacklist Overpopulated Color
                    self.blacklist_overpopulated_color(
                        blacklisted_colors_all, color_counter)

                # Append
                tile = (color, image, rect)
                self.tiles[x].append(tile)

    def init_winlossstates(self):
        self.coordinates = [
            (x, y) 
            for x in range(0, 36) 
                for y in range(0, 17) 
                    if (x, y) not in self.specialtile_position]

        self.winstate_ing = False
        self.dissipated = False

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        for row in self.tiles:
            for (_, image, pos) in row:
                display.blit(image, pos)

    # Update ------------------------------------------------------ #
    # Win State
    def update_tiles_to_winstate(self):
        # Turn All Tiles to Special Color
        for x, row in enumerate(self.tiles):
            for y, (_, _, pos) in enumerate(row):
                image = self.images[self.specialtile_color]
                self.tiles[x][y] = (self.specialtile_color, image, pos)

        # Update Special Tile to Black
        color = 6
        for (x, y) in self.specialtile_position:
            # Get Position
            _, _, position = self.tiles[x][y]
            
            # Get Image
            image = self.images[color]

            # Append
            self.tiles[x][y] = (color, image, position)

    # Lost Dissipation
    def update_tiles_to_lossdissipation(self):
        if not self.dissipated:
            # Dissipate Tiles 12 at a Time
            for _ in range(12):
                # Get Random Tile Coordinates
                (x, y) = random.choice(self.coordinates)

                # Get Position
                _, _, position = self.tiles[x][y]

                # Get Images
                image = self.images[self.specialtile_color]

                # Append
                self.tiles[x][y] = (self.specialtile_color, image, position)

                # Remove Tile Coordinates from List
                self.coordinates.remove((x, y))

                # Stop if Coordinates List is Empty
                if len(self.coordinates) <= 0:
                    self.dissipated = True
                    break

    # Functions --------------------------------------------------- #
    # Initialize Special Tiles
    def get_speicaltiles_position(self):
        special_tiles = []
        x_blacklist = []
        y_blacklist = []
        for _ in range(3):
            # Position Choices
            x_choices = [num for num in range(36) if num not in x_blacklist]
            y_choices = [num for num in range(17) if num not in y_blacklist]

            # Get Position
            tile_position = (
                random.choice(x_choices), 
                random.choice(y_choices))

            # Append
            special_tiles.append(tile_position)

        return special_tiles

    # Initialize Tiles
    def blacklist_neighboring_tiles(self, blacklisted_colors, x, y):
        # Get Number of Neighboring Coordinates to be Blacklisted (4-8)
        limit = random.randint(4, 8)

        # Get 4-8 Neighboring Coordinates (according to the variable: limit) to Be Blacklisted
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

    def get_choices(self, blacklist):
        # Remove a Random Number in Blacklist
        if len(blacklist) >= 7:
            color = random.choice(
                [i for i in range(7) if i != self.specialtile_color])
            blacklist.pop(blacklist.index(color))

        # Get Choices but Exclude the Blacklisted Colors
        choices = [i for i in range(7) if i not in blacklist]

        # Return Choices
        return choices

    def blacklist_overpopulated_color(self, blacklisted_colors, color_counter):
        for (color, length) in color_counter.items():
            if length >= 102 and color not in blacklisted_colors:
                blacklisted_colors.append(color)

    def get_tile_rect(self, x, y):
        offset = (32, 60)
        rect = pygame.Rect(
            offset[0] + x*16, offset[1] + y*16,
            16, 16)
        
        return rect
