from .number_font import NumberFont
import pygame
import json
import time
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

# Json
with open(f"{path}/data/game.json") as json_file:
    game_data = json.load(json_file)


class Countdown(NumberFont):
    # Initialize -------------------------------------------------- #
    def __init__(self):
        super().__init__()

        # Game
        self.start_of_game = None

        # Images
        self.init_title()
        self.init_numbers()

        # Time Remaining
        self.init_time()

    def init_title(self):
        # Spriteset
        title_image = pygame.image.load(
            f"{path}/assets/countdown.png")

        # Initialize
        wd, ht = title_image.get_rect().size
        resized_image = pygame.transform.scale(
            title_image, (wd * 2, ht * 2))
        rect = pygame.Rect(
            game_data["countdown_position"]["title"], 
            resized_image.get_rect().size)

        # Append
        self.title = [resized_image, rect]

    def init_numbers(self):
        self.number_positions = {}
        numbers = [i for i in range(3, -1, -1)]
        for num in numbers:
            pos = game_data["countdown_position"]["numbers"][str(num)]
            self.number_positions[num] = pos
        
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
            text = list(str(self.time_remaining))
            pos = self.number_positions[self.time_remaining]
            self.render_font(display, text, pos, 5)

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
