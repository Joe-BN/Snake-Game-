import pygame
import sys

DARK_GREY = (14, 9, 8)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)

SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 800

def settings_screen(screen, font, large_font):
    clock = pygame.time.Clock()
    selected_mode = 'single'
    selected_difficulty = 'easy'
    
    # Positions defination
    y =100 # variable to reposiotion height (item y-possition)

    title_pos = (SCREEN_WIDTH // 2, 70)
    mode_label_pos = (SCREEN_WIDTH // 2, 100 + y)
    single_pos = (SCREEN_WIDTH // 2 - 50, 150 + y)
    multi_pos = (SCREEN_WIDTH // 2 - 50, 200 + y)
    diff_label_pos = (SCREEN_WIDTH // 2, 250 + y)
    easy_pos = (SCREEN_WIDTH // 2 - 50, 300 + y)
    medium_pos = (SCREEN_WIDTH // 2 - 50, 350 + y)
    hard_pos = (SCREEN_WIDTH // 2 - 50, 400 + y)
    asian_pos = (SCREEN_WIDTH // 2 - 50, 450 + y) 
    start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 500 + 40 + y, 100, 50)
    
    # Clickable areas inputs
    radio_size = 20
    single_rect = pygame.Rect(single_pos[0] - 10, single_pos[1] - 10, radio_size, radio_size)
    multi_rect = pygame.Rect(multi_pos[0] - 10, multi_pos[1] - 10, radio_size, radio_size)
    easy_rect = pygame.Rect(easy_pos[0] - 10, easy_pos[1] - 10, radio_size, radio_size)
    medium_rect = pygame.Rect(medium_pos[0] - 10, medium_pos[1] - 10, radio_size, radio_size)
    hard_rect = pygame.Rect(hard_pos[0] - 10, hard_pos[1] - 10, radio_size, radio_size)
    asian_rect = pygame.Rect(asian_pos[0] - 10, asian_pos[1] - 10, radio_size, radio_size)  # Fixed
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Player mode
                if single_rect.collidepoint(mouse_pos):
                    selected_mode = 'single'
                elif multi_rect.collidepoint(mouse_pos):
                    selected_mode = 'multi'
                
                # difficulty
                elif easy_rect.collidepoint(mouse_pos):
                    selected_difficulty = 'easy'
                elif medium_rect.collidepoint(mouse_pos):
                    selected_difficulty = 'medium'
                elif hard_rect.collidepoint(mouse_pos):
                    selected_difficulty = 'hard'
                elif asian_rect.collidepoint(mouse_pos):
                    selected_difficulty = 'asian'
                elif start_rect.collidepoint(mouse_pos):
                    return selected_mode, selected_difficulty
        
        screen.fill(DARK_GREY)
        title_text = large_font.render("Game Settings", True, WHITE)
        screen.blit(title_text, (title_pos[0] - title_text.get_width() // 2, title_pos[1]))
        mode_label = font.render("Game Mode:", True, WHITE)
        screen.blit(mode_label, (mode_label_pos[0] - mode_label.get_width() // 2, mode_label_pos[1]))
        
        # Mode radio buttons
        pygame.draw.circle(screen, WHITE, single_pos, 10, 1)
        if selected_mode == 'single':
            pygame.draw.circle(screen, GREEN, single_pos, 5)
        single_label = font.render("Single Player", True, WHITE)
        screen.blit(single_label, (single_pos[0] + 30, single_pos[1] - single_label.get_height() // 2))
        
        pygame.draw.circle(screen, WHITE, multi_pos, 10, 1)
        if selected_mode == 'multi':
            pygame.draw.circle(screen, GREEN, multi_pos, 5)
        multi_label = font.render("Multiplayer", True, WHITE)
        screen.blit(multi_label, (multi_pos[0] + 30, multi_pos[1] - multi_label.get_height() // 2))
        
        # Difficulty radio buttons
        diff_label = font.render("Difficulty:", True, WHITE)
        screen.blit(diff_label, (diff_label_pos[0] - diff_label.get_width() // 2, diff_label_pos[1]))
        
        pygame.draw.circle(screen, WHITE, easy_pos, 10, 1)
        if selected_difficulty == 'easy':
            pygame.draw.circle(screen, GREEN, easy_pos, 5)
        easy_label = font.render("Easy", True, WHITE)
        screen.blit(easy_label, (easy_pos[0] + 30, easy_pos[1] - easy_label.get_height() // 2))
        
        pygame.draw.circle(screen, WHITE, medium_pos, 10, 1)
        if selected_difficulty == 'medium':
            pygame.draw.circle(screen, GREEN, medium_pos, 5)
        medium_label = font.render("Medium", True, WHITE)
        screen.blit(medium_label, (medium_pos[0] + 30, medium_pos[1] - medium_label.get_height() // 2))
        
        pygame.draw.circle(screen, WHITE, hard_pos, 10, 1)
        if selected_difficulty == 'hard':
            pygame.draw.circle(screen, GREEN, hard_pos, 5)
        hard_label = font.render("Hard", True, WHITE)
        screen.blit(hard_label, (hard_pos[0] + 30, hard_pos[1] - hard_label.get_height() // 2))
        
        # Fixed Asian difficulty drawing
        pygame.draw.circle(screen, WHITE, asian_pos, 10, 1)  # Use asian_pos
        if selected_difficulty == 'asian':
            pygame.draw.circle(screen, GREEN, asian_pos, 5)  # Use asian_pos
        asian_label = font.render("Asian", True, WHITE)
        screen.blit(asian_label, (asian_pos[0] + 10, asian_pos[1] - asian_label.get_height() // 2))  # Use asian_pos
        
        # Start button
        pygame.draw.rect(screen, BLUE, start_rect)
        start_text = font.render("Start", True, WHITE)
        start_text_pos = (start_rect.centerx - start_text.get_width() // 2,
                          start_rect.centery - start_text.get_height() // 2)
        screen.blit(start_text, start_text_pos)
        
        pygame.display.flip()
        clock.tick(60)

# Keep the main function for standalone testing (optional)
def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 30)

    large_font = pygame.font.SysFont(None, 50)
    mode, difficulty = settings_screen(screen, font, large_font)
    print(f"Selected Mode: {mode}, Difficulty: {difficulty}")

    pygame.quit()

if __name__ == "__main__":
    main()