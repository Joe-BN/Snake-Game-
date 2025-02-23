import pygame
import sys
import random
import time
import data as data
import util as util

def get_random_food_position(snake, game_width, game_height, cell_size):
    """Returns a random (x, y) position for food that is not on the snake."""
    cols = game_width // cell_size
    rows = game_height // cell_size
    while True:
        food_x = random.randint(0, cols - 1) * cell_size
        food_y = random.randint(0, rows - 1) * cell_size
        if (food_x, food_y) not in snake:
            return (food_x, food_y)

def main():
    pygame.init()
    data.initialize_db()

    # --- Configuration ---
    # Dimensions for game area and side menu.
    GAME_AREA_WIDTH = 800
    SIDE_MENU_WIDTH = 220
    TOTAL_WIDTH = GAME_AREA_WIDTH + SIDE_MENU_WIDTH
    HEIGHT = 800

    # Grid/Cell size
    cell_size = 20

    # Create game window
    screen = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    # Define colors
    BLACK     = (0, 0, 0)
    GREY = (183,183,183)
    # GREY      = (200, 200, 200)
    DARK_GREY = (14, 9, 8) # a bit red  :)
    GRID_COLOUR = (85, 96, 97)
    WHITE     = (255, 255, 255)
    GREEN     = (0, 200, 0)
    RED       = (255, 0, 0)
    BLUE      = (0, 0, 255)


    # Set up font
    font_size = 25
    font = pygame.font.SysFont(None, font_size)

    # Difficulty settings
    # The move_interval (in milliseconds) determines how fast the snake moves.
    difficulty = 2

    move_interval = {
        1: 150, 
        2: 100,
        3: 70,
        4: 40,
    }

    clock = pygame.time.Clock()

    def reset_game():
        nonlocal snake, direction, score, food, game_state, last_move_time

        # Start snake in the middle of the game area (aligned to the grid).
        start_x = (GAME_AREA_WIDTH // cell_size // 2) * cell_size
        start_y = (HEIGHT // cell_size // 2) * cell_size

        # Snake is a list of (x, y) tuples; starting with 3 segments.
        snake = [
            (start_x, start_y),
            (start_x - cell_size, start_y),
            (start_x - 2 * cell_size, start_y)
        ]


        direction = (cell_size, 0)  # Initially direction

        score = 0
        food = get_random_food_position(snake, GAME_AREA_WIDTH, HEIGHT, cell_size)
        game_state = 'playing'
        last_move_time = pygame.time.get_ticks()


    # Initial Game Variables
    snake = []
    direction = (cell_size, 0)
    score = 0 # tracking  score (map this to a database and get the value o start) !!!! also display high score when playing
    food = None
    game_state = 'playing' # keep a record of the event state (playing and gameover)
    last_move_time = pygame.time.get_ticks()
    reset_game()  # Set initial game state.


    # Game Loop
    while True:
        # Event Handling functionality
        for event in pygame.event.get(): # listen for inputs or actions
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Direction control (prevent reversing)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if direction != (0, cell_size):
                        direction = (0, -cell_size)
                elif event.key == pygame.K_DOWN:
                    if direction != (0, -cell_size):
                        direction = (0, cell_size)
                elif event.key == pygame.K_LEFT:
                    if direction != (cell_size, 0):
                        direction = (-cell_size, 0)
                elif event.key == pygame.K_RIGHT:
                    if direction != (-cell_size, 0):
                        direction = (cell_size, 0)

                # Change difficulty with number keys.
                elif event.key == pygame.K_1:
                    difficulty = 1
                elif event.key == pygame.K_2:
                    difficulty = 2
                elif event.key == pygame.K_3:
                    difficulty = 3
                elif event.key == pygame.K_4:
                    difficulty = 4


                # Restart the game if over.
                if game_state == 'game_over' and event.key == pygame.K_r:
                    reset_game()


        # Game Update
        if game_state == 'playing':
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time > move_interval[difficulty]:

                # Calculate new head position based on current direction.
                new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

                # Check for collision with walls.
                if (new_head[0] < 0 or new_head[0] >= GAME_AREA_WIDTH or
                    new_head[1] < 0 or new_head[1] >= HEIGHT):
                    game_state = 'game_over'

                # Check for collision with self.
                elif new_head in snake:
                    game_state = 'game_over'
                else:
                    # Insert new head into the snake.
                    snake.insert(0, new_head)

                    # Check if food is eaten.
                    if new_head == food:
                        score += 1
                        # play sound when eat
                        util.play_sound(1)

                        food = get_random_food_position(snake, GAME_AREA_WIDTH, HEIGHT, cell_size)
                    else:
                        # Remove the tail segment if no food eaten.
                        snake.pop()
                last_move_time = current_time

        # Drawing
        screen.fill(BLACK)

        # Draw game area background.
        pygame.draw.rect(screen, GREY, (0, 0, GAME_AREA_WIDTH, HEIGHT))

        # Draw the snake.
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], cell_size, cell_size))

        # Draw the food.
        pygame.draw.rect(screen, RED, (food[0], food[1], cell_size, cell_size))

        # Draw grid lines for clarity.
        for x in range(0, GAME_AREA_WIDTH, cell_size):
            pygame.draw.line(screen, GRID_COLOUR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, cell_size):
            pygame.draw.line(screen, GRID_COLOUR, (0, y), (GAME_AREA_WIDTH, y))

        # Draw side menu background.
        pygame.draw.rect(screen, DARK_GREY, (GAME_AREA_WIDTH, 0, SIDE_MENU_WIDTH, HEIGHT))


        # Render and display score, difficulty, and instructions.
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (GAME_AREA_WIDTH + 10, 20))

        diff_text = font.render(f"Difficulty: {difficulty}", True, WHITE)
        screen.blit(diff_text, (GAME_AREA_WIDTH + 10, 60))

        instruct_text = font.render("Arrows to move", True, WHITE)
        screen.blit(instruct_text, (GAME_AREA_WIDTH + 10, 100))

        # enter into documentation later
        instruct_text2 = font.render("1,2,3 or 4 for diff", True, WHITE)
        screen.blit(instruct_text2, (GAME_AREA_WIDTH + 10, 140))

        score_text = font.render(f"Hight Score: {data.get_high_score()}", True, WHITE)
        screen.blit(score_text, (GAME_AREA_WIDTH + 10, 770))

           

        # Display text on game over
        if game_state == 'game_over':
            if (data.update_high_score(score)):
                over_text = font.render("NEW HIGH SCORE !!!", True, BLUE)
                screen.blit(over_text, (GAME_AREA_WIDTH + 10, 500))
                util.play_sound(3)

            else :
                util.play_sound(2)
                

            data.update_high_score(score)
        
            time.sleep(2) # small pause so that the sound plays (adjustable)

            over_text = font.render("Game Over!", True, BLUE)
            screen.blit(over_text, (GAME_AREA_WIDTH + 10, 200))

            restart_text = font.render("Press R to restart", True, BLUE)
            screen.blit(restart_text, (GAME_AREA_WIDTH + 10, 240))


        # loop game
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()