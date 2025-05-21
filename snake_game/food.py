import pygame
import random

class Food:
    def __init__(self, screen_width, screen_height, block_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size
        self.color = (213, 50, 80) # Red color for food
        self.x = 0
        self.y = 0
        # Initial call to respawn will need a dummy snake body or be handled carefully
        # For now, let's assume it's called after snake is created.
        # Or, we can remove the initial respawn and let the game loop do it.
        # Let's remove it from __init__ to avoid issues with snake object not existing yet.

    def respawn(self, snake_body): # Added snake_body parameter
        while True:
            self.x = round(random.randrange(0, self.screen_width - self.block_size) / self.block_size) * self.block_size
            self.y = round(random.randrange(0, self.screen_height - self.block_size) / self.block_size) * self.block_size
            # Check if the new food position overlaps with any part of the snake's body
            if [self.x, self.y] not in snake_body:
                break # Valid position found

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.block_size, self.block_size])
