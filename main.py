import pygame


# Redraw
def redraw_game():
    pygame.display.update()


# Loop
def game_loop():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        redraw_game()
        clock.tick()


if __name__ == "__main__":
    pygame.init()

    # Window
    win_size = (640 * 2, 360 * 2)
    win = pygame.display.set_mode(win_size)
    display = pygame.Surface((640, 360))
    pygame.display.set_caption("Activate: Agility")
    clock = pygame.time.Clock()

    # Execute
    game_loop()
