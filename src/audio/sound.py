import pygame
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", 
        "resources", "audio"
        )
    )


class Sound:
    # Initialize -------------------------------------------------- #
    def __init__(self, options_toggleable_btns):
        self.button_click_sound = pygame.mixer.Sound(
            f"{resources_path}/ES_Switch Click 5 - SFX Producer.mp3")

        self.pause_sound = pygame.mixer.Sound(
            f"{resources_path}/envatoelements_Pause.mp3")
        self.gameover_sound = pygame.mixer.Sound(
            f"{resources_path}/envatoelements_Game Over.mp3")
        
        self.lost_sound = pygame.mixer.Sound(
            f"{resources_path}/mixkit_Lost Life.mp3")
        self.win_sound = pygame.mixer.Sound(
            f"{resources_path}/mixkit_Win.mp3")

        self.abilityready_sound = pygame.mixer.Sound(
            f"{resources_path}/mixkit_Ability Ready.mp3")

        self.disapparition_sound = pygame.mixer.Sound(
            f"{resources_path}/youtube_Disapparition.mp3")
        self.apparition_sound = pygame.mixer.Sound(
            f"{resources_path}/youtube_Apparition.mp3")

        self.playing = options_toggleable_btns["sound"][1]

    # Play -------------------------------------------------------- #
    def play_button_click(self):
        if self.playing:
            self.button_click_sound.play()

    def play_pause(self):
        if self.playing:
            self.pause_sound.play()

    def play_gameover(self):
        if self.playing:
            self.gameover_sound.play()

    def play_lost(self):
        if self.playing:
            self.lost_sound.play()

    def play_win(self):
        if self.playing:
            self.win_sound.play()

    def play_abilityready(self):
        if self.playing:
            self.abilityready_sound.play()

    def play_disapparition(self):
        if self.playing:
            self.disapparition_sound.play()

    def play_apparition(self):
        if self.playing:
            self.apparition_sound.play()

    # Update ------------------------------------------------------ #
    def update(self, options_toggleable_btns):
        self.playing = options_toggleable_btns["sound"][1]
