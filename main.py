import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up paddles and ball
paddle_width = 10
paddle_height = 100
paddle_speed = 6
paddle1_x = 20
paddle1_y = screen_height // 2 - paddle_height // 2
paddle2_x = screen_width - 20 - paddle_width
paddle2_y = screen_height // 2 - paddle_height // 2

ball_radius = 10
ball_speed = 5  # Initial ball speed
ball_speed_x = ball_speed
ball_speed_y = ball_speed
ball_x = screen_width // 2
ball_y = screen_height // 2

# Initialize scores
score_player1 = 0
score_player2 = 0

# Set up font for displaying scores
font = pygame.font.Font(None, 36)

# Difficulty levels
difficulty_levels = {
    "Easy": {"paddle_speed": 4, "ball_speed": 5},
    "Medium": {"paddle_speed": 5.9, "ball_speed": 7},
    "Hard": {"paddle_speed": 8, "ball_speed": 9}
}

current_difficulty = "Medium"  # Default difficulty level

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Change difficulty level
            if event.key == pygame.K_1:
                current_difficulty = "Easy"
            elif event.key == pygame.K_2:
                current_difficulty = "Medium"
            elif event.key == pygame.K_3:
                current_difficulty = "Hard"

    # Move player's paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle1_y < screen_height - paddle_height:
        paddle1_y += paddle_speed

    # Move AI's paddle to track the ball
    if ball_y < paddle2_y + paddle_height // 2:
        paddle2_y -= difficulty_levels[current_difficulty]["paddle_speed"]
    elif ball_y > paddle2_y + paddle_height // 2:
        paddle2_y += difficulty_levels[current_difficulty]["paddle_speed"]

    # Move ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with top and bottom walls
    if ball_y <= 0 or ball_y >= screen_height - ball_radius:
        ball_speed_y *= -1

    # Ball collision with paddles
    if (paddle1_x <= ball_x <= paddle1_x + paddle_width and
            paddle1_y <= ball_y <= paddle1_y + paddle_height):
        ball_speed_x *= -1

    if (paddle2_x <= ball_x <= paddle2_x + paddle_width and
            paddle2_y <= ball_y <= paddle2_y + paddle_height):
        ball_speed_x *= -1

    # Ball out of bounds
    if ball_x < 0:
        ball_x = screen_width // 2
        ball_y = screen_height // 2
        ball_speed_x = difficulty_levels[current_difficulty]["ball_speed"]*1.5
        ball_speed_y = difficulty_levels[current_difficulty]["ball_speed"]
        score_player2 += 1
    elif ball_x > screen_width:
        ball_x = screen_width // 2
        ball_y = screen_height // 2
        ball_speed_x = difficulty_levels[current_difficulty]["ball_speed"]
        ball_speed_y = difficulty_levels[current_difficulty]["ball_speed"]
        score_player1 += 1

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, (paddle1_x, paddle1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, WHITE, (paddle2_x, paddle2_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)

    # Display scores and current difficulty level
    text_surface_player1 = font.render("Player : " + str(score_player1), True, WHITE)
    text_surface_player2 = font.render("Computer : " + str(score_player2), True, WHITE)
    text_surface_difficulty = font.render("Difficulty: " + current_difficulty, True, WHITE)
    screen.blit(text_surface_player1, (20, 20))
    screen.blit(text_surface_player2, (screen_width - 160, 20))
    screen.blit(text_surface_difficulty, (20, screen_height - 40))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
