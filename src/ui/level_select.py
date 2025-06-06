import pygame
from src.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WHITE,
    BUTTON_WIDTH, BUTTON_HEIGHT
)
from .button import Button

class LevelSelect:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.selected_level = None
        
        # Создаем кнопки для каждого уровня
        for i in range(3):
            button = Button(
                WINDOW_WIDTH//2 - BUTTON_WIDTH//2,
                WINDOW_HEIGHT//2 - BUTTON_HEIGHT + (i - 1) * (BUTTON_HEIGHT + 20),
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                f"Уровень {i + 1}"
            )
            self.buttons.append(button)
            
        # Добавляем кнопку "Назад"
        self.back_button = Button(
            WINDOW_WIDTH//2 - BUTTON_WIDTH//2,
            WINDOW_HEIGHT - BUTTON_HEIGHT - 20,  # Размещаем внизу экрана
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Назад"
        )

    def handle_event(self, event):
        # Проверяем нажатие на кнопку "Назад"
        if self.back_button.handle_event(event):
            return "back"
            
        # Проверяем нажатие на кнопки уровней
        for i, button in enumerate(self.buttons):
            if button.handle_event(event):
                self.selected_level = i + 1
                return "level_selected"
        return None

    def draw(self):
        self.screen.fill(WHITE)
        
        # Отрисовка заголовка
        font = pygame.font.Font(None, 48)
        title = font.render("Выберите уровень", True, (0, 0, 0))
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4))
        self.screen.blit(title, title_rect)
        
        # Отрисовка кнопок уровней
        for button in self.buttons:
            button.draw(self.screen)
            
        # Отрисовка кнопки "Назад"
        self.back_button.draw(self.screen)

    def get_selected_level(self):
        return self.selected_level 