import pygame
# Assuming bullet.py is in the same directory, otherwise adjust import
from bullet import Bullet 

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type, assets_path):
        super().__init__()
        self.enemy_type = enemy_type
        self.assets_path = assets_path # Store assets_path for shooting

        try:
            image_name = f"enemy_{self.enemy_type}.png"
            self.image_orig = pygame.image.load(f"{self.assets_path}/{image_name}").convert_alpha()
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.using_sprite = True
        except pygame.error:
            self.image = pygame.Surface([30, 30])
            self.image.fill((200, 0, 0))
            self.rect = self.image.get_rect()
            self.using_sprite = False
        
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Movement is now handled globally for the group in main.py
        pass

    def shoot(self):
        # Bullet starts from the bottom-middle of the enemy
        # Direction is 1 (downwards for enemy bullets)
        bullet = Bullet(self.rect.centerx, self.rect.bottom, 1, self.assets_path)
        return bullet
