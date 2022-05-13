from fonts import NumberFont
import pygame
import json
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", 
        "resources", "windows", "gameover"
        )
    )

# Json
with open(f"{resources_path}/gameover.json") as json_file:
    gameover_data = json.load(json_file)


class Status(NumberFont):
    # Initialize
    def __init__(self, score, highscore, endtime):
        super().__init__()

        self.init_board()
        self.init_stats(score, highscore, endtime)

    def init_board(self):
        img = pygame.image.load(
            f"{resources_path}/status.png")
        rect = pygame.Rect(
            gameover_data["status_positions"]["board"],
            img.get_rect().size)

        self.status_board = [img, rect]

    def init_stats(self, score, highscore, endtime):
        self.score = {
            "text": f"{score:,}",
            "pos": gameover_data["status_positions"]["score"]
        }
        self.high_score = {
            "text": f"{highscore:,}",
            "pos": gameover_data["status_positions"]["highscore"]
        }
        self.end_time = {
            "text": f"{endtime}",
            "pos": gameover_data["status_positions"]["endtime"]
        }

    # Draw
    def draw(self, display):
        # Board
        display.blit(*self.status_board)
        
        # Score
        self.render_font(
            display, 
            self.score["text"], self.score["pos"],
            enlarge=1, color=(70, 130, 50))

        # Highscore
        self.render_font(
            display, 
            self.high_score["text"], self.high_score["pos"],
            enlarge=1, color=(70, 130, 50))

        # End Time
        self.render_font(
            display,
            self.end_time["text"], self.end_time["pos"],
            enlarge=1, color=(70, 130, 50))
