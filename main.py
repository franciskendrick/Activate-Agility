from player import Player
from windows import window, background, tiles
from windows.game import PlayerGauge, player_gauge
from windows.menu import menu
import pygame
import sys


# Redraw
def redraw_game():
    # Background
    display.fill(background.color)
    background.draw_walls(display)
    tiles.draw(display)

    # Status Bar
    player_gauge.draw(display)

    # Player
    player.draw(display)

    # Blit to Screen ---------------------------------------------- #
    resized_display = pygame.transform.scale(display, win_size)
    win.blit(resized_display, (0, 0))

    pygame.display.update()


# Loop
def game_loop():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Player
        player.update()

        # Player Gauge
        player_gauge.update(player.stats)

        # Update
        redraw_game()
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
    game_loop()
