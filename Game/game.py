import pygame               # game rendering library
import sys                  # access system file paths
import random               # randomization library
import time                 # time and delay
import data        # interact with database
import util         # utility functionalities
import landing as settings  #ADD  the landing page

def get_random_food_position(snake, game_width, game_height, cell_size):
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

    # Configuration
    GAME_AREA_WIDTH = 800
    SIDE_MENU_WIDTH = 220
    TOTAL_WIDTH = GAME_AREA_WIDTH + SIDE_MENU_WIDTH
    HEIGHT = 800
    cell_size = 20

    screen = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game Pro")

    # Colors
    BLACK = (0, 0, 0)
    GREY = (183, 183, 183)
    DARK_GREY = (14, 9, 8)
    WHITE = (255, 255, 255)
    GREEN = (0, 200, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    ORANGE = ( 242, 123, 24)

    # Font
    font_size = 25
    font = pygame.font.SysFont(None, font_size)
    large_font = pygame.font.SysFont(None, 50)  # Added for settings screen title

    # Difficulty settings (will be set by settings screen)
    difficulty = 1
    mult = 1
    move_interval = {
        1: 150,
        2: 90, 
        3: 60, 
        4: 30
    }

    clock = pygame.time.Clock()

    # Game variables
    snake1 = []
    snake2 = []

    direction1 = (cell_size, 0)
    direction2 = (-cell_size, 0)

    score1 = 0
    score2 = 0

    food = None
    game_state = 'playing'
    last_move_time = 0

    def reset_game():
        nonlocal snake1, snake2, direction1, direction2, score1, score2, food, game_state, last_move_time
        start_x1 = (GAME_AREA_WIDTH // cell_size // 3) * cell_size
        start_y1 = (HEIGHT // cell_size // 2) * cell_size
        start_x2 = (2 * GAME_AREA_WIDTH // cell_size // 3) * cell_size
        start_y2 = ((HEIGHT // cell_size // 2) * cell_size) + (3 * cell_size)
        
        snake1 = [
            (start_x1, start_y1),
            (start_x1 - cell_size, start_y1), 
            (start_x1 - 2 * cell_size, start_y1)
        ]
        snake2 = [
            (start_x2, start_y2), 
            (start_x2 + cell_size, start_y2), 
            (start_x2 + 2 * cell_size, start_y2)
        ]

        direction1 = (cell_size, 0)
        direction2 = (-cell_size, 0)

        score1, score2 = 0, 0
        food = get_random_food_position(snake1 + snake2, GAME_AREA_WIDTH, HEIGHT, cell_size)
        game_state = 'playing'
        last_move_time = pygame.time.get_ticks()

        msg = "End"

    # Get settings from settings screen
    mode, difficulty_str = settings.settings_screen(screen, font, large_font)
    multiplayer = (mode == 'multi')
    difficulty_map = {
        'easy':   1, 
        'medium': 2, 
        'hard':   3, 
        'asian':  4,
    }
    difficulty = difficulty_map[difficulty_str]
    mult_map = {
        1: 1, 
        2: 2, 
        3: 4, 
        4: 8
    }
    mult = mult_map[difficulty]

    # Initialize game state
    reset_game()

    # Game Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Player 1 controls
                if event.key == pygame.K_UP and direction1 != (0, cell_size):
                    direction1 = (0, -cell_size)
                elif event.key == pygame.K_DOWN and direction1 != (0, -cell_size):
                    direction1 = (0, cell_size)
                elif event.key == pygame.K_LEFT and direction1 != (cell_size, 0):
                    direction1 = (-cell_size, 0)
                elif event.key == pygame.K_RIGHT and direction1 != (-cell_size, 0):
                    direction1 = (cell_size, 0)

                # Player 2 controls
                if multiplayer:
                    if event.key == pygame.K_w and direction2 != (0, cell_size):
                        direction2 = (0, -cell_size)
                    elif event.key == pygame.K_s and direction2 != (0, -cell_size):
                        direction2 = (0, cell_size)
                    elif event.key == pygame.K_a and direction2 != (cell_size, 0):
                        direction2 = (-cell_size, 0)
                    elif event.key == pygame.K_d and direction2 != (-cell_size, 0):
                        direction2 = (cell_size, 0)

                # Game over controls
                if game_state == 'game_over' and event.key == pygame.K_r:
                    reset_game()
                elif game_state == 'game_over' and event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        # Game Update
        if game_state == 'playing':
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time > move_interval[difficulty]:
                new_head1 = (snake1[0][0] + direction1[0], snake1[0][1] + direction1[1])
                if multiplayer:
                    new_head2 = (snake2[0][0] + direction2[0], snake2[0][1] + direction2[1])

                if (new_head2 in snake2):
                    msg = "Player 1 bit Self !"
                if (new_head2 in snake1):
                    msg = "Player 1 bit Player 2 !"

                if (new_head1 in snake1 or new_head1 in (snake2 if multiplayer else []) or
                    new_head1[0] < 0 or new_head1[0] >= GAME_AREA_WIDTH or
                    new_head1[1] < 0 or new_head1[1] >= HEIGHT):
                    game_state = 'game_over'
                else:
                    snake1.insert(0, new_head1)
                    if new_head1 == food:
                        score1 += (1 * mult)
                        food = get_random_food_position(snake1 + (snake2 if multiplayer else []), GAME_AREA_WIDTH, HEIGHT, cell_size)
                        util.play_sound(1)
                    else:
                        snake1.pop()

                if multiplayer:
                    if (new_head2 in snake2):
                        msg = "Player 2 bit Self !"
                    if (new_head2 in snake1):
                        msg = "Player 2 bit Player !"

                    if (new_head2 in snake2 or new_head2 in snake1 or
                        new_head2[0] < 0 or new_head2[0] >= GAME_AREA_WIDTH or
                        new_head2[1] < 0 or new_head2[1] >= HEIGHT):
                        game_state = 'game_over'
                    else:
                        snake2.insert(0, new_head2)
                        if new_head2 == food:
                            score2 += (1 * mult)
                            food = get_random_food_position(snake1 + snake2, GAME_AREA_WIDTH, HEIGHT, cell_size)
                            util.play_sound(1)

                        else:
                            snake2.pop()
                last_move_time = current_time

        # Drawing
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREY, (0, 0, GAME_AREA_WIDTH, HEIGHT))

        for segment in snake1:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], cell_size, cell_size))

        if multiplayer:
            for segment in snake2:
                pygame.draw.rect(screen, BLUE, (segment[0], segment[1], cell_size, cell_size))

        pygame.draw.rect(screen, RED, (food[0], food[1], cell_size, cell_size))

        # grid display
        GRID_COLOUR = (85, 96, 97)
        for x in range(0, GAME_AREA_WIDTH, cell_size):
            pygame.draw.line(screen, GRID_COLOUR, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, cell_size):
            pygame.draw.line(screen, GRID_COLOUR, (0, y), (GAME_AREA_WIDTH, y))

        pygame.draw.rect(screen, DARK_GREY, (GAME_AREA_WIDTH, 0, SIDE_MENU_WIDTH, HEIGHT))
        
        score_str = f"Score: {score1}" if not multiplayer else f"P1: {score1}  P2: {score2}"
        score_text = font.render(score_str, True, WHITE)
        screen.blit(score_text, (GAME_AREA_WIDTH + 10, 20))

        diff_text = font.render(f"Difficulty: {difficulty_str}", True, WHITE)
        screen.blit(diff_text, (GAME_AREA_WIDTH + 10, 60))

        control_text = "Arrows to move" if not multiplayer else "P1: Arrows  P2: W/A/S/D"
        instruct_text = font.render(control_text, True, WHITE)
        screen.blit(instruct_text, (GAME_AREA_WIDTH + 10, 100))


        high_score = data.get_high_score()
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (GAME_AREA_WIDTH + 10, 770))

        if game_state == 'game_over':
            if multiplayer:
                if data.update_high_score(score1) or data.update_high_score(score2):
                    over_text = font.render("NEW HIGH SCORE !!!", True, BLUE)
                    screen.blit(over_text, (GAME_AREA_WIDTH + 10, 500))

                    overlay_active = True
                    if overlay_active:
                        trophy_image = util.fetch_win()
                        if trophy_image:
                            trophy_rect = trophy_image.get_rect(center=(GAME_AREA_WIDTH // 2, HEIGHT // 2 + 50))
                            screen.blit(trophy_image, trophy_rect)
                            util.fetch_win()
                time.sleep(2)
                over_text = font.render("Game Over!", True, BLUE)
                screen.blit(over_text, (GAME_AREA_WIDTH + 10, 200))

            else:
                if data.update_high_score(score1):
                    over_text = font.render("NEW HIGH SCORE !!!", True, BLUE)
                    screen.blit(over_text, (GAME_AREA_WIDTH + 10, 500))
                                

                    overlay_active = True
                    if overlay_active:
                        trophy_image = util.fetch_win()
                        if trophy_image:
                            trophy_rect = trophy_image.get_rect(center=(GAME_AREA_WIDTH // 2, HEIGHT // 2 + 50))
                            screen.blit(trophy_image, trophy_rect)
                            util.fetch_win()
                        
                else:
                    util.play_sound(2)

                data.update_high_score(score1)
                if multiplayer: data.update_high_score(score2)
                
                time.sleep(3)
                over_text = font.render("Game Over!", True, BLUE)
                screen.blit(over_text, (GAME_AREA_WIDTH + 10, 240))
                
                # faulter = font.render(f"Fault: \n {msg}", True, BLUE)
                # screen.blit(faulter, (GAME_AREA_WIDTH + 10, 240))

            restart_text = font.render("Press Q to Quit", True, BLUE)
            screen.blit(restart_text, (GAME_AREA_WIDTH + 10, 340))

            restart_text = font.render("Press R to restart", True, BLUE)
            screen.blit(restart_text, (GAME_AREA_WIDTH + 10, 380))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()