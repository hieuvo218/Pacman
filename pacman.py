import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Enemy")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Player
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# Bullets
bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullets = []

# Enemies
enemy_width = 50
enemy_height = 50
enemy_speed = 5
enemies = []

# Score
score = 0
font = pygame.font.SysFont(None, 30)

# Function to draw text on the screen
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Fire a bullet
                bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])

    # Handle player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Move bullets
    bullets = [[bx, by - bullet_speed] for bx, by in bullets]

    # Move enemies
    enemies = [[ex, ey + enemy_speed] for ex, ey in enemies]

    # Check for collisions between bullets and enemies
    for bullet in bullets:
        for enemy in enemies:
            if (
                enemy[0] < bullet[0] < enemy[0] + enemy_width
                and enemy[1] < bullet[1] < enemy[1] + enemy_height
            ):
                # Bullet hit an enemy
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1

    # Check for collisions between player and enemies
    for enemy in enemies:
        if (
            player_x < enemy[0] + enemy_width
            and player_x + player_width > enemy[0]
            and player_y < enemy[1] + enemy_height
            and player_y + player_height > enemy[1]
        ):
            # Player collided with an enemy
            pygame.quit()
            sys.exit()

    # Remove bullets that are off the screen
    bullets = [bullet for bullet in bullets if bullet[1] > 0]

    # Generate new enemies at random intervals
    if random.randint(1, 75) == 1:
        enemies.append([random.randint(0, WIDTH - enemy_width), 0])

    # Update the display
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (player_x, player_y, player_width, player_height))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, RED, (bullet[0], bullet[1], bullet_width, bullet_height))

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_width, enemy_height))

    # Draw the score
    draw_text(f"Score: {score}", RED, 10, 10)

    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)
