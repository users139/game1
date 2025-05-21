import pygame

class Snake:
    def __init__(self, screen_width, screen_height, block_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size
        self.body_color = (0, 128, 0) # Dark Green for the body
        self.head_color = (0, 200, 0) # A Lighter Green for the head
        self.reset()

    def reset(self):
        self.x = self.screen_width / 2
        self.y = self.screen_height / 2
        self.x_change = 0
        self.y_change = 0
        self.body = [[self.x, self.y]]
        self.length = 1

    def move(self):
        self.x += self.x_change
        self.y += self.y_change
        snake_head = [self.x, self.y]
        self.body.append(snake_head)
        if len(self.body) > self.length:
            del self.body[0]

    def grow(self):
        self.length += 1

    def draw(self, screen):
        # Draw the head first
        if self.body: # Ensure body is not empty
            head_segment = self.body[-1]
            pygame.draw.rect(screen, self.head_color, [head_segment[0], head_segment[1], self.block_size, self.block_size])
            # Draw the rest of the body
            for segment in self.body[:-1]:
                pygame.draw.rect(screen, self.body_color, [segment[0], segment[1], self.block_size, self.block_size])

    def check_collision_with_self(self):
        snake_head = [self.x, self.y]
        # Check collision with the part of the body excluding the actual head (last segment)
        # but including the segment that was previously the head if the snake is long enough
        for segment in self.body[:-1]:
            if segment == snake_head:
                return True
        return False

    def check_collision_with_wall(self):
        if self.x >= self.screen_width or self.x < 0 or self.y >= self.screen_height or self.y < 0:
            return True
        return False

    def change_direction(self, direction):
        if direction == "LEFT" and self.x_change == self.block_size:
            return
        if direction == "RIGHT" and self.x_change == -self.block_size:
            return
        if direction == "UP" and self.y_change == self.block_size:
            return
        if direction == "DOWN" and self.y_change == -self.block_size:
            return

        if direction == "LEFT":
            self.x_change = -self.block_size
            self.y_change = 0
        elif direction == "RIGHT":
            self.x_change = self.block_size
            self.y_change = 0
        elif direction == "UP":
            self.y_change = -self.block_size
            self.x_change = 0
        elif direction == "DOWN":
            self.y_change = self.block_size
            self.x_change = 0
