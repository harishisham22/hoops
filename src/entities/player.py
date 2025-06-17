import pygame
import math

class Player:
    def __init__(self, window_height):
        self.x = 160
        self.y = window_height - 60
        self.width = 40
        self.height = 60
        self.speed = 5
        self.jumping = False
        self.jump_power = 15
        self.velocity_y = 0
        self.gravity = 0.8
        self.has_ball = False
        self.dribbling = False
        self.dribble_height = 0
        self.dribble_direction = 1
        # Double tap tracking
        self.last_a_press = 0
        self.last_d_press = 0
        self.last_w_press = 0
        self.double_tap_window = 300  # milliseconds
        self.dash_cooldown = 2000  # milliseconds
        self.last_dash_time = 0
        self.dash_speed = 15
        self.dash_duration = 200  # milliseconds
        self.dash_start_time = 0
        self.is_dashing = False

    def move(self, keys, ball, window_width):
        current_time = pygame.time.get_ticks()
        
        # Handle double tap dash
        if keys[pygame.K_a] and not self.is_dashing:
            if current_time - self.last_a_press < self.double_tap_window and current_time - self.last_dash_time > self.dash_cooldown:
                self.is_dashing = True
                self.dash_start_time = current_time
                self.last_dash_time = current_time
            self.last_a_press = current_time
            self.x -= self.speed
            if self.has_ball:
                self.dribble_direction = -1
                
        if keys[pygame.K_d] and not self.is_dashing:
            if current_time - self.last_d_press < self.double_tap_window and current_time - self.last_dash_time > self.dash_cooldown:
                self.is_dashing = True
                self.dash_start_time = current_time
                self.last_dash_time = current_time
            self.x += self.speed
            if self.has_ball:
                self.dribble_direction = 1

        # Handle dash movement
        if self.is_dashing:
            if current_time - self.dash_start_time < self.dash_duration:
                self.x -= self.dash_speed  # Dash left
            else:
                self.is_dashing = False

        # Jump with potential double tap dash
        if keys[pygame.K_w] and not self.jumping:
            if current_time - self.last_w_press < self.double_tap_window and current_time - self.last_dash_time > self.dash_cooldown:
                # Vertical dash
                self.velocity_y = -self.jump_power * 1.5
                self.last_dash_time = current_time
            else:
                self.velocity_y = -self.jump_power
            self.jumping = True
            self.last_w_press = current_time

        # Handle ball possession
        if self.has_ball:
            ball.x = self.x + self.width/2
            ball.y = self.y - 20 + self.dribble_height
            if not self.jumping:
                self.dribble_height = 10 * math.sin(pygame.time.get_ticks() * 0.01)
            else:
                self.dribble_height = 0
                ball.y = self.y - 20

    def update(self, window_width, window_height):
        # Apply gravity
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        # Ground collision
        if self.y > window_height - 60:
            self.y = window_height - 60
            self.jumping = False
            self.velocity_y = 0

        # Screen boundaries
        if self.x < 0:
            self.x = 0
        if self.x > window_width - self.width:
            self.x = window_width - self.width

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height)) 