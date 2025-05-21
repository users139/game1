import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, assets_path):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.assets_path = assets_path
        self.speed = 5
        
        try:
            self.image_orig = pygame.image.load(f"{self.assets_path}/player_ship.png").convert_alpha()
            # Scale the image if it's too big/small - e.g. self.image_orig = pygame.transform.scale(self.image_orig, (width, height))
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.using_sprite = True
        except pygame.error:
            print("Player sprite not found. Using a colored rectangle.")
            self.image = pygame.Surface([50, 30])
            self.image.fill((0, 200, 0))
            self.rect = self.image.get_rect()
            self.using_sprite = False

        self.initial_x = screen_width // 2
        self.initial_y = screen_height - 10
        self.rect.centerx = self.initial_x
        self.rect.bottom = self.initial_y
        
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_delay = 250 
        self.hidden = False # For when player is hit
        self.hide_timer = pygame.time.get_ticks()

    def move_left(self):
        if not self.hidden:
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0

    def move_right(self):
        if not self.hidden:
            self.rect.x += self.speed
            if self.rect.right > self.screen_width:
                self.rect.right = self.screen_width

    def shoot(self):
        if not self.hidden:
            now = pygame.time.get_ticks()
            if now - self.last_shot_time > self.shoot_delay:
                self.last_shot_time = now
                bullet = Bullet(self.rect.centerx, self.rect.top, -1, self.assets_path) 
                return bullet
        return None

    def hide(self):
        # Hide player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (self.screen_width / 2, self.screen_height + 200) # Move off screen

    def unhide(self):
        self.hidden = False
        self.rect.centerx = self.initial_x
        self.rect.bottom = self.initial_y
            
    def update(self):
        # Unhide if hidden after a delay
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000: # 1 second hidden
            self.unhide()
        pass
