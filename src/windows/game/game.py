from windows.windows import window
from .tiles import Tiles
from .player_gauge import PlayerGauge
from .special_color_identifier import SpecialColorIdentifier
from .countdown import Countdown
from .score import Score
from .high_score import HighScore
import pygame

pygame.init()


class Game:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.display = pygame.Surface(
            window.rect.size, pygame.SRCALPHA)
        self.display.convert_alpha()
        self.rect = pygame.Rect(
            (0, 0), self.display.get_size())

    def init_objects(self, maximum_stats):
        # Initialize Game Objects
        self.tiles = Tiles()
        self.speical_color_identifier = SpecialColorIdentifier(
            self.tiles.specialtile_color)
        self.player_gauge = PlayerGauge(maximum_stats)
        self.countdown = Countdown()
        self.score = Score()
    
        # Initialize Sound Variables
        self.lostsound_played = False
        self.winsound_played = False
        self.abilityready_played = False

    def init_highscore(self):
        self.highscore = HighScore()
    
    def init_startofgame(self, start_of_game):
        self.countdown.init_startofgame(start_of_game)
        self.speical_color_identifier.init_startofgame(start_of_game)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Fill Game Display with Transparent Background
        self.display.fill((0, 0, 0, 0))

        # Draw Game Window on Game Display
        self.tiles.draw(self.display)
        self.speical_color_identifier.draw(self.display)
        self.player_gauge.draw(self.display)
        self.countdown.draw(self.display)
        self.score.draw(self.display)
        self.highscore.draw(self.display)

        # Blit Game Display to Original Display
        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)

    # Update ------------------------------------------------------ #
    def update(self, player_status, countdown_audio, speicalcolor_audio_identifier):
        self.player_gauge.update(player_status)
        self.speical_color_identifier.update(speicalcolor_audio_identifier)
        self.countdown.update(countdown_audio)

    # Functions --------------------------------------------------- #
    def reset_objects(self):
        self.tiles.init()
        self.speical_color_identifier.init(
            self.tiles.specialtile_color)
        self.countdown.init()

    def reset_gamestate_soundvars(self):
        self.lostsound_played = False
        self.winsound_played = False

    def reset_abilityready_soundvars(self, player):
        if player.stats["mana"] < player.maximum_stats["mana"]:
            self.abilityready_played = False
