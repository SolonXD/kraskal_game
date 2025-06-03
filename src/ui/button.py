import pygame
from constants import GRAY, LIGHT_GRAY, BLACK, BUTTON_FONT_SIZE

class Button:
    def __init__(self, x, y, width, height, text, font_size=BUTTON_FONT_SIZE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False

    def draw(self, surface):
        color = LIGHT_GRAY if self.is_hovered else GRAY
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False 