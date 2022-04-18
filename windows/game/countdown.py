from functions import separate_sets_from_yaxis, clip_set_to_list_on_xaxis
import pygame
import json
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

# Json
with open(f"{path}/data/game.json") as json_file:
    game_data = json.load(json_file)


class Countdown:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        spriteset = pygame.image.load(
            f"{path}/assets/countdown.png")
        separated_sets = separate_sets_from_yaxis(
            spriteset, (255, 0, 0))

        # Title
        image = clip_set_to_list_on_xaxis(separated_sets[0])
        rect = pygame.Rect(
            game_data["countdown_position"]["title"], 
            image.get_rect().size)
        self.title = [image, rect]

        # Numbers
        self.numbers = {}
        images = clip_set_to_list_on_xaxis(separated_sets[1])
        numbers = [i for i in range(5, -1, -1)]
        for num, image in zip(numbers, images):
            wd, ht = image.get_rect().size

            resized_image = pygame.transform.scale(
                image, (wd * 6, ht * 6))
            rect = pygame.Rect(
                game_data["countdown_position"]["numbers"][str(num)],
                image.get_rect().size)

            self.numbers[num] = [resized_image, rect]

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass


countdown = Countdown()
