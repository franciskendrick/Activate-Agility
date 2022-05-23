import pygame
import json
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", 
        "resources", "windows", "paused"
        )
    )

# Json
with open(f"{resources_path}/paused.json") as json_file:
    paused_data = json.load(json_file)


class Status:
    # Initialize -------------------------------------------------- #
    def __init__(self, score, highscore):
        self.init_board()
        self.init_scores(score, highscore)

    def init_board(self):
        img = pygame.image.load(
            f"{resources_path}/status_bkg.png")
        rect = pygame.Rect(
            paused_data["status_positions"]["board"],
            img.get_rect().size)

        self.status_board = [img, rect]

    def init_scores(self, score, highscore):
        # Score
        self.score = {
            "text": f"{score:,}",
            "pos": paused_data["status_positions"]["score"]
        }

        # Highscore
        self.high_score = {
            "text": f"{highscore:,}",
            "pos": paused_data["status_positions"]["highscore"]
        }

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Board
        display.blit(*self.status_board)
