import pygame
from src.constants import BLACK, WHITE

class City:
    def __init__(self, x, y, name, radius=15):
        self.x = x
        self.y = y
        self.name = name
        self.radius = radius
        self.connected_cities = set()
        self.is_selected = False

    def draw(self, screen):
        color = (255, 0, 0) if self.is_selected else BLACK
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius - 2)

        font = pygame.font.Font(None, 28 if self.is_selected else 24)
        text_color = (255, 0, 0) if self.is_selected else BLACK
        text = font.render(self.name, True, text_color)
        text_rect = text.get_rect(center=(self.x, self.y - self.radius - 15))
        
        if self.is_selected:
            padding = 5
            bg_rect = text_rect.inflate(padding * 2, padding * 2)
            pygame.draw.rect(screen, WHITE, bg_rect)
            pygame.draw.rect(screen, text_color, bg_rect, 1)
        
        screen.blit(text, text_rect)

    def is_point_inside(self, point):
        x, y = point
        return ((x - self.x) ** 2 + (y - self.y) ** 2) <= self.radius ** 2

    def connect_to(self, other_city):
        self.connected_cities.add(other_city)
        other_city.connected_cities.add(self)

    def disconnect_from(self, other_city):
        self.connected_cities.discard(other_city)
        other_city.connected_cities.discard(self)

    def get_distance_to(self, other_city):
        dx = self.x - other_city.x
        dy = self.y - other_city.y
        return round(((dx ** 2 + dy ** 2) ** 0.5), 1) 