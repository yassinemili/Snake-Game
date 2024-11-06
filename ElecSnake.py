"Game File"
import pygame, sys, random

# Set Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# Initialize Pygame and check for errors
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initializing game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialized')

# Set up full-screen window
frame_size_x, frame_size_y = pygame.display.Info().current_w, pygame.display.Info().current_h
pygame.display.set_caption('ELEC Snake')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y), pygame.FULLSCREEN)

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
sky_blue = (135, 206, 235)

# FPS controller
fps_controller = pygame.time.Clock()

# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [80, 50], [60, 50]]
food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
food_spawn = True
direction = 'RIGHT'
change_to = direction
score = 0

# Load images for food and snake segments
food_image = pygame.image.load('./elecLogo.png')
food_image = pygame.transform.scale(food_image, (40, 40))

snake_image = pygame.image.load('./elecLogo.png')
snake_image = pygame.transform.scale(snake_image, (30, 30))

# Game Over
def game_over():
    # Using 'Consolas' for a monospaced font
    my_font = pygame.font.SysFont('Consolas', 70)
    game_over_surface_2 = my_font.render('Excited to have you join US!', True, white)
    
    # Load and scale the logo
    logo_image = pygame.image.load('./elecLogo.png')
    logo_image = pygame.transform.scale(logo_image, (200, 200))  # Adjust the size as needed
    logo_rect = logo_image.get_rect()
    
    # Position the logo between the texts (around the middle)
    logo_rect.center = (frame_size_x / 2, frame_size_y / 2)

    # Position for the rest of the message on the bottom
    game_over_rect_2 = game_over_surface_2.get_rect()
    game_over_rect_2.midtop = (frame_size_x / 2, frame_size_y / 1.5)

    game_window.fill(black)
    game_window.blit(logo_image, logo_rect)  # Display the logo between texts
    game_window.blit(game_over_surface_2, game_over_rect_2)  # Display the rest of the message
    
    # Developer info at the top-right corner
    dev_font = pygame.font.SysFont('Consolas', 20)
    dev_surface = dev_font.render('Developer: Yassine Mili', True, sky_blue)
    dev_rect = dev_surface.get_rect(topright=(frame_size_x - 10, 10))
    game_window.blit(dev_surface, dev_rect)
    
    show_score(0, red, 'Consolas', 20)
    pygame.display.flip()

    # Wait for space to restart or ESC to quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()  # Restart the game
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()  # Exit the game

# Score display
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)

def main():
    global snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score

    # Reset game variables
    snake_pos = [100, 50]
    snake_body = [[100, 50], [80, 50], [60, 50]]
    food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()  # Exit the game

        # Ensure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Move the snake
        if direction == 'UP':
            snake_pos[1] -= 20
        if direction == 'DOWN':
            snake_pos[1] += 20
        if direction == 'LEFT':
            snake_pos[0] -= 20
        if direction == 'RIGHT':
            snake_pos[0] += 20

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if abs(snake_pos[0] - food_pos[0]) < 20 and abs(snake_pos[1] - food_pos[1]) < 20:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # Spawn food on the screen
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
        food_spawn = True

        # Draw game graphics
        game_window.fill(black)
        
        # Draw each snake segment with gaps
        for pos in snake_body:
            game_window.blit(snake_image, (pos[0], pos[1]))

        # Draw the food
        game_window.blit(food_image, (food_pos[0], food_pos[1]))

        # Game Over conditions
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10:
            game_over()
        if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
            game_over()
        for block in snake_body[1:]:
            if snake_pos == block:
                game_over()

        show_score(1, white, 'Consolas', 20)
        pygame.display.update()
        fps_controller.tick(difficulty)

# Start the game
main()
