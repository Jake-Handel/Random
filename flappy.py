import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_SIZE = 30
PIPE_WIDTH = 80
BIRD_COLOR = (255, 255, 0)  # Yellow
PIPE_COLOR = (0, 255, 0)    # Green
GROUND_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (135, 206, 235)  # Sky Blue

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Codey Bird")

# Game clock
clock = pygame.time.Clock()

# Bird properties
bird_x = 50
bird_y = 300
bird_velocity = 0
gravity = 0.5
flap_strength = -10

# Pipe properties
pipe_velocity = -3
pipe_frequency = 1600  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency

# Score
score = 0
font = pygame.font.Font(None, 36)

# Function to create pipes
def create_pipe():
    pipe_x = SCREEN_WIDTH
    pipe_height = random.randint(100, 300)
    gap_size = random.randint(150,250)
    top_pipe = pygame.Rect(pipe_x, 0, PIPE_WIDTH, pipe_height)
    bottom_pipe = pygame.Rect(pipe_x, pipe_height + gap_size, PIPE_WIDTH, SCREEN_HEIGHT - pipe_height - gap_size)
    return top_pipe, bottom_pipe

# Initial pipes
pipes = []
pipes.append(create_pipe())

# Function to make the bird flap
def flap():
    global bird_velocity
    bird_velocity = flap_strength

# Scoring function
def update_score():
    global score
    for pipe in pipes:
        if pipe[0].x + PIPE_WIDTH // 2 == bird_x:
               print(score)
               pass
        pass
   

# Main game loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flap()
    
    # Bird movement
    bird_velocity += gravity
    bird_y += bird_velocity
    
    # Draw bird
    bird_rect = pygame.Rect(bird_x, bird_y, BIRD_SIZE, BIRD_SIZE)
    pygame.draw.rect(screen, BIRD_COLOR, bird_rect)
    
    # Draw ground
    ground_rect_top = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT/50)
    ground_rect_bottom = pygame.Rect(0, 590, SCREEN_WIDTH, SCREEN_HEIGHT/50)
    pygame.draw.rect(screen, GROUND_COLOR, ground_rect_top)
    pygame.draw.rect(screen, GROUND_COLOR, ground_rect_bottom)
    
    # Pipe movement and generation
    current_time = pygame.time.get_ticks()
    if current_time - last_pipe > pipe_frequency:
        pipes.append(create_pipe())
        last_pipe = current_time
    
    for pipe in pipes:
        top_pipe, bottom_pipe = pipe
        top_pipe.x += pipe_velocity
        bottom_pipe.x += pipe_velocity
        pygame.draw.rect(screen, PIPE_COLOR, top_pipe)
        pygame.draw.rect(screen, PIPE_COLOR, bottom_pipe)
    
    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if pipe[0].x + PIPE_WIDTH > 0]
    
    # Update score
    update_score()
    
    # Display score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    # Collision detection
    for pipe in pipes:
        if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]) or bird_rect.colliderect(ground_rect_top) or bird_rect.colliderect(ground_rect_bottom):
            running = False
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

