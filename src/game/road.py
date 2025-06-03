import pygame
from src.constants import BLACK, GRAY

class Road:
    text_rects = []

    def __init__(self, city1, city2):
        self.city1 = city1
        self.city2 = city2
        self.is_built = False
        self.is_optimal = False
        self.text_offset = 0

    @classmethod
    def clear_text_rects(cls):
        cls.text_rects.clear()

    def draw(self, screen, highlight=False):
        if self.is_built:
            if self.is_optimal:
                color = (0, 255, 0)
            else:
                color = GRAY
            alpha = 255
        else:
            if highlight:
                color = (150, 150, 150)
                alpha = 200
            else:
                color = (200, 200, 200)
                alpha = 100

        road_surface = pygame.Surface((self.city1.x + self.city2.x, self.city1.y + self.city2.y), pygame.SRCALPHA)
        
        pygame.draw.line(road_surface, (*color, alpha), 
                        (self.city1.x, self.city1.y),
                        (self.city2.x, self.city2.y), 
                        3 if highlight else 2)

        distance = int(self.city1.get_distance_to(self.city2))
        font = pygame.font.Font(None, 24 if highlight else 20)
        text_color = (0, 0, 0) if highlight else (*BLACK, alpha)
        text = font.render(str(distance), True, text_color)
        
        mid_x = (self.city1.x + self.city2.x) // 2
        mid_y = (self.city1.y + self.city2.y) // 2

        dx = self.city2.x - self.city1.x
        dy = self.city2.y - self.city1.y
        angle = pygame.math.Vector2(dx, dy).angle_to(pygame.math.Vector2(1, 0))
        
        offset = 15 + self.text_offset
        offset_x = offset * pygame.math.Vector2(0, -1).rotate(-angle).x
        offset_y = offset * pygame.math.Vector2(0, -1).rotate(-angle).y
        
        text_pos = (mid_x + offset_x, mid_y + offset_y)
        text_rect = text.get_rect(center=text_pos)

        while any(text_rect.colliderect(other_rect) for other_rect in Road.text_rects):
            self.text_offset += 5
            offset = 15 + self.text_offset
            offset_x = offset * pygame.math.Vector2(0, -1).rotate(-angle).x
            offset_y = offset * pygame.math.Vector2(0, -1).rotate(-angle).y
            text_pos = (mid_x + offset_x, mid_y + offset_y)
            text_rect = text.get_rect(center=text_pos)

        Road.text_rects.append(text_rect)
        
        screen.blit(road_surface, (0, 0))
        screen.blit(text, text_rect)

    def get_length(self):
        return self.city1.get_distance_to(self.city2)

    def contains_city(self, city):
        return city in (self.city1, self.city2)

    def get_other_city(self, city):
        if city == self.city1:
            return self.city2
        elif city == self.city2:
            return self.city1
        return None 