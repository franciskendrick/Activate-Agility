from functions import clip_set_to_list_on_xaxis, separate_sets_from_yaxis, edge_collision
import pygame
import json
import time
import os

pygame.init()
resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", 
        "resources", "player"
        )
    )

# Json
with open(f"{resources_path}/player.json") as json_file:
    player_data = json.load(json_file)


class Player:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_direction()
        self.init_movement()
        self.init_rect()
        self.init_hitbox()
        self.init_winningstate()
        self.init_status()

    def init_images(self):
        direction_order = ["down", "up", "right", "left"]
        self.idx = 0

        # Get Idle Spriteset
        spriteset = pygame.image.load(
            f"{resources_path}/idle.png")
        idle_spriteset = separate_sets_from_yaxis(
            spriteset, (255, 0, 0))

        # Get Moving Spriteset
        spriteset = pygame.image.load(
            f"{resources_path}/moving.png")
        moving_spriteset = separate_sets_from_yaxis(
            spriteset, (255, 0, 0))

        # Get Walk Images from Moving Spriteset
        walk_images = {}
        order_idxs = [0, 1, 0, 3]
        for name, spriteset in zip(direction_order, moving_spriteset):
            # Seperate Moving Spriteset
            sprites = clip_set_to_list_on_xaxis(spriteset)

            # Get Sprite List
            sprite_list = []
            for idx in order_idxs:
                sprite_list.append(sprites[idx])

            # Append
            walk_images[name] = sprite_list

        # Get Sprint Images from Moving Spriteset
        sprint_images = {}
        order_idxs = [0, 1, 2, 1, 0, 3, 4, 3]
        for name, spriteset in zip(direction_order, moving_spriteset):
            # Seperate Moving Spriteset
            sprites = clip_set_to_list_on_xaxis(spriteset)

            # Get Sprite List
            sprite_list = []
            for idx in order_idxs:
                sprite_list.append(sprites[idx])

            # Append
            sprint_images[name] = sprite_list

        # Images
        self.images = {
            "standing": {
                name:clip_set_to_list_on_xaxis(spriteset) 
                    for name, spriteset in zip(
                        direction_order, idle_spriteset)
            },
            "walking": walk_images,
            "sprinting": sprint_images
        }

    def init_direction(self):
        self.direction = "down"

    def init_rect(self):
        size = self.images[self.state][self.direction][self.idx].get_rect().size
        self.rect = pygame.Rect(player_data["starting_position"], size)

    def init_hitbox(self):
        pos = self.get_hitbox_pos()
        size = player_data["hitbox_size"]
        self.hitbox = pygame.Rect(pos, size)

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
        self.on_specialtile = False

    def init_status(self):
        self.maximum_stats = {
            "health": 3,
            "mana": 5,
            "stamina": 20}
        self.original_stats = {
            "health": 3,
            "mana": 0,
            "stamina": 20}
        self.stats = {
            "health": 3,
            "mana": 0,
            "stamina": 20}

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        images = self.images[self.state][self.direction]
        # Reset
        if self.idx >= len(images) * 5:
            self.idx = 0

        # Draw
        img = images[self.idx // 5]
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

        # Update Hitbox Position
        self.update_hitbox()

    # Hitbox
    def update_hitbox(self):
        x, y = self.get_hitbox_pos()
        self.hitbox.x = x
        self.hitbox.y = y

    # Speical Tile Collision
    def specialtile_collision(self, specialtile_rects, time_remaining):
        # Detect if Player is on Special Tile on Time Remaining: 0
        if time_remaining == 0:  # time remaining is at zero
            for tile_rect in specialtile_rects:  # loop through all rects of speical tiles
                if self.hitbox.colliderect(tile_rect):  # check of player and tile collision
                    self.on_specialtile = True 
            specialtile_rects.clear()

    # Functions --------------------------------------------------- #
    # Movement & Direction
    def sprint_movement(self):
        keys = pygame.key.get_pressed()

        # Left
        if keys[pygame.K_a]: 
            self.move_x(-self.sprint_vel)
            self.direction = "left"
            self.state = "sprinting"
        # Right
        if keys[pygame.K_d]: 
            self.move_x(self.sprint_vel)
            self.direction = "right" 
            self.state = "sprinting"
        # Up
        if keys[pygame.K_w]:
            self.move_y(-self.sprint_vel)
            self.direction = "up"
            self.state = "sprinting"
        # Down
        if keys[pygame.K_s]:
            self.move_y(self.sprint_vel)
            self.direction = "down"
            self.state = "sprinting"

    def walk_movement(self):
        keys = pygame.key.get_pressed()

        # Left
        if keys[pygame.K_a]: 
            self.move_x(-self.walk_vel)
            self.direction = "left"
            self.state = "walking"
        # Right
        if keys[pygame.K_d]: 
            self.move_x(self.walk_vel)
            self.direction = "right" 
            self.state = "walking"
        # Up
        if keys[pygame.K_w]:
            self.move_y(-self.walk_vel)
            self.direction = "up"
            self.state = "walking"
        # Down
        if keys[pygame.K_s]:
            self.move_y(self.walk_vel)
            self.direction = "down"
            self.state = "walking"

    def move_x(self, vel):
        handle_hitbox = self.hitbox.copy()
        handle_hitbox.x += vel
        if not edge_collision(handle_hitbox):
            self.rect.x += vel

    def move_y(self, vel):
        handle_hitbox = self.hitbox.copy()
        handle_hitbox.y += vel
        if not edge_collision(handle_hitbox):
            self.rect.y += vel

    # Hitbox
    def get_hitbox_pos(self):
        x_offset, y_offset = player_data["recttohitbox_offset"]
        pos = (self.rect.x + x_offset, self.rect.y + y_offset)

        return pos

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

    # Stats
    def reset_stats(self):
        self.stats = self.original_stats.copy()
