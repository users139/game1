import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, assets_path, speed_factor=1):
        super().__init__()
        self.speed = 10 * speed_factor 
        self.direction = direction # -1 for up (player), 1 for down (enemy)
        
        # Try to load an image, otherwise use a colored rectangle
        try:
            # Worker: If you can, create a simple bullet.png (e.g., a small yellow rectangle or circle)
            # and save it in the 'space_invaders_game/assets/' directory.
            # Dimensions should be small, e.g., 5x10 pixels for a vertical bullet.
            self.image_orig = pygame.image.load(f"{assets_path}/bullet.png").convert_alpha()
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.using_sprite = True
        except pygame.error:
            # print("Bullet sprite not found. Using a colored rectangle.") # Optional: can be noisy
            self.image = pygame.Surface([4, 10]) # Width, Height
            self.image.fill((255, 255, 0)) # Yellow color for bullet
            self.rect = self.image.get_rect()
            self.using_sprite = False
        
        self.rect.centerx = x
        self.rect.bottom = y # For player bullets, y is the top of the player
        if direction == 1: # Enemy bullet, y is bottom of enemy
             self.rect.top = y


    def update(self):
        self.rect.y += self.direction * self.speed
        # Remove bullet if it goes off screen
        if self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height():
            self.kill() # Removes sprite from all groups
