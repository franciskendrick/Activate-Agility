from player import Player
from windows import window, background
from windows.game import Tiles, PlayerGauge, Countdown, SpecialColorVisualIdentifier
from windows.menu import menu
import pygame
import time
import sys


# Functions
def placeholder():  # !!!
    pass


# Redraw
def redraw_game():
    # Background
    display.fill(background.color)
    background.draw_walls(display)
    tiles.draw(display)

    # Windows.Game
    player_gauge.draw(display)
    speicalcolor_visual_identifier.draw(display)
    countdown.draw(display)

    # Player
    player.draw(display)

    # Blit to Screen ---------------------------------------------- #
    resized_display = pygame.transform.scale(display, win_size)
    win.blit(resized_display, (0, 0))

    pygame.display.update()


def redraw_menu():
    # Background
    display.fill(background.color)

    # Menu
    menu.draw(display)

    # Blit to Screen ---------------------------------------------- #
    resized_display = pygame.transform.scale(display, win_size)
    win.blit(resized_display, (0, 0))

    pygame.display.update()


# Loop
def game_loop():
    global tiles, speicalcolor_visual_identifier, countdown

    # Initialize Game Variables
    tiles = Tiles()
    speicalcolor_visual_identifier = SpecialColorVisualIdentifier(
        tiles.specialtile_color)
    countdown = Countdown()
    
    # Start of Game
    start_of_game = time.perf_counter()
    speicalcolor_visual_identifier.start_of_game = start_of_game
    countdown.start_of_game = start_of_game

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Player
        player.update(
            tiles.speicaltile_rects,
            countdown.time_remaining)

        # Windows.Game
        player_gauge.update(player.stats)
        speicalcolor_visual_identifier.update()
        countdown.update()

        print(len(tiles.speicaltile_rects))

        # Win-Loss State
        if countdown.time_remaining == 0:
            if player.on_speicaltile:  # win
                tiles.update_tiles_to_winstate()
            else:  # loss
                tiles.update_tiles_to_lossdissipation()

        # Update
        redraw_game()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


def menu_loop():
    btn_switchcase = {
        "play": [game_loop],
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

    # Player
    player = Player()

    # Player Gauge
    player_gauge = PlayerGauge(player.maximum_stats)

    # Execute
    menu_loop()
