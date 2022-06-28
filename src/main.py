from audio.color_identifier import SpecialColorAudioIdentifier
from player import Player
from windows.windows import window, background
from windows.gameover import GameOver
from windows.game import Game
from windows.menu import Menu
from windows.options import Options
from windows.gameover import GameOver
from windows.paused import Paused
from cursors import NormalCursor, SkillCrosshair, TransitionAnimation
from audio import Music, Sound, CountdownAudio
import pygame
import time
import sys


# Functions ------------------------------------------------------- #
def placeholder():  # !!!
    pass


def init_game():
    global player
    global start_of_game, start_of_gamesession, end_of_game

    # Player
    player.reset_statedirection()
    player.init_rect()
    player.init_teleportation()
    player.init_status()

    # Initialize Game Objects
    game.init_objects(player.maximum_stats)

    # Reset Countdown Audio Variables
    countdown_audio.reset_audioplayed()

    # Time 
    start_of_game = time.perf_counter()
    start_of_gamesession = start_of_game
    end_of_game = None

    # Intialize Countdown & Color Visual Identifier's start_of_game
    game.init_startofgame(start_of_game)


def restart_game():
    global player
    global start_of_game, end_of_game

    # Reset Game Variables
    game.reset_objects()
    game.reset_gamestate_soundvars()
    game.reset_abilityready_soundvars(player)
    
    # Reset Countdown Audio Variables
    countdown_audio.reset_audioplayed()

    # Player
    player.init_teleportation()
    player.init_winningstate()

    # Time
    start_of_game = time.perf_counter()
    end_of_game = None

    # Intialize Countdown & Color Visual Identifier's start_of_game
    game.init_startofgame(start_of_game)


def restart_startofgame():
    # Restart Countdown & Color Visual Identifier's start_of_game
    new_startofgame = time.perf_counter()
    game.init_startofgame(new_startofgame)


# Redraws --------------------------------------------------------- #
def redraw_game():
    # Background
    display.fill(background.color)
    background.draw_walls(display)

    # Game
    game.draw(display)

    # Player
    player.draw(display)

    # Cursor
    if player.stats["mana"] >= player.maximum_stats["mana"]:
        cursor_transition.draw(display)
    elif player.stats["mana"] >= player.maximum_stats["mana"] and cursor_transition.is_finished:
        crosshair.draw(display)
    else:
        cursor.draw(display)

    # Blit to Screen ---------------------------------------------- #
    resized_display = pygame.transform.scale(display, win_size)
    win.blit(resized_display, (0, 0))

    pygame.display.update()


def redraw_menu():
    # Background
    display.fill(background.color)
    background.draw_walls(display)

    # Menu's Background
    menu.draw_background(display)

    # Player
    player.draw(display)

    # Menu's Window
    menu.draw_menuwindow(display)

    # Cursor
    cursor.draw(display)

    # Blit to Screen ---------------------------------------------- #
    resized_display = pygame.transform.scale(display, win_size)
    win.blit(resized_display, (0, 0))

    pygame.display.update()


def redraw_options(from_loop):
    # Background
    display.fill(background.color)
    background.draw_walls(display)

    # Tiles
    if from_loop == "menu":
        menu.tiles.draw(display)
    elif from_loop == "pause":
        paused.tiles.draw(display)
    elif from_loop == "gameover":
        game.tiles.draw(display)

    # Player
    player.draw(display)

    # Options
    options.draw(display)

    # Cursor
    cursor.draw(display)

    # Blit to Screen ---------------------------------------------- #
    resized_display = pygame.transform.scale(display, win_size)
    win.blit(resized_display, (0, 0))

    pygame.display.update()


def redraw_gameover():
    # Background
    display.fill(background.color)
    background.draw_walls(display)
    game.tiles.draw(display)

    # Player
    player.draw(display)

    # GameOver
    gameover.draw(display)

    # Cursor
    cursor.draw(display)

    # Blit to Screen ---------------------------------------------- #
    resized_display = pygame.transform.scale(display, win_size)
    win.blit(resized_display, (0, 0))

    pygame.display.update()


def redraw_paused():
    # Background
    display.fill(background.color)
    background.draw_walls(display)
    game.tiles.draw(display)

    # Pause's Background
    paused.draw_background(display)

    # Player
    player.draw(display)

    # Pause's Window
    paused.draw_pausewindow(display)

    # Cursor
    cursor.draw(display)

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
            # Quit
            if event.type == pygame.QUIT:
                window.update_gameinfo(
                    game.highscore.value,
                    options.toggleable_buttons.buttons)
                run = False

            # KeyDown Detection
            if event.type == pygame.KEYDOWN:
                # Pause Game
                if event.key == pygame.K_ESCAPE:
                    sound.play_pause()
                    paused_loop("game")

            # Player Teleportation
            player.teleport(event)

        # Player
        player.update(
            game.tiles.speicaltile_rects,
            game.countdown.time_remaining,
            sound)
        if (player.stats["mana"] == player.maximum_stats["mana"] and
                not game.abilityready_played):
            game.abilityready_played = True
            sound.play_abilityready()

        # Game
        game.update(
            player.stats, 
            countdown_audio, 
            speicalcolor_audio_identifier)

        # Cursor
        cursor.update()
        crosshair.update()
        cursor_transition.update(player)

        # Countdown is Over
        if game.countdown.time_remaining == 0:
            # Win or Loss
            if player.on_specialtile:  # win
                # Update Tiles' State
                game.tiles.update_tiles_to_winstate()

                # Play Win Sound
                if not game.winsound_played:
                    sound.play_win()
                    game.winsound_played = True

                if end_of_game == None:
                    # Update End of Game Time
                    end_of_game = time.perf_counter()

                    # Update Player Mana Stat
                    if player.stats["mana"] < player.maximum_stats["mana"]:
                        player.stats["mana"] += 1

                    # Add to Score
                    game.score.value += 1

                    # Add to Highscore
                    if game.score.value > game.highscore.value:
                        game.highscore.value = game.score.value
            else:  # loss
                # Update Tiles' State
                game.tiles.update_tiles_to_lossdissipation()

                # Play Lost Sound
                if not game.lostsound_played:
                    sound.play_lost()
                    game.lostsound_played = True

                # Update Player Stats and End of Game Time
                if game.tiles.dissipated and end_of_game == None:
                    # Update End of Game Time
                    end_of_game = time.perf_counter()

                    # Update Player Health Stat
                    player.stats["health"] -= 1

                    # Update Player Mana Stat
                    player.stats["mana"] = 0

                    # Move to GameOver Loop
                    if player.stats["health"] == 0:
                        sound.play_gameover()
                        gameover_loop()

            # Restart Game
            if end_of_game != None:
                dt = time.perf_counter() - end_of_game
                if dt * 1000 >= 1000:
                    restart_game()

        # Update
        redraw_game()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


def menu_loop():
    global menu

    # Initialize Menu's Animation
    menu.init_animation()

    # Initialize Menu's Buttons Switchcase
    btn_switchcase = {
        "play": [init_game, game_loop],
        "options": options_loop,
        None: [placeholder]
    }

    # Loop
    run = True
    while run:
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                window.update_gameinfo(
                    game.highscore.value,
                    options.toggleable_buttons.buttons)
                run = False

            # Menu Buttons
            btn_pressed = menu.buttons.get_button_pressed(event, sound)
            if btn_pressed != "options":
                for function in btn_switchcase[btn_pressed]:
                    function()
            else:
                btn_switchcase[btn_pressed]("menu")
            menu.buttons.handle_mousemotion(event)
            
        # Cursor
        cursor.update()
        crosshair.update()

        # Update
        redraw_menu()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


def options_loop(from_loop):
    global options

    isfrom_paused = True if from_loop == "pause" else False

    # Initialize Options' Animation
    options.init_animation()

    # Initialize Options' Buttons Switchcase
    backbtn_switchcase = {
        "pause": [paused_loop],
        "menu": [init_game, menu_loop],
        "gameover": [gameover_loop]
    }
    if from_loop == "pause":  # from pause
        btn_switchcase = {
            "back": backbtn_switchcase[from_loop],
            "play": {
                "pause": [
                    game.countdown.restart_countdown_time, 
                    restart_startofgame,
                    game_loop]
            },
            "menu": [init_game, menu_loop],
            "animation": [placeholder],
            "music": [music.update],
            "sound": [
                sound.update, 
                countdown_audio.update, 
                speicalcolor_audio_identifier.update],
            None: [placeholder]
        }
    else:  # from menu or gameover
        btn_switchcase = {
            "back": backbtn_switchcase[from_loop],
            "play": {
                "menu": [init_game, game_loop],
                "gameover": [init_game, game_loop]
            },
            "menu": [init_game, menu_loop],
            "fullscreen": [placeholder],
            "music": [music.update],
            "sound": [
                sound.update, 
                countdown_audio.update, 
                speicalcolor_audio_identifier.update],
            None: [placeholder]
        }

    # Loop
    run = True
    while run:
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                window.update_gameinfo(
                    game.highscore.value,
                    options.toggleable_buttons.buttons)
                run = False

            # Options Redirect Buttons
            btn_pressed = options.redirect_buttons.get_button_pressed(event, sound)
            functions = btn_switchcase[btn_pressed]
            functions = functions[from_loop] if btn_pressed == "play" else functions
            if isfrom_paused and btn_pressed == "back":
                functions[0]("options")
            else:
                for function in functions:
                    function()

            options.redirect_buttons.handle_mousemotion(event)

            # Options Toggleable Buttons
            btn_pressed = options.toggleable_buttons.get_button_pressed(event, sound)
            functions = btn_switchcase[btn_pressed]
            if btn_pressed == "music" or btn_pressed == "sound":
                for function in functions:
                    function(options.toggleable_buttons.buttons)
            else:
                for function in functions:
                    function()

            options.toggleable_buttons.handle_mousemotion(event)
        
        # Cursor
        cursor.update()
        crosshair.update()

        # Update
        redraw_options(from_loop)
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


def gameover_loop():
    global gameover

    # Change Player's State to Idle/Standing
    player.state = "standing"

    # Initialize GameOver's Status & Animation
    gameover.init_status(
        game.score.value, 
        game.highscore.value, 
        start_of_gamesession)
    gameover.init_animation()

    # Initialize GameOver's Buttons Switchcase
    btn_switchcase = {
        "play": [init_game, game_loop],
        "options": options_loop,
        "menu": [init_game, menu_loop],
        None: [placeholder]
    }
    
    # Loop
    run = True
    while run:
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                window.update_gameinfo(
                    game.highscore.value,
                    options.toggleable_buttons.buttons)
                run = False

            # GameOver Buttons
            btn_pressed = gameover.buttons.get_button_pressed(event, sound)
            if btn_pressed != "options":
                for function in btn_switchcase[btn_pressed]:
                    function()
            else:
                btn_switchcase[btn_pressed]("gameover")
            gameover.buttons.handle_mousemotion(event)

        # Cursor
        cursor.update()
        crosshair.update()

        # Update
        redraw_gameover()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


def paused_loop(from_loop):
    global paused

    # Change Player's State to Idle/Standing
    player.state = "standing"

    # Initialize Pause's Status & Animation
    paused.init_status(game.score.value, game.highscore.value)
    paused.init_animation()
    if from_loop != "options":
        paused.init_tiles()

    # Initialize Pause's Buttons Switchcase
    btn_switchcase = {
        "play": [
            game.countdown.restart_countdown_time, 
            restart_startofgame, 
            game_loop],
        "restart": [init_game, game_loop],
        "options": options_loop,
        "menu": [init_game, menu_loop],
        None: [placeholder]
    }

    # Loop
    run = True
    while run:
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                window.update_gameinfo(
                    game.highscore.value,
                    options.toggleable_buttons.buttons)
                run = False

            # KeyDown Detection
            if event.type == pygame.KEYDOWN:
                # Back to Game
                if event.key == pygame.K_ESCAPE:
                    # Restart Countdown Time
                    game.countdown.restart_countdown_time()
                        
                    # Restart Countdown & Color Visual Identifier's start_of_game
                    restart_startofgame()

                    # Game Loop
                    game_loop()

            # Paused Buttons
            btn_pressed = paused.buttons.get_button_pressed(event, sound)
            if btn_pressed != "options":
                for function in btn_switchcase[btn_pressed]:
                    function()
            else:
                btn_switchcase[btn_pressed]("pause")
            paused.buttons.handle_mousemotion(event)
        
        # Cursor
        cursor.update()
        crosshair.update()

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
        int(window.rect.width * window.enlarge),
        int(window.rect.height * window.enlarge))
    win = pygame.display.set_mode(
        win_size, pygame.FULLSCREEN, 32)
    display = pygame.Surface(window.rect.size)
    pygame.display.set_caption("Activate: Agility")
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    # Initialize Player
    player = Player()

    # Initialize Windows
    game = Game()
    menu = Menu()
    options = Options()
    gameover = GameOver()
    paused = Paused()

    # Initialize Highscore
    game.init_highscore()

    # Initialize Cursors
    cursor = NormalCursor()
    crosshair = SkillCrosshair()
    cursor_transition = TransitionAnimation()

    # Initialize Audios 
    music = Music()
    sound = Sound(
        options.toggleable_buttons.buttons)
    countdown_audio = CountdownAudio(
        options.toggleable_buttons.buttons)
    speicalcolor_audio_identifier = SpecialColorAudioIdentifier(
        options.toggleable_buttons.buttons)

    # Execute
    menu_loop()
