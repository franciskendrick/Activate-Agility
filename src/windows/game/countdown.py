from fonts import NumberFont
import pygame
import json
import time
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", 
        "resources", "windows", "game"
        )
    )

# Json
with open(f"{resources_path}/game.json") as json_file:
    game_data = json.load(json_file)


class Countdown(NumberFont):
    # Initialize -------------------------------------------------- #
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        # Images
        self.init_title()
        self.init_numbers()

        # Time Remaining
        self.init_time()

    def init_title(self):
        # Spriteset
        title_image = pygame.image.load(
            f"{resources_path}/countdown.png")

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

    def init_startofgame(self, start_of_game):
        self.start_of_game = start_of_game

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Title
        display.blit(*self.title)

        # Numbers
        if self.time_is_visible:
            text = str(self.time_remaining)
            pos = self.number_positions[self.time_remaining]
            self.render_font(display, text, pos, 5)

    # Update ------------------------------------------------------ #
    def update(self, sound):
        self.update_visibility()
        self.update_timeremaining(sound)

    def update_visibility(self):
        dt = time.perf_counter() - self.start_of_game
        if not self.time_is_visible and dt * 1000 >= self.visible_delay:
            self.time_is_visible = True

    def update_timeremaining(self, sound):
        # Delta Time
        count_dt = time.perf_counter() - self.last_count
        game_dt = time.perf_counter() - self.start_of_game

        # Play Countdown Audio
        if (game_dt * 1000 >= self.visible_delay and
                self.time_remaining > 0 and
                not sound.audio_played[self.time_remaining]):
            play_audio = sound.audioplaying_switchcase[self.time_remaining]
            play_audio()

            sound.audio_played[self.time_remaining] = True

        # Update 
        if (game_dt * 1000 >= self.visible_delay + 1000 and
                self.time_remaining > 0 and 
                count_dt * 1000 >= 1000):
            # Update Time Value
            self.time_remaining -= 1

            # Update Last Count
            self.last_count = time.perf_counter()

    # Functions --------------------------------------------------- #
    def restart_countdown_time(self):
        self.last_count = time.perf_counter()
