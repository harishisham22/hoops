import pygame

class Hoop:
    def __init__(self, window_width, window_height):
        self.x = window_width - 300
        self.y = window_height - 250
        self.width = 80
        self.height = 60
        self.rim_width = 60
        self.rim_height = 5

    def draw(self, screen):
        # Draw backboard
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))
        # Draw rim
        pygame.draw.rect(screen, (255, 0, 0), (self.x + 10, self.y + 40, self.rim_width, self.rim_height))

    def check_score(self, ball):
        if (ball.x > self.x + 10 and ball.x < self.x + 70 and
            ball.y > self.y + 40 and ball.y < self.y + 45 and
            ball.velocity_y > 0):
            return True
        return False 