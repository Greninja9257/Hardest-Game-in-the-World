import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Hardest Game Ever!!!!")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define player and enemy
player_width = 20
player_height = 20
player_x = window_width // 2
player_y = window_height // 2
player_speed = 6
player_health = 200
player_max_health = 200

enemy_width = 30
enemy_height = 30
enemies = []
for i in range(12):
    enemy_x = random.randint(0, window_width - enemy_width)
    enemy_y = random.randint(0, window_height - enemy_height)
    enemy_speed = random.randint(1, 3)
    enemy_attack_timer = 80  # 3 seconds (180 frames at 60 FPS)
    enemies.append({"x": enemy_x, "y": enemy_y, "speed": enemy_speed, "attack_timer": enemy_attack_timer})

# Define falling objects
falling_objects = []
for i in range(20):
    obj_x = random.randint(0, window_width)
    obj_y = 0
    obj_speed = random.randint(1, 3)
    falling_objects.append({"x": obj_x, "y": obj_y, "speed": obj_speed})

# Game loop
running = True
game_over = False
clock = pygame.time.Clock()  # Create a clock object

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player
    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

    # Keep player within window borders
    player_x = max(0, min(player_x, window_width - player_width))
    player_y = max(0, min(player_y, window_height - player_height))

    # Move the enemies towards the player
    for enemy in enemies:
        enemy_x = enemy["x"]
        enemy_y = enemy["y"]
        enemy_speed = enemy["speed"]
        enemy_attack_timer = enemy["attack_timer"]

        # Calculate the direction towards the player
        dx = player_x - enemy_x
        dy = player_y - enemy_y
        distance = max(abs(dx), abs(dy))
        if distance != 0:
            dx /= distance
            dy /= distance

        # Move the enemy towards the player
        enemy["x"] += dx * enemy_speed
        enemy["y"] += dy * enemy_speed

        # Check for collision with enemy
        if (
            enemy_x <= player_x <= enemy_x + enemy_width
            and enemy_y <= player_y <= enemy_y + enemy_height
        ):
            if enemy_attack_timer <= 0:
                player_health -= 5
                enemy_attack_timer = 80  # Reset attack timer

        # Decrement enemy attack timer
        enemy["attack_timer"] -= 1

    # Move the falling objects downwards
    for obj in falling_objects:
        obj["y"] += obj["speed"]
        if obj["y"] > window_height:
            obj["x"] = random.randint(0, window_width)
            obj["y"] = 0

        # Check for collision with falling object
        if (
            obj["x"] <= player_x <= obj["x"] + 10
            and obj["y"] <= player_y <= obj["y"] + 10
        ):
            player_health -= 20  # Increase health loss from falling object collision

    # Check if player has lost all health
    if player_health <= 0:
        game_over = True

    # Clear the window
    window.fill(WHITE)

    # Draw the player and enemies
    pygame.draw.rect(window, BLACK, (player_x, player_y, player_width, player_height))
    for enemy in enemies:
        pygame.draw.rect(window, RED, (enemy["x"], enemy["y"], enemy_width, enemy_height))

    # Draw the falling objects
    for obj in falling_objects:
        pygame.draw.rect(window, BLACK, (obj["x"], obj["y"], 10, 10))

    # Draw the player's health bar
    health_bar_width = int(player_health / player_max_health * 200)
    pygame.draw.rect(window, RED, (10, 10, 200, 20))
    pygame.draw.rect(window, GREEN, (10, 10, health_bar_width, 20))

    # Draw game over message if player has lost all health
    if game_over:
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (window_width // 2, window_height // 2)
        window.blit(text, text_rect)

    # Update the display
    pygame.display.update()

    # Tick the clock
    clock.tick(60)  # Limit the frame rate to 60 FPS

# Quit Pygame
pygame.quit()