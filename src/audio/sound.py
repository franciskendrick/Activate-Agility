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
    def __init__(self):
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

    # Play -------------------------------------------------------- #
    def play_pause(self):
        self.pause_sound.play()

    def play_gameover(self):
        self.gameover_sound.play()

    def play_lost(self):
        self.lost_sound.play()

    def play_win(self):
        self.win_sound.play()

    def play_abilityready(self):
        self.abilityready_sound.play()

    def play_disapparition(self):
        self.disapparition_sound.play()

    def play_apparition(self):
        self.apparition_sound.play()

    # Update ------------------------------------------------------ #
    def update(self):
        pass
