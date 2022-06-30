from functions import clip_set_to_list_on_xaxis, separate_sets_from_yaxis, edge_collision
from windows.windows import window
from .teleportation_particles import TeleportationParticles
from .teleport_sizedecrease import TeleportSizeDecrease
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
        self.init_teleportation()
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
        
        # Separate Moving Spriteset to their Directions
        separated_movingspriteset = separate_sets_from_yaxis(
            moving_spriteset, (255 , 0, 0)) 

        # Images
        self.images = {
            "standing": self.get_idleimages(),
            "walking": self.get_walkimages(separated_movingspriteset),
            "sprinting": self.get_sprintimages(separated_movingspriteset)
        }

    def get_idleimages(self):
        # Get Idle Spriteset
        spriteset = pygame.image.load(
            f"{resources_path}/idle.png")

        # Separated Idle Spriteset to their Directions
        separated_spriteset = separate_sets_from_yaxis(
            spriteset, (255, 0, 0))

        # Put Idle Images into a Dictionary
        images = {}
        for name, spriteset in zip(player_data["direction_order"], separated_spriteset):
            images[name] = clip_set_to_list_on_xaxis(spriteset)

        # Return Images
        return images 

    def get_walkimages(self, separated_movingspriteset):
        # Put Walk Images into a Dictionary
        images = {}
        for name, spriteset in zip(player_data["direction_order"], separated_movingspriteset):
            # Separate Moving Spriteset to their Sprites
            sprites = clip_set_to_list_on_xaxis(spriteset)

            # Order the Moving Spriteset's Sprites to Make a Walk Animation
            ordered_sprites = [sprites[idx] for idx in player_data["walk_index_order"]]

            # Append Ordered Sprites
            images[name] = ordered_sprites

        # Return Images
        return images

    def get_sprintimages(self, separated_movingspriteset):
        # Put Sprint Images into a Dictionary
        images = {}
        for name, spriteset in zip(player_data["direction_order"], separated_movingspriteset):
            # Separate Moving Spriteset to their Sprites
            sprites = clip_set_to_list_on_xaxis(spriteset)

            # Order the Moving Spriteset's Sprites to Make a Sprint Animation
            ordered_sprites = [sprites[idx] for idx in player_data["sprint_index_order"]]

            # Append Ordered Sprites
            images[name] = ordered_sprites

        # Return Images
        return images

    # Movement
    def init_movement(self):
        # Velocities
        self.walk_vel = 2
        self.sprint_vel = 4

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

    # Teleportation
    def init_teleportation(self):
        # Teleportation Particles
        self.t_particles = TeleportationParticles()
        self.destination_position = None

        # Teleportation Player Size Decrease & Increase
        self.t_sizedecrease = TeleportSizeDecrease()
        self.start_sizedecrease = False
        self.start_sizeincrease = False

        # Sound
        self.disapparition_played = False
        self.apparition_played = False

        # Is Teleporting
        self.is_teleporting = False

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
        
        # Get Multiplier
        dt = round(window.delta_time)
        dt_multiplier = round(5 / dt) if dt > 0 else 0
        multiplier = dt_multiplier if dt_multiplier > 0 else 5 

        # Reset
        if self.idx >= len(images) * multiplier:
            self.idx = 0
        
        # Draw Player
        if not self.start_sizedecrease:
            img = images[self.idx // multiplier]
            display.blit(img, self.rect)

        # Draw Teleport
        if self.is_teleporting:
            # Draw Player's Teleporting Size Decrease & Increase
            if self.start_sizedecrease:
                self.t_sizedecrease.draw_disapparition(display, self.direction)
            if self.start_sizeincrease:
                self.t_sizedecrease.draw_apparition(display, self.direction)

            # Draw Teleport Particles
            self.t_particles.draw_disapparition(display)
            self.t_particles.draw_apparition(display)

        # Update
        self.idx += 1

    # Update ------------------------------------------------------ #
    def update(self, specialtile_rects, time_remaining, sound):
        if self.is_teleporting:
            self.state = "standing"
        else:
            self.movement()
        self.specialtile_collision(specialtile_rects, time_remaining)
        self.update_teleportation_variables(sound)

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
        pos = self.get_hitbox_pos_from_rect()
        self.hitbox.x, self.hitbox.y = pos

    # Special Tile Collision
    def specialtile_collision(self, specialtile_rects, time_remaining):
        if time_remaining > 0:  # check if time remaining is greater than zero so bugs won't occur
            for tile_rect in specialtile_rects:  # loop throught all rects of speical tiles
                if self.hitbox.colliderect(tile_rect):  # check if player and tile is colliding
                    self.on_specialtile = True
                    break
                else:
                    self.on_specialtile = False

    # Teleportation
    def update_teleportation_variables(self, sound):
        # Reset Teleportation Variables
        if self.t_particles.has_disapparated:
            # Reset Teleporting Variable
            self.is_teleporting = False

            # Reset Teleport Particles Animation Variables
            self.t_particles.init_animationvariables()

            # Reset Player's Teleport Size Decrease and Increase Variables
            self.t_sizedecrease.init_animationvariables()
            self.start_sizedecrease = False
            self.start_sizeincrease = False

            # Reset Teleporting Sound Variables
            self.disapparition_played = False
            self.apparition_played = False

        # If Player is Teleporting
        if self.is_teleporting:
            # Get Multiplier
            dt = round(window.delta_time)
            dt_multiplier = round(3 / dt) if dt > 0 else 0
            multiplier = dt_multiplier if dt_multiplier > 0 else 3

            # Disapparition ----------------------------------------------------------- #
            particles_d_idx = self.t_particles.disapparition_idx

            # Teleport Player to Destination
            if particles_d_idx == 6 * multiplier:
                # Teleport Player's Hitbox Center to Destination Position
                hitbox_x, hitbox_y = self.get_hitbox_pos_from_rect(
                    *self.destination_position)
                self.hitbox.centerx = hitbox_x / window.enlarge
                self.hitbox.centery = hitbox_y / window.enlarge

                # Offset the Position of Player
                self.rect.x, self.rect.y = self.destination_position

                # Clear Destination Position 
                self.destination_position = None

            # Toggle On Start Player's Size Decrease
            if particles_d_idx >= 3 * multiplier and not self.t_sizedecrease.has_disapparated:
                self.start_sizedecrease = True

            # Toggle On Start Player's Disapparition Sound
            if particles_d_idx >= 5 * multiplier and not self.disapparition_played:
                sound.play_disapparition()
                self.disapparition_played = True

            # Apparition -------------------------------------------------------------- #
            particles_a_idx = self.t_particles.apparated_idx

            # Toggle On Start Player's Size Increase
            if (particles_a_idx >= 0 * multiplier and 
                    self.t_sizedecrease.has_disapparated and 
                    not self.t_sizedecrease.has_apparated):
                self.start_sizeincrease = True

            # Toggle On Start Player's Apparition
            if (particles_a_idx >= 0 * multiplier and 
                    self.t_sizedecrease.has_disapparated and 
                    not self.apparition_played):
                sound.play_apparition()
                self.apparition_played = True

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
        handle_hitbox.x += vel * window.delta_time
        if not edge_collision(handle_hitbox):  # hitbox is not colliding with room's edges
            self.rect.x += vel * round(window.delta_time)
        elif handle_hitbox.centerx > window.room_rect.centerx:  # player is in the right side of the room
            self.rect.right = window.room_rect.right

    def move_y(self, vel):
        handle_hitbox = self.hitbox.copy()
        handle_hitbox.y += vel * window.delta_time
        if not edge_collision(handle_hitbox):  # hitbox is not colliding with room's edges
            self.rect.y += vel * round(window.delta_time)
        elif handle_hitbox.centery > window.room_rect.centery:  # player is in the right side of the room
            self.rect.bottom = window.room_rect.bottom

    # Rectagnle & Hitbox
    def get_hitbox_pos_from_rect(self, x=None, y=None):
        x_offset, y_offset = player_data["recttohitbox_offset"]
        if (x, y) != (None, None):  # if there is a value given
            pos = (x + x_offset, y + y_offset)
        else:  # if there isn't a value given
            pos = (self.rect.x + x_offset, self.rect.y + y_offset)

        return pos

    def get_rect_pos_from_hitbox(self, x=None, y=None):
        x_offset, y_offset = player_data["recttohitbox_offset"]
        if (x, y) != (None, None):  # if there is a value given
            pos = (x - x_offset, y - y_offset)
        else:  # if there isn't a value given
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

        # Regenerate Stamina
        if (walk_dt * 1000 >= self.stamina_regenerate and
                sprint_dt * 1000 >= self.stamina_regenerate):

            # Update Player Stamina Stat
            if self.stats["stamina"] < self.maximum_stats["stamina"]:
                self.stats["stamina"] += 1

            # Update Walk and Sprint Time
            self.last_walk = time.perf_counter()
            self.last_sprint = time.perf_counter()

    # Teleportation
    def teleport(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Mouse's Left Click is Down 
        # Player's Mana is Sufficient to Use the Teleport Skill (mana == 5)
        # Cursor is Inside the Playable Room
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and 
                self.stats["mana"] == self.maximum_stats["mana"] and
                window.room_rect.collidepoint(
                    mouse_x / window.enlarge, mouse_y / window.enlarge)):

            # Get From Position
            from_position = (self.rect.x, self.rect.y)

            # Get Destination Position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.destination_position = self.get_rect_pos_from_hitbox(
                mouse_x / window.enlarge,
                mouse_y / window.enlarge)

            # Initialize Particles Positions
            self.t_particles.init_positions(
                from_position, self.destination_position)

            # Initialize Player's Size Decrease Positions
            self.t_sizedecrease.init_positions(
                from_position, self.destination_position)

            # Toggle On Teleporting
            self.is_teleporting = True

            # Clears Mana
            self.stats["mana"] = 0

    # Reset
    def reset_statedirection(self):
        self.direction = "down"
        self.state = "standing"
