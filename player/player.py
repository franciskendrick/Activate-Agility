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
        self.init_winningstate()
        self.init_status()

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

    def init_winningstate(self):
        self.on_speicaltile = False

    def init_status(self):
        self.maximum_stats = {
            "health": 3,
            "mana": 5,
            "stamina": 20}
        self.stats = self.maximum_stats.copy()

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
    def update(self, specialtile_rects, tiles_dissipated, time_remaining):
        self.movement()
        self.specialtile_collision(
            specialtile_rects, tiles_dissipated, time_remaining)

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

    # Speical Tile Collision
    def specialtile_collision(self, specialtile_rects, tiles_dissipated, time_remaining):
        # Detect if Player is on Special Tile on Time Remaining: 0
        if time_remaining == 0 and not tiles_dissipated:  # time remaining is at zero AND tiles has not yet dissipated
            for tile_rect in specialtile_rects:  # loop through all rects of speical tiles
                if self.rect.colliderect(tile_rect):  # check of player and tile collision
                    self.on_speicaltile = True  

    # Functions --------------------------------------------------- #
    # Movement
    def get_velocity(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:  # shift is down
            if self.stats["stamina"] > 0:  # still has stamina
                vel = self.sprint_vel

                # Update Stamina Stat
                dt = time.perf_counter() - self.last_sprint
                if dt * 1000 >= self.stamina_degenerate:
                    self.stats["stamina"] -= 1
                    self.last_sprint = time.perf_counter()
            else:  # no stamina
                vel = self.walk_vel
        else:  # shift is up
            vel = self.walk_vel

            # Update Stamina Stat
            dt = time.perf_counter() - self.last_sprint
            if dt * 1000 >= self.stamina_regenerate:
                if self.stats["stamina"] < self.maximum_stats["stamina"]:
                    self.stats["stamina"] += 1
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
