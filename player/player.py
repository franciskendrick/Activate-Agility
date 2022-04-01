from functions import clip_set_to_list_on_xaxis, edge_collision
import pygame
import time
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class Player:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_rect()
        self.init_movement()

    def init_images(self):
        # Spriteset
        spriteset = pygame.image.load(
            f"{path}/assets/player.png")
        self.idx = 0

        # Images
        self.images = clip_set_to_list_on_xaxis(spriteset)

    def init_rect(self):
        size = self.images[self.idx].get_rect().size
        self.rect = pygame.Rect(100, 100, *size)

    def init_movement(self):
        # Velocities
        self.walk_vel = 3
        self.sprint_vel = 5

        # Time 
        self.last_sprint = time.perf_counter()
        self.stamina_degenerate = 250  # milliseconds
        self.stamina_regenerate = 500  # milliseconds

        # Stamina
        self.maximum_stamina = 20
        self.stamina = 20

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Reset
        if self.idx >= len(self.images) * 5:
            self.idx = 0

        # Draw
        img = self.images[self.idx // 5]
        display.blit(img, self.rect)

        # Update
        self.idx += 1

    # Update ------------------------------------------------------ #
    def update(self):
        self.movement()

    # Movement
    def movement(self):
        keys = pygame.key.get_pressed()

        # Sprint
        vel = self.get_velocity()

        # Movement
        if keys[pygame.K_a]:  # left
            self.move_x(-vel)
        if keys[pygame.K_d]:  # right
            self.move_x(vel)
        if keys[pygame.K_w]:  # up
            self.move_y(-vel)
        if keys[pygame.K_s]:  # down
            self.move_y(vel)

    # Functions --------------------------------------------------- #
    # Movement
    def get_velocity(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:  # shift is down
            if self.stamina > 0:  # still has stamina
                vel = self.sprint_vel

                # Update Stamina Stat
                dt = time.perf_counter() - self.last_sprint
                if dt * 1000 >= self.stamina_degenerate:
                    self.stamina -= 1
                    self.last_sprint = time.perf_counter()
            else:  # no stamina
                vel = self.walk_vel
        else:  # shift is up
            vel = self.walk_vel

            # Update Stamina Stat
            dt = time.perf_counter() - self.last_sprint
            if dt * 1000 >= self.stamina_regenerate:
                if self.stamina < 20:
                    self.stamina += 1
                self.last_sprint = time.perf_counter()
            
        return vel

    def move_x(self, vel):
        handle_rect = self.rect.copy()
        handle_rect.x += vel
        if not edge_collision(handle_rect):
            self.rect.x += vel

    def move_y(self, vel):
        handle_rect = self.rect.copy()
        handle_rect.y += vel
        if not edge_collision(handle_rect):
            self.rect.y += vel
