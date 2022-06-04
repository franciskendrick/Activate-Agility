from player import Player
from windows import gameover
from windows.windows import window, background
from windows.game import Tiles, PlayerGauge, SpecialColorVisualIdentifier, Countdown, Score, HighScore
from windows.menu import Menu
from windows.options import Options
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

    # Initialize Game Variables
    tiles = Tiles()
    speicalcolor_visual_identifier = SpecialColorVisualIdentifier(
        tiles.specialtile_color)
    countdown = Countdown()
    player_gauge = PlayerGauge(player.maximum_stats)
    score = Score()

    # Time 
    start_of_game = time.perf_counter()
    start_of_gamesession = start_of_game
    end_of_game = None

    # Intialize Countdown & Color Visual Identifier's start_of_game
    countdown.init_startofgame(start_of_game)
    speicalcolor_visual_identifier.init_startofgame(start_of_game)


def restart_gamesession():
    global player
    global tiles, speicalcolor_visual_identifier
    global countdown, player_gauge, score, high_score
    global start_of_game, start_of_gamesession, end_of_game

    # Initialize Game Variables
    tiles = Tiles()
    speicalcolor_visual_identifier = SpecialColorVisualIdentifier(
        tiles.specialtile_color)
    countdown = Countdown()
    player_gauge = PlayerGauge(player.maximum_stats)
    score = Score()

    # Time 
    start_of_game = time.perf_counter()
    start_of_gamesession = start_of_game
    end_of_game = None

    # Intialize Countdown & Color Visual Identifier's start_of_game
    countdown.init_startofgame(start_of_game)
    speicalcolor_visual_identifier.init_startofgame(start_of_game)


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

    # Intialize Countdown & Color Visual Identifier's start_of_game
    countdown.init_startofgame(start_of_game)
    speicalcolor_visual_identifier.init_startofgame(start_of_game)


def restart_startofgame():
    # Restart Countdown & Color Visual Identifier's start_of_game
    new_startofgame = time.perf_counter()
    countdown.init_startofgame(new_startofgame)
    speicalcolor_visual_identifier.init_startofgame(new_startofgame)


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

    # Player
    player.draw(display)

    # Blit to Screen ---------------------------------------------- #
    resized_display = pygame.transform.scale(display, win_size)
    win.blit(resized_display, (0, 0))

    pygame.display.update()


def redraw_options():
    # Background
    display.fill(background.color)
    background.draw_walls(display)

    # Options
    options.draw(display)

    # Blit to Screen ---------------------------------------------- #
    resized_display = pygame.transform.scale(display, win_size)
    win.blit(resized_display, (0, 0))

    pygame.display.update()


def redraw_gameover():
    # Background
    display.fill(background.color)
    background.draw_walls(display)
    tiles.draw(display)

    # Player
    player.draw(display)

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
    tiles.draw(display)

    # Pause's Background
    paused.draw_background(display)

    # Player
    player.draw(display)

    # Pause's Window
    paused.draw_pausewindow(display)

    # Blit to Screen ---------------------------------------------- #
    resized_display = pygame.transform.scale(display, win_size)
    win.blit(resized_display, (0, 0))

    pygame.display.update()


# Loops ----------------------------------------------------------- #
def game_loop():
    global end_of_game

    # Loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.update_gameinfo(high_score.value)
                run = False

            if event.type == pygame.KEYDOWN:
                # Pause Game
                if event.key == pygame.K_ESCAPE:
                    paused_loop()

        # Player
        player.update(
            tiles.speicaltile_rects,
            countdown.time_remaining)

        # Windows.Game
        player_gauge.update(player.stats)
        speicalcolor_visual_identifier.update()
        countdown.update()

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
    
    # Initialize Menu
    menu = Menu()

    # Initialize Menu Buttons Switchcase
    btn_switchcase = {
        "play": [init_game, game_loop],
        "options": [placeholder],
        None: [placeholder]
    }

    # Loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.update_gameinfo(high_score.value)
                run = False

            # Menu Buttons
            btn_pressed = menu.buttons.get_button_pressed(event)
            for function in btn_switchcase[btn_pressed]:
                function()
            menu.buttons.handle_mousemotion(event)
            
        # Update
        redraw_menu()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


def options_loop():
    global options

    # Initialize Options
    options = Options()

    # Loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.update_gameinfo(high_score.value)
                run = False

            # Options Redirect Buttons
            options.redirect_buttons.handle_mousemotion(event)
        
        # Update
        redraw_options()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


def gameover_loop():
    global gameover

    # Change Player's State to Idle/Standing
    player.state = "standing"

    # Initialize GameOver
    gameover = GameOver(
        score.value, high_score.value, start_of_gamesession)

    # Initialize GameOver Buttons Switchcase
    btn_switchcase = {
        "play": [init_game, game_loop],
        "options": [placeholder],
        "menu": [init_game, menu_loop],
        None: [placeholder]
    }
    
    # Loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.update_gameinfo(high_score.value)
                run = False

            # GameOver Buttons
            btn_pressed = gameover.buttons.get_button_pressed(event)
            for function in btn_switchcase[btn_pressed]:
                function()
            gameover.buttons.handle_mousemotion(event)

        # Update
        redraw_gameover()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


def paused_loop():
    global paused

    # Change Player's State to Idle/Standing
    player.state = "standing"

    # Initialize Paused
    paused = Paused(
        score.value, high_score.value)

    # Initialize Paused Buttons Switchcase
    btn_switchcase = {
        "play": [
            countdown.restart_countdown_time, 
            restart_startofgame, 
            game_loop],
        "restart": [init_game, game_loop],
        "options": [placeholder],
        "menu": [init_game, menu_loop],
        None: [placeholder]
    }

    # Loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.update_gameinfo(high_score.value)
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Restart Countdown Time
                    countdown.restart_countdown_time()
                        
                    # Restart Countdown & Color Visual Identifier's start_of_game
                    restart_startofgame()

                    # Game Loop
                    game_loop()

            # Paused Buttons
            btn_pressed = paused.buttons.get_button_pressed(event)
            for function in btn_switchcase[btn_pressed]:
                function()
            paused.buttons.handle_mousemotion(event)

        # Update
        redraw_paused()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


# Execute --------------------------------------------------------- #
if __name__ == "__main__":
    pygame.init()

    # Initialize Window
    win_size = (
        window.rect.width * window.enlarge,
        window.rect.height * window.enlarge)
    win = pygame.display.set_mode(win_size)
    display = pygame.Surface(window.rect.size)
    pygame.display.set_caption("Activate: Agility")
    clock = pygame.time.Clock()

    # Initialize Player
    player = Player()

    # Initialize Highscore
    high_score = HighScore()
    
    # Execute
    options_loop()
