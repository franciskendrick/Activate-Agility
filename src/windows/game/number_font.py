from functions import clip_font_to_dict
import pygame
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", 
        "resources", "windows", "game"
        )
    )


class NumberFont:
    def __init__(self):
        # Order
        self.order = [
            '0', '1', '2', '3', '4', 
            '5', '6', '7', '8', '9', ','
        ] 

        # Characters
        font_set = pygame.image.load(
            f"{resources_path}/number_font.png")
        self.characters = clip_font_to_dict(
            font_set, self.order)

        # Spacing
        self.character_spacing = 1
        self.space = 3

    def render_font(self, display, text, pos, enlarge=2):
        x, y = pos
        x_offset = 0

        # Loop Over Every Character in Text
        for char in text:
            if char != " ":  # character
                # Get Character Image
                character = self.characters[char]

                # Resize Character Image
                wd, ht = character.get_size()
                resized_character = pygame.transform.scale(
                    character, (wd * enlarge, ht * enlarge))

                # Blit to Screen
                display.blit(resized_character, (x + x_offset, y))

                # Add to Offset Width of Resized Character + Spacing
                x_offset += resized_character.get_width() + self.character_spacing
            else:  # space
                # Add to Offset Space Width + Spacing
                x_offset += self.space + self.character_spacing

    def get_font_rect(self, text, pos, enlarge=2):
        wd = 0
        heights = []

        # Loop Over Every Character in Text
        for char in text:
            if char != " ":  # characters
                # Get Character Image
                character = self.characters[char]

                # Add to Offset Width of Character + Spacing
                wd += character.get_width() + self.character_spacing

                # Append Character's Height 
                heights.append(character.get_height())
            else:  # space
                # Add to Width Space Width + Spacing
                wd += self.space + self.character_spacing

        # Get Rectangle and Return
        return pygame.Rect(*pos, wd * enlarge, max(heights) * enlarge)
