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
        numbers = [i for i in range(3, -1, -1)]
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
        # Time Remaining
        self.time_remaining = 3

        # Time Countdown
        self.last_count = time.perf_counter()

        # Time Visibility
        self.time_is_visible = False
        self.visible_delay = 1000  # milliseconds

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Title
        display.blit(*self.title)

        # Numbers
        if self.time_is_visible:
            display.blit(*self.numbers[self.time_remaining])

    # Update ------------------------------------------------------ #
    def update(self, start_of_game):
        self.update_visibility(start_of_game)
        self.update_timeremaining(start_of_game)

    def update_visibility(self, start_of_game):
        dt = time.perf_counter() - start_of_game
        if not self.time_is_visible and dt * 1000 >= self.visible_delay:
            self.time_is_visible = True

    def update_timeremaining(self, start_of_game):
        # Delta Time
        count_dt = time.perf_counter() - self.last_count
        game_dt = time.perf_counter() - start_of_game

        # Visibility Delay
        visibility_delay = game_dt * 1000 >= self.visible_delay+1000

        # Time Remaining is More than Zero
        time_morethan_zero = self.time_remaining > 0

        # Time Countdown
        time_countdown = count_dt * 1000 >= 1000

        # Update 
        if visibility_delay and time_morethan_zero and time_countdown:
            # Update Time Value
            self.time_remaining -= 1

            # Update Last Count
            self.last_count = time.perf_counter()
