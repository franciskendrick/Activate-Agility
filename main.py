from player import Player
from windows import window, background, tiles
from windows.game import PlayerGauge, Countdown, speicalcolor_visual_identifier
from windows.menu import menu
import pygame
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
    global countdown
    countdown = Countdown()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # !!!
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # loss
                    tiles.lost = True

                if event.key == pygame.K_e:  # win
                    tiles.update_tiles_to_winstate()

        # Player
        player.update()

        # Windows
        tiles.update()

        # Windows.Game
        player_gauge.update(player.stats)
        countdown.update()

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
