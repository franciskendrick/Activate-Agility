from player import Player
from windows import gameover
from windows.windows import window, background
from windows.game import Tiles, PlayerGauge, SpecialColorVisualIdentifier, Countdown, Score, HighScore
from windows.menu import Menu
from windows.gameover import GameOver
from windows.paused import Paused
import pygame
import time
import sys


# Functions ------------------------------------------------------- #
def placeholder():  # !!!
    pass


def init_game():
    global player
    global tiles, speicalcolor_visual_identifier
    global countdown, player_gauge, score, high_score
    global start_of_game, start_of_gamesession, end_of_game

    # Initialize Player
    player = Player()

    # Initialize Game Variables
    tiles = Tiles()
    speicalcolor_visual_identifier = SpecialColorVisualIdentifier(
        tiles.specialtile_color)
    countdown = Countdown()
    player_gauge = PlayerGauge(player.maximum_stats)
    score = Score()
    high_score = HighScore()

    # Time 
    start_of_game = time.perf_counter()
    start_of_gamesession = start_of_game
    end_of_game = None


def restart_game():
    global player
    global start_of_game, end_of_game

    # Reset Game Variables
    tiles.init()
    speicalcolor_visual_identifier.init(tiles.specialtile_color)
    countdown.init()

    # Player
    player.on_specialtile = False

    # Time
    start_of_game = time.perf_counter()
    end_of_game = None


# Redraws --------------------------------------------------------- #
def redraw_game():
    # Background
    display.fill(background.color)
    background.draw_walls(display)
    tiles.draw(display)

    # Windows.Game
    player_gauge.draw(display)
    speicalcolor_visual_identifier.draw(display)
    countdown.draw(display)
    score.draw(display)
    high_score.draw(display)

    # Player
    player.draw(display)

    # Blit to Screen ---------------------------------------------- #
    resized_display = pygame.transform.scale(display, win_size)
    win.blit(resized_display, (0, 0))

    pygame.display.update()


def redraw_menu():
    # Background
    display.fill(background.color)
    background.draw_walls(display)

    # Menu
    menu.draw(display)

    # Blit to Screen ---------------------------------------------- #
    resized_display = pygame.transform.scale(display, win_size)
    win.blit(resized_display, (0, 0))

    pygame.display.update()


def redraw_gameover():
    # Background
    display.fill(background.color)
    background.draw_walls(display)

    # GameOver
    gameover.draw(display)

    # Blit to Screen ---------------------------------------------- #
    resized_display = pygame.transform.scale(display, win_size)
    win.blit(resized_display, (0, 0))

    pygame.display.update()


def redraw_paused():
    # Background
    display.fill(background.color)
    background.draw_walls(display)

    # GameOver
    paused.draw(display)

    # Blit to Screen ---------------------------------------------- #
    resized_display = pygame.transform.scale(display, win_size)
    win.blit(resized_display, (0, 0))

    pygame.display.update()


# Loops ----------------------------------------------------------- #
def game_loop():
    global end_of_game

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # Pause
                if event.key == pygame.K_ESCAPE:
                    paused_loop()

        # Player
        player.update(
            tiles.speicaltile_rects,
            countdown.time_remaining)

        # Windows.Game
        player_gauge.update(player.stats)
        speicalcolor_visual_identifier.update(start_of_game)
        countdown.update(start_of_game)

        # Countdown is Over
        if countdown.time_remaining == 0:
            # Win of Loss
            if player.on_specialtile:  # win
                # Update Tiles' State
                tiles.update_tiles_to_winstate()

                if end_of_game == None:
                    # Update End of Game Time
                    end_of_game = time.perf_counter()

                    # Update Player Mana Stat
                    if player.stats["mana"] < player.maximum_stats["mana"]:
                        player.stats["mana"] += 1

                    # Add to Score
                    score.value += 1

                    # Add to Highscore
                    if score.value > high_score.value:
                        high_score.value = score.value
            else:  # loss
                # Update Tiles' State
                tiles.update_tiles_to_lossdissipation()

                if tiles.dissipated and end_of_game == None:
                    # Update End of Game Time
                    end_of_game = time.perf_counter()

                    # Update Player Health Stat
                    player.stats["health"] -= 1

                    # Update Player Mana Stat
                    player.stats["mana"] = 0

                    # Move to GameOver Loop
                    if player.stats["health"] == 0:
                        gameover_loop()

            # Restart Game
            if end_of_game != None:
                dt = time.perf_counter() - end_of_game
                if dt * 1000 >= 1000:
                    # Restart Game
                    restart_game()

        # Update
        redraw_game()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


def menu_loop():
    global menu
    
    menu = Menu()
    btn_switchcase = {
        "play": [init_game, game_loop],
        "options": [placeholder],
        None: [placeholder]
    }

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Menu Buttons
            btn_pressed = menu.get_button_pressed(event)
            for function in btn_switchcase[btn_pressed]:
                function()
            menu.handle_mousemotion(event)
            
        # Update
        redraw_menu()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


def gameover_loop():
    global gameover

    gameover = GameOver(
        score.value, high_score.value, start_of_gamesession)
    btn_switchcase = {
        "play": [init_game, game_loop],
        "options": [placeholder],
        "menu": [init_game, menu_loop],
        None: [placeholder]
    }
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # GameOver Buttons
            btn_pressed = gameover.get_button_pressed(event)
            for function in btn_switchcase[btn_pressed]:
                function()
            gameover.handle_mousemotion(event)

        # Update
        redraw_gameover()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


def paused_loop():
    global paused

    paused = Paused()
    btn_switchcase = {
        "play": [game_loop],
        "restart": [init_game, game_loop],
        "options": [placeholder],
        "menu": [init_game, menu_loop],
        None: [placeholder]
    }

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Paused Buttons
            btn_pressed = paused.get_button_pressed(event)
            for function in btn_switchcase[btn_pressed]:
                function()
            paused.handle_mousemotion(event)

        # Update
        redraw_paused()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


# Execute --------------------------------------------------------- #
if __name__ == "__main__":
    pygame.init()

    # Window
    win_size = (
        window.rect.width * window.enlarge,
        window.rect.height * window.enlarge)
    win = pygame.display.set_mode(win_size)
    display = pygame.Surface(window.rect.size)
    pygame.display.set_caption("Activate: Agility")
    clock = pygame.time.Clock()

    # !!!
    init_game()

    # Execute
    game_loop()
