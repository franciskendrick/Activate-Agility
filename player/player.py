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

        # State
        self.state = "standing"

        # Sprint Time 
        self.last_sprint = time.perf_counter()
        self.sprint_stamina_degenerate = 125  # milliseconds

        # Walk Time
        self.last_walk = time.perf_counter()
        self.walk_stamina_degenerate = 800  # milliseconds

        # Regeneration Time
        self.stamina_regenerate = 1000  # milliseconds

    def init_winningstate(self):
        self.on_speicaltile = False

    def init_status(self):
        self.maximum_stats = {
            "health": 3,
            "mana": 5,
            "stamina": 20}
        self.stats = {
            "health": 3,
            "mana": 0,
            "stamina": 20}

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

        # Check Standing State
        self.check_standing_state()

        # Movement
        if keys[pygame.K_LSHIFT] and self.stats["stamina"] > 0:  # sprinting
            self.sprint_movement()
        elif not keys[pygame.K_LSHIFT] and self.stats["stamina"] > 0:  # walking
            self.walk_movement()
        elif self.stats["stamina"] <= 0:  # standint
            self.state = "standing"

        # Update Stamina Regeneration
        if self.state == "walking":  # degenerate stamina (on walking)
            self.degenerate_stamina_onwalk()
        elif self.state == "sprinting":  # degenerate stamina (on sprinting)
            self.degenerate_stamina_onsprint()
        elif self.state == "standing":  # regenerate stamina (standing)
            self.regenerate_stamina()
        
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
    def sprint_movement(self):
        keys = pygame.key.get_pressed()

        # Left
        if keys[pygame.K_a]: 
            self.move_x(-self.sprint_vel)
            self.state = "sprinting"
        # Right
        if keys[pygame.K_d]: 
            self.move_x(self.sprint_vel)
            self.state = "sprinting"
        # Up
        if keys[pygame.K_w]:
            self.move_y(-self.sprint_vel)
            self.state = "sprinting"
        # Down
        if keys[pygame.K_s]:
            self.move_y(self.sprint_vel)
            self.state = "sprinting"

    def walk_movement(self):
        keys = pygame.key.get_pressed()

        # Left
        if keys[pygame.K_a]: 
            self.move_x(-self.walk_vel)
            self.state = "walking"
        # Right
        if keys[pygame.K_d]: 
            self.move_x(self.walk_vel)
            self.state = "walking"
        # Up
        if keys[pygame.K_w]:
            self.move_y(-self.walk_vel)
            self.state = "walking"
        # Down
        if keys[pygame.K_s]:
            self.move_y(self.walk_vel)
            self.state = "walking"

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

    # Check State
    def check_standing_state(self):
        keys = pygame.key.get_pressed()
        
        # Get Conditions
        not_left = not keys[pygame.K_a]
        not_right = not keys[pygame.K_d]
        not_up = not keys[pygame.K_w]
        not_down = not keys[pygame.K_s]

        # Check State
        if not_left and not_right and not_up and not_down:
            self.state = "standing"

    # Stamina Status
    def degenerate_stamina_onwalk(self):
        dt = time.perf_counter() - self.last_walk
        if dt * 1000 >= self.walk_stamina_degenerate:
            if self.stats["stamina"] > 0:
                self.stats["stamina"] -= 1
            self.last_walk = time.perf_counter()

    def degenerate_stamina_onsprint(self):
        dt = time.perf_counter() - self.last_sprint
        if dt * 1000 >= self.sprint_stamina_degenerate:
            if self.stats["stamina"] > 0:
                self.stats["stamina"] -= 1
            self.last_sprint = time.perf_counter()

    def regenerate_stamina(self):
        # Get Delta Time
        walk_dt = time.perf_counter() - self.last_walk
        sprint_dt = time.perf_counter() - self.last_sprint

        # Get Conditions
        regen_on_walk = walk_dt * 1000 >= self.stamina_regenerate
        regen_on_sprint = sprint_dt * 1000 >= self.stamina_regenerate

        # If Statement
        if regen_on_walk or regen_on_sprint:
            # Update Player Stamina Stat
            if self.stats["stamina"] < self.maximum_stats["stamina"]:
                self.stats["stamina"] += 1

            # Update Walk and Sprint Time
            self.last_walk = time.perf_counter()
            self.last_sprint = time.perf_counter()


