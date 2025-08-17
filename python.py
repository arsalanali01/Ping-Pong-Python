import pygame #install all the required files
import sys
from pygame.locals import QUIT, K_w, K_s, K_UP, K_DOWN

# Basic setup

pygame.init()
WIDTH, HEIGHT = 800, 500          # Window size (comfortable widescreen)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60                           # Frames per second (smoothness)
CLOCK = pygame.time.Clock()

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game objects (rectangles)
PADDLE_W, PADDLE_H = 12, 90
BALL_SIZE = 14

# Start paddles near left/right edges, centered vertically
left_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)
right_paddle = pygame.Rect(WIDTH - 30 - PADDLE_W, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)

# Ball starts at center
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Speeds & scores
PADDLE_SPEED = 6
BALL_SPEED_X = 5     # Horizontal speed (positive = moving right)
BALL_SPEED_Y = 4     # Vertical speed  (positive = moving down)

left_score = 0
right_score = 0
SCORE_FONT = pygame.font.SysFont("arial", 36)

# Reset ball to center after a point
def reset_ball(scored_to_right: bool):
    """Place the ball back in the middle and aim it toward the player who lost the last point."""
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.center = (WIDTH // 2, HEIGHT // 2)

    # Send ball toward the player who just got scored on
    BALL_SPEED_X = 5 if scored_to_right else -5
    BALL_SPEED_Y = 4

# Input handling for paddles
def handle_input():
    keys = pygame.key.get_pressed()

    # Left paddle: W (up) / S (down)
    if keys[K_w]:
        left_paddle.y -= PADDLE_SPEED
    if keys[K_s]:
        left_paddle.y += PADDLE_SPEED

    # Right paddle: Up / Down arrows
    if keys[K_UP]:
        right_paddle.y -= PADDLE_SPEED
    if keys[K_DOWN]:
        right_paddle.y += PADDLE_SPEED

    # Keep paddles on screen
    left_paddle.y = max(0, min(HEIGHT - PADDLE_H, left_paddle.y))
    right_paddle.y = max(0, min(HEIGHT - PADDLE_H, right_paddle.y))

# Ball movement & collisions
def update_ball():
    global BALL_SPEED_X, BALL_SPEED_Y, left_score, right_score

    # Move ball
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # Bounce on top/bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y *= -1

    # Bounce on paddles (simple rectangle collision)
    if ball.colliderect(left_paddle) and BALL_SPEED_X < 0:
        BALL_SPEED_X *= -1
    if ball.colliderect(right_paddle) and BALL_SPEED_X > 0:
        BALL_SPEED_X *= -1

    # Check if someone scored (ball goes past left or right edge)
    if ball.left <= 0:
        right_score += 1
        reset_ball(scored_to_right=False)  # Point to right player
    if ball.right >= WIDTH:
        left_score += 1
        reset_ball(scored_to_right=True)   # Point to left player

# Drawing everything
def draw():
    # Background
    WIN.fill(BLACK)

    # Center line (just for style)
    for y in range(0, HEIGHT, 20):
        pygame.draw.rect(WIN, WHITE, (WIDTH // 2 - 2, y, 4, 10))

    # Paddles and ball
    pygame.draw.rect(WIN, WHITE, left_paddle)
    pygame.draw.rect(WIN, WHITE, right_paddle)
    pygame.draw.ellipse(WIN, WHITE, ball)

    # Scores (left on left side, right on right side)
    left_text = SCORE_FONT.render(str(left_score), True, WHITE)
    right_text = SCORE_FONT.render(str(right_score), True, WHITE)
    WIN.blit(left_text, (WIDTH // 4 - left_text.get_width() // 2, 20))
    WIN.blit(right_text, (3 * WIDTH // 4 - right_text.get_width() // 2, 20))

    pygame.display.flip()

# Main game loop
def main():
    while True:
        # Handle window close
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        handle_input()
        update_ball()
        draw()

        CLOCK.tick(FPS)

if __name__ == "__main__":
    main()
