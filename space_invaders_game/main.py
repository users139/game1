import pygame
import sys
import os
import random
from player import Player
from bullet import Bullet
from enemy import Enemy

pygame.init()
# pygame.mixer.init() # For sounds later

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders by Jules")

current_dir = os.path.dirname(os.path.abspath(__file__))
assets_path = os.path.join(current_dir, "assets")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0) # For game over message
# ... other colors ...

clock = pygame.time.Clock()
FPS = 60

score = 0
player_lives = 3 # Initialize player lives

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y) # Default for score
    if y == screen_height / 2 or y == screen_height / 4 or y == screen_height * 3/4 : # Center for game over messages
         text_rect.center = (x,y)
    surf.blit(text_surface, text_rect)

player = Player(screen_width, screen_height, assets_path)
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

all_sprites.add(player)

# Enemy properties
enemy_rows = 3
enemy_cols = 8
enemy_start_x = 50
enemy_start_y = 50
enemy_spacing_x = 70
enemy_spacing_y = 50
enemy_points = 10
enemy_speed_x = 1 # Slowed down for balance
enemy_speed_y_drop = 10
enemy_direction = 1
last_enemy_shoot_time = pygame.time.get_ticks()
enemy_shoot_delay = 1000 # ms

def spawn_enemies():
    # enemies.empty() # This was causing all_sprites to lose enemies if called mid-game without care
    # all_sprites.remove(enemies.sprites()) 
    # Correct way to clear enemies for a new wave:
    for enemy in enemies: # Remove from all groups
        enemy.kill()

    for row in range(enemy_rows):
        for col in range(enemy_cols):
            x = enemy_start_x + col * enemy_spacing_x
            y = enemy_start_y + row * enemy_spacing_y
            enemy = Enemy(x, y, "type_A", assets_path)
            all_sprites.add(enemy)
            enemies.add(enemy)

spawn_enemies() # Initial spawn

game_over = False # Game state flag

running = True
while running:
    if game_over:
        screen.fill(BLACK)
        draw_text(screen, "GAME OVER", 64, screen_width / 2, screen_height / 4, RED)
        draw_text(screen, f"Final Score: {score}", 22, screen_width / 2, screen_height / 2, WHITE)
        draw_text(screen, "Press R to Restart or Q to Quit", 22, screen_width / 2, screen_height * 3/4, WHITE)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_r:
                    # Reset game state
                    game_over = False
                    score = 0
                    player_lives = 3
                    player.unhide() 
                    player.rect.centerx = player.initial_x 
                    player.rect.bottom = player.initial_y
                    
                    # Clear old bullets and enemies thoroughly
                    for bullet_sprite in bullets: bullet_sprite.kill()
                    for e_bullet_sprite in enemy_bullets: e_bullet_sprite.kill()
                    # spawn_enemies() will clear and re-add enemies to all_sprites and enemies group
                    
                    all_sprites.empty() # Clear all_sprites
                    all_sprites.add(player) # Re-add player
                    spawn_enemies() # Respawn enemies
                    enemy_direction = 1 
        clock.tick(FPS) # Keep clock ticking for event handling responsiveness
        continue 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = player.shoot()
                if bullet:
                    all_sprites.add(bullet)
                    bullets.add(bullet)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()

    # --- Enemy Movement ---
    # move_sideways = True # Not needed
    drop_down = False
    if enemies.sprites(): 
        for enemy_sprite in enemies:
            # enemy_sprite.rect.x += enemy_speed_x * enemy_direction # Original position for movement
            # This was a bug, movement should be applied after checking for drop
            if enemy_sprite.rect.right + (enemy_speed_x * enemy_direction) > screen_width or \
               enemy_sprite.rect.left + (enemy_speed_x * enemy_direction) < 0:
                drop_down = True
                break # Found one enemy that would go off screen
        
        if drop_down:
            enemy_direction *= -1
            for enemy_sprite in enemies:
                enemy_sprite.rect.y += enemy_speed_y_drop
        
        # Apply horizontal movement after checking/applying vertical drop
        for enemy_sprite in enemies:
            enemy_sprite.rect.x += enemy_speed_x * enemy_direction
    
    else: 
        spawn_enemies() 

    # --- Enemy Shooting ---
    now = pygame.time.get_ticks()
    if now - last_enemy_shoot_time > enemy_shoot_delay:
        if enemies.sprites():
            last_enemy_shoot_time = now
            random_enemy = random.choice(enemies.sprites())
            enemy_bullet = random_enemy.shoot()
            all_sprites.add(enemy_bullet)
            enemy_bullets.add(enemy_bullet)

    all_sprites.update() 

    # --- Collision Detection ---
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for hit_bullet, hit_enemies_list in hits.items():
        for _ in hit_enemies_list:
            score += enemy_points

    if not player.hidden: 
        player_hits = pygame.sprite.spritecollide(player, enemy_bullets, True) 
        if player_hits:
            player_lives -= 1
            player.hide() 
            if player_lives <= 0:
                game_over = True 

    # --- Drawing ---
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, f"Score: {score}", 18, screen_width / 2, 10, WHITE)
    draw_text(screen, f"Lives: {player_lives}", 18, 60, 10, WHITE) 

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
