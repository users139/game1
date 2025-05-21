import pygame
from snake import Snake
from food import Food
import os

pygame.init()
pygame.mixer.init()

try:
    eat_sound_path = os.path.join(os.path.dirname(__file__), 'eat_sound.wav')
    game_over_sound_path = os.path.join(os.path.dirname(__file__), 'game_over_sound.wav')
    eat_sound = pygame.mixer.Sound(eat_sound_path)
    game_over_sound = pygame.mixer.Sound(game_over_sound_path)
    sounds_loaded = True
except pygame.error as e:
    print(f"Warning: Could not load sound files (eat_sound.wav, game_over_sound.wav): {e}")
    print("Please ensure 'eat_sound.wav' and 'game_over_sound.wav' are in the same directory as main.py")
    eat_sound = None
    game_over_sound = None
    sounds_loaded = False

BACKGROUND_COLOR = (0, 0, 50)
WHITE = (255, 255, 255)
RED = (213, 50, 80)
BLUE = (50, 153, 213)

screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game by Jules")

font_style = pygame.font.SysFont(None, 30)
message_font = pygame.font.SysFont(None, 50)
instruction_font = pygame.font.SysFont(None, 25)

snake_block_size = 10
snake_speed = 15
clock = pygame.time.Clock()

def display_score(score):
    value = font_style.render("Your Score: " + str(score), True, WHITE)
    screen.blit(value, [0, 0])

def display_message(msg, color, y_offset=0, font=None):
    if font is None:
        font = message_font
    mesg = font.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(screen_width / 2, screen_height / 2 + y_offset))
    screen.blit(mesg, mesg_rect)

def start_screen():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                intro = False
        screen.fill(BACKGROUND_COLOR)
        display_message("Welcome to Snake!", WHITE, y_offset=-50)
        display_message("Use Arrow Keys to Move", WHITE, y_offset=0, font=instruction_font)
        display_message("Press any key to start", WHITE, y_offset=50, font=instruction_font)
        pygame.display.update()
        clock.tick(15)

def game_loop():
    game_over = False
    game_close = False

    snake = Snake(screen_width, screen_height, snake_block_size)
    food = Food(screen_width, screen_height, snake_block_size)
    food.respawn(snake.body) # Initial food spawn, passing snake's current body

    score = 0

    while not game_over:
        while game_close:
            screen.fill(BACKGROUND_COLOR)
            display_message("You Lost!", RED, y_offset=-50)
            display_message("Press Q-Quit or C-Play Again", WHITE, y_offset=0, font=instruction_font)
            display_score(score)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")
                elif event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")

        snake.move()

        if snake.check_collision_with_wall() or snake.check_collision_with_self():
            if sounds_loaded and game_over_sound:
                game_over_sound.play()
            game_close = True

        if snake.x == food.x and snake.y == food.y:
            if sounds_loaded and eat_sound:
                eat_sound.play()
            food.respawn(snake.body) # Pass snake's body when respawning
            snake.grow()
            score += 1

        screen.fill(BACKGROUND_COLOR)
        food.draw(screen)
        snake.draw(screen)
        display_score(score)
        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

start_screen()
game_loop()
