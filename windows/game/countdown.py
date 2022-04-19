from functions import separate_sets_from_yaxis, clip_set_to_list_on_xaxis
import pygame
import json
import time
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

# Json
with open(f"{path}/data/game.json") as json_file:
    game_data = json.load(json_file)


class Countdown:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        # Game
        self.start_of_game = None

        # Spriteset
        spriteset = pygame.image.load(
            f"{path}/assets/countdown.png")
        title_set, numbers_set = separate_sets_from_yaxis(
            spriteset, (255, 0, 0))

        # Images
        self.init_title(title_set)
        self.init_numbers(numbers_set)

        # Time Remaining
        self.init_time()

    def init_title(self, set):
        # Initialize
        image = clip_set_to_list_on_xaxis(set)
        rect = pygame.Rect(
            game_data["countdown_position"]["title"], 
            image.get_rect().size)

        # Append
        self.title = [image, rect]

    def init_numbers(self, set):
        self.numbers = {}
        images = clip_set_to_list_on_xaxis(set)
        numbers = [i for i in range(5, -1, -1)]
        for num, image in zip(numbers, images):
            # Get Image Size
            wd, ht = image.get_rect().size

            # Initialize
            resized_image = pygame.transform.scale(
                image, (wd * 6, ht * 6))
            rect = pygame.Rect(
                game_data["countdown_position"]["numbers"][str(num)],
                image.get_rect().size)

            # Append
            self.numbers[num] = [resized_image, rect]

    def init_time(self):
        self.time_remaining = 5
        self.time_visible = False
        self.last_count = time.perf_counter()

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Title
        display.blit(*self.title)

        # Numbers
        if self.time_visible:
            display.blit(*self.numbers[self.time_remaining])

    # Update ------------------------------------------------------ #
    def update(self):
        self.update_timevisibility()
        self.update_timeremaining()

    def update_timevisibility(self):
        dt = time.perf_counter() - self.start_of_game
        if not self.time_visible and dt * 1000 >= 2000:
            self.time_visible = True

    def update_timeremaining(self):
        count_dt = time.perf_counter() - self.last_count
        game_dt = time.perf_counter() - self.start_of_game
        # one second cooldown that starts one second after time is visible and stops if time hits zero
        if game_dt * 1000 >= 3000 and self.time_remaining > 0 and count_dt * 1000 >= 1000:
            self.time_remaining -= 1
            self.last_count = time.perf_counter()
