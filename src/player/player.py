from functions import clip_set_to_list_on_xaxis, separate_sets_from_yaxis, edge_collision
from windows.windows import window
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
        self.init_movement()
        self.init_rect()
        self.init_hitbox()
        self.init_winningstate()
        self.init_status()

        self.idx = 0
        self.maximum_stats = {
            "health": 3,
            "mana": 5,
            "stamina": 20}

    # Initialize Images
    def init_images(self):
        # Get Moving Spriteset
        moving_spriteset = pygame.image.load(
            f"{resources_path}/moving.png")
        
        # Seperate Moving Spriteset to their Directions
        seperated_movingspriteset = separate_sets_from_yaxis(
            moving_spriteset, (255 , 0, 0)) 

        # Images
        self.images = {
            "standing": self.get_idleimages(),
            "walking": self.get_walkimages(seperated_movingspriteset),
            "sprinting": self.get_sprintimages(seperated_movingspriteset)
        }

    def get_idleimages(self):
        direction_order = ["down", "up", "right", "left"]

        # Get Idle Spriteset
        spriteset = pygame.image.load(
            f"{resources_path}/idle.png")

        # Seperate Idle Spriteset to their Directions
        separated_spriteset = separate_sets_from_yaxis(
            spriteset, (255, 0, 0))

        # Put Idle Images into a Dictionary
        images = {}
        for name, spriteset in zip(direction_order, separated_spriteset):
            images[name] = clip_set_to_list_on_xaxis(spriteset)

        # Return Images
        return images 

    def get_walkimages(self, seperated_movingspriteset):
        direction_order = ["down", "up", "right", "left"]
        order_idxs = [0, 1, 0, 3]

        # Put Walk Images into a Dictionary
        images = {}
        for name, spriteset in zip(direction_order, seperated_movingspriteset):
            # Separate Moving Spriteset to their Sprites
            sprites = clip_set_to_list_on_xaxis(spriteset)

            # Order the Moving Spriteset's Sprites to Make a Walk Animation
            ordered_sprites = [sprites[idx] for idx in order_idxs]

            # Append Ordered Sprites
            images[name] = ordered_sprites

        # Return Images
        return images

    def get_sprintimages(self, seperated_movingspriteset):
        direction_order = ["down", "up", "right", "left"]
        order_idxs = [0, 1, 2, 1, 0, 3, 4, 3]

        # Put Sprint Images into a Dictionary
        images = {}
        for name, spriteset in zip(direction_order, seperated_movingspriteset):
            # Seperate Moving Spriteset to their Sprites
            sprites = clip_set_to_list_on_xaxis(spriteset)

            # Order the Moving Spriteset's Sprites to Make a Sprint Animation
            ordered_sprites = [sprites[idx] for idx in order_idxs]

            # Append Ordered Sprites
            images[name] = ordered_sprites

        # Return Images
        return images

    # Movement
    def init_movement(self):
        # Velocities
        self.walk_vel = 3
        self.sprint_vel = 5

        # State & Direction
        self.state = "standing"
        self.direction = "down"

        # Sprint Time
        self.last_sprint = time.perf_counter()
        self.sprint_stamina_degenerate = 125  # milliseconds

        # Walk Time
        self.last_walk = time.perf_counter()
        self.walk_stamina_degenerate = 800  # milliseconds

        # Regeneration
        self.stamina_regenerate = 1000  # milliseconds
        self.generate_stamina_switchcase = {
            "walking": self.degenerate_stamina_onwalk,
            "sprinting": self.degenerate_stamina_onsprint,
            "standing": self.regenerate_stamina
        }   

    # Rectangles
    def init_rect(self):
        size = self.images[self.state][self.direction][0].get_rect().size
        self.rect = pygame.Rect(player_data["starting_position"], size)

    def init_hitbox(self):
        pos = self.get_hitbox_pos_from_rect()
        size = player_data["hitbox_size"]
        self.hitbox = pygame.Rect(pos, size)

    # Status
    def init_winningstate(self):
        self.on_specialtile = False

    def init_status(self):
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

        # Check if Player is Standing
        self.check_if_standing()

        # Movement
        # if left-shift is down AND player's stamina is more than zero
        if keys[pygame.K_LSHIFT] and self.stats["stamina"] > 0:  # sprinting
            self.sprint_movement()
        # if left-shift is up AND player's stamina is more than zero
        elif not keys[pygame.K_LSHIFT] and self.stats["stamina"] > 0:  # walking
            self.walk_movement()
        # if player's stamina is less than or equal to zero
        elif self.stats["stamina"] <= 0:  # standing
            self.state = "standing"

        # Update Stamina Regeneration
        self.generate_stamina_switchcase[self.state]()

        # Update Hitbox Position
        self.update_hitbox()

    # Hitbox
    def update_hitbox(self):
        x, y = self.get_hitbox_pos_from_rect()
        self.hitbox.x = x
        self.hitbox.y = y

    # Special Tile Collision
    def specialtile_collision(self, specialtile_rects, time_remaining):
        if time_remaining > 0:  # check if time remaining is greater than zero so bugs won't occur
            for tile_rect in specialtile_rects:  # loop throught all rects of speical tiles
                if self.hitbox.colliderect(tile_rect):  # check if player and tile is colliding
                    self.on_specialtile = True
                    break
                else:
                    self.on_specialtile = False

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

    # Rectagnle & Hitbox
    def get_hitbox_pos_from_rect(self):
        x_offset, y_offset = player_data["recttohitbox_offset"]
        pos = (self.rect.x + x_offset, self.rect.y + y_offset)

        return pos

    def get_rect_pos_from_hitbox(self):
        x_offset, y_offset = player_data["recttohitbox_offset"]
        pos = (self.hitbox.x - x_offset, self.hitbox.y - y_offset)

        return pos

    # Check State
    def check_if_standing(self):
        keys = pygame.key.get_pressed()
        
        # Get Conditions
        not_left = not keys[pygame.K_a]
        not_right = not keys[pygame.K_d]
        not_up = not keys[pygame.K_w]
        not_down = not keys[pygame.K_s]

        # Check if Player is Standing
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

    # Teleportation
    def teleport(self, event):
        # Checks if Player's Mana is Sufficient to Use the Teleport Skill (mana == 5)
        sufficient_mana = self.stats["mana"] == self.maximum_stats["mana"]
        # Checks if Mouse's Left Click is Down
        leftclick_down = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

        # If Statement
        if sufficient_mana and leftclick_down:
            # Teleport Player's Hitbox Center to Mouse Position when Left-Clicked
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.hitbox.centerx = mouse_x / window.enlarge
            self.hitbox.centery = mouse_y / window.enlarge

            # Offset the Position of Player
            position = self.get_rect_pos_from_hitbox()
            self.rect.x, self.rect.y = position

            # Clears Mana
            self.stats["mana"] = 0

    # Reset
    def reset_statedirection(self):
        self.direction = "down"
        self.state = "standing"
