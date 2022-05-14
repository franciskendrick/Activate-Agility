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
        self.init_scores(score, highscore)
        self.init_endtime(endtime)

    def init_board(self):
        img = pygame.image.load(
            f"{resources_path}/status.png")
        rect = pygame.Rect(
            gameover_data["status_positions"]["board"],
            img.get_rect().size)

        self.status_board = [img, rect]

    def init_scores(self, score, highscore):
        # Score
        self.score = {
            "text": f"{score:,}",
            "pos": gameover_data["status_positions"]["score"]
        }

        # Highscore
        self.high_score = {
            "text": f"{highscore:,}",
            "pos": gameover_data["status_positions"]["highscore"]
        }

    def init_endtime(self, endtime):
        # Convert Endtime to Floating-point
        endtime = float(endtime)

        # Divide EndTime to Minutes and Seconds
        _min, _sec = divmod(endtime, 60)

        # Get Seconds and Milliseconds
        rounded_sec = str(round(_sec, 2))
        sec, ms = rounded_sec.split(".")

        # Get Hour and Minutes
        hour, min = divmod(_min, 60)

        # Convert Time into Integer and then into a String
        hour = str(int(hour))
        min = str(int(min))
        sec = str(int(sec))
        ms = str(int(ms))

        # Pad Time with Zeros on the Left
        hour = hour.zfill(2)
        min = min.zfill(2)
        sec = sec.zfill(2)
        ms = ms.zfill(2)

        # EndTime Text
        endtime_text = f"{hour}:{min}:{sec}:{ms}"

        # Endtime
        self.end_time = {
            "text": endtime_text,
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
