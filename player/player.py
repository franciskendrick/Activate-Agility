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

        # Sprint Time 
        self.last_sprint = time.perf_counter()
        self.sprint_stamina_degenerate = 125  # milliseconds

        # Walk Time
        self.last_walk = time.perf_counter()
        self.walk_stamina_degenerate = 1000  # milliseconds

        # Regeneration Time
        self.stamina_regenerate = 1000  # milliseconds

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
    def update(self, specialtile_rects, time_remaining):
        self.movement()
        self.specialtile_collision(specialtile_rects, time_remaining)

    # Movement
    def movement(self):
        keys = pygame.key.get_pressed()

        # Sprint
        vel = self.get_velocity()

        # Movement
        is_walking = False
        if keys[pygame.K_a]:  # left
            self.move_x(-vel)
            is_walking = True
        if keys[pygame.K_d]:  # right
            self.move_x(vel)
            is_walking = True
        if keys[pygame.K_w]:  # up
            self.move_y(-vel)
            is_walking = True
        if keys[pygame.K_s]:  # down
            self.move_y(vel)
            is_walking = True

        # Degenerate Stamina (walk)
        if is_walking:
            dt = time.perf_counter() - self.last_walk
            if dt * 1000 >= self.walk_stamina_degenerate:
                self.stats["stamina"] -= 1
                self.last_walk = time.perf_counter()

        else:
            walk_dt = time.perf_counter() - self.last_walk
            sprint_dt = time.perf_counter() - self.last_sprint
            if walk_dt * 1000 >= self.stamina_regenerate:
                if self.stats["stamina"] < self.maximum_stats["stamina"]:
                    self.stats["stamina"] += 1
                self.last_walk = time.perf_counter()
            elif sprint_dt * 1000 >= self.stamina_regenerate:
                if self.stats["stamina"] < self.maximum_stats["stamina"]:
                    self.stats["stamina"] += 1
                self.last_sprint = time.perf_counter()

    # Speical Tile Collision
    def specialtile_collision(self, specialtile_rects, time_remaining):
        # Detect if Player is on Special Tile on Time Remaining: 0
        if time_remaining == 0:  # time remaining is at zero
            for tile_rect in specialtile_rects:  # loop through all rects of speical tiles
                if self.rect.colliderect(tile_rect):  # check of player and tile collision
                    self.on_speicaltile = True 
            specialtile_rects.clear()

    # Functions --------------------------------------------------- #
    # Movement
    def get_velocity(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] and self.stats["stamina"] > 0:  # shift is down AND still has stamina
            vel = self.sprint_vel

            # Degenerate Stamina (sprint)
            dt = time.perf_counter() - self.last_sprint
            if dt * 1000 >= self.sprint_stamina_degenerate:
                self.stats["stamina"] -= 1
                self.last_sprint = time.perf_counter()
        else:  # shift is up OR no stamina
            vel = self.walk_vel

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
