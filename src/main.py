import pygame
import sys
from src.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WHITE,
    BUTTON_WIDTH, BUTTON_HEIGHT
)
from src.ui.button import Button
from src.ui.level_select import LevelSelect
from src.game.level import Level
from src.game.levels_data import LEVEL_NAMES, LEVEL_DESCRIPTIONS

class GameState:
    MAIN_MENU = "main_menu"
    LEVEL_SELECT = "level_select"
    PLAYING = "playing"

def main():
    
    pygame.init()
    
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Строитель дорог")

    
    start_button = Button(
        WINDOW_WIDTH//2 - BUTTON_WIDTH//2,
        WINDOW_HEIGHT//2 - BUTTON_HEIGHT - 25,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        "Начать"
    )
    
    exit_button = Button(
        WINDOW_WIDTH//2 - BUTTON_WIDTH//2,
        WINDOW_HEIGHT//2 + 25,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        "Выйти"
    )

    
    level_select = LevelSelect(screen)
    
    
    current_state = GameState.MAIN_MENU
    current_level = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if current_state == GameState.MAIN_MENU:
                if start_button.handle_event(event):
                    current_state = GameState.LEVEL_SELECT
                elif exit_button.handle_event(event):
                    running = False

            elif current_state == GameState.LEVEL_SELECT:
                result = level_select.handle_event(event)
                if result == "back":
                    current_state = GameState.MAIN_MENU
                elif result == "level_selected":
                    selected_level = level_select.get_selected_level()
                    if selected_level is not None:
                        
                        current_level = Level(selected_level, WINDOW_WIDTH, WINDOW_HEIGHT)
                        current_state = GameState.PLAYING

            elif current_state == GameState.PLAYING:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  
                        current_level.handle_click(event.pos)
                    elif event.button == 3:  
                        
                        current_state = GameState.LEVEL_SELECT
                        current_level = None

       
        if current_state == GameState.MAIN_MENU:
            screen.fill(WHITE)
            start_button.draw(screen)
            exit_button.draw(screen)
        elif current_state == GameState.LEVEL_SELECT:
            level_select.draw()
        elif current_state == GameState.PLAYING:
            screen.fill(WHITE)
            current_level.draw(screen)
            
            
            font = pygame.font.Font(None, 24)
            hint1 = font.render("ПКМ - вернуться в меню", True, (0, 0, 0))
            hint2 = font.render("ЛКМ - соединить города", True, (0, 0, 0))
            screen.blit(hint1, (WINDOW_WIDTH - hint1.get_width() - 10, WINDOW_HEIGHT - 50))
            screen.blit(hint2, (WINDOW_WIDTH - hint2.get_width() - 10, WINDOW_HEIGHT - 25))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 