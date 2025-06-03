import pygame
from src.game.city import City
from src.game.road import Road
from src.game.levels_data import LEVELS, LEVEL_NAMES, LEVEL_DESCRIPTIONS

class Level:
    UI_TOP_MARGIN = 120
    UI_BOTTOM_MARGIN = 40
    UI_SIDE_MARGIN = 50

    def __init__(self, level_number, width, height):
        self.width = width
        self.height = height
        self.level_number = level_number
        self.cities = []
        self.roads = []
        self.selected_city = None
        self.total_length = 0
        self.optimal_length = 0
        self.is_complete = False
        
        self.game_area = {
            'left': self.UI_SIDE_MARGIN,
            'right': self.width - self.UI_SIDE_MARGIN,
            'top': self.UI_TOP_MARGIN,
            'bottom': self.height - self.UI_BOTTOM_MARGIN
        }
        
        self._create_cities_from_data()
        self._generate_roads()
        self._calculate_optimal_solution()

    def _create_cities_from_data(self):
        level_data = LEVELS[self.level_number - 1]
        for i, (x, y) in enumerate(level_data):
            name = f"Город {i + 1}"
            self.cities.append(City(x, y, name))

    def _generate_roads(self):
        for i in range(len(self.cities)):
            for j in range(i + 1, len(self.cities)):
                self.roads.append(Road(self.cities[i], self.cities[j]))

    def _calculate_optimal_solution(self):
        sorted_roads = sorted(self.roads, key=lambda x: x.get_length())
        for road in sorted_roads:
            if not self._would_create_cycle(road):
                road.is_optimal = True
                self.optimal_length += road.get_length()

    def _would_create_cycle(self, road):
        visited = set()
        
        def dfs(city, target, parent=None):
            if city == target and parent is not None:
                return True
            if city in visited:
                return False
                
            visited.add(city)
            for connected_city in city.connected_cities:
                if connected_city != parent:
                    if dfs(connected_city, target, city):
                        return True
            return False

        return dfs(road.city1, road.city2)

    def handle_click(self, pos):
        if not (self.game_area['left'] <= pos[0] <= self.game_area['right'] and
                self.game_area['top'] <= pos[1] <= self.game_area['bottom']):
            return

        clicked_city = None
        for city in self.cities:
            if city.is_point_inside(pos):
                clicked_city = city
                break

        if clicked_city:
            if self.selected_city is None:
                self.selected_city = clicked_city
                clicked_city.is_selected = True
            elif self.selected_city == clicked_city:
                self.selected_city.is_selected = False
                self.selected_city = None
            else:
                self._build_road(self.selected_city, clicked_city)
                self.selected_city.is_selected = False
                self.selected_city = None

    def _build_road(self, city1, city2):
        for road in self.roads:
            if (road.city1 == city1 and road.city2 == city2) or \
               (road.city1 == city2 and road.city2 == city1):
                if not road.is_built:
                    road.is_built = True
                    city1.connect_to(city2)
                    self.total_length += road.get_length()
                    self._check_completion()
                break

    def _check_completion(self):
        if not self.cities:
            return

        visited = set()
        def dfs(city):
            visited.add(city)
            for connected_city in city.connected_cities:
                if connected_city not in visited:
                    dfs(connected_city)

        dfs(self.cities[0])
        self.is_complete = len(visited) == len(self.cities)

    def draw(self, screen):
        Road.clear_text_rects()
        
        for road in self.roads:
            if self.selected_city and (road.city1 == self.selected_city or road.city2 == self.selected_city):
                road.draw(screen, highlight=True)
            else:
                road.draw(screen)
        
        for city in self.cities:
            city.draw(screen)

        font = pygame.font.Font(None, 36)
        text = font.render(f"Длина: {int(self.total_length)} / {int(self.optimal_length)}", True, (0, 0, 0))
        screen.blit(text, (10, 10))

        level_name = LEVEL_NAMES[self.level_number - 1]
        level_desc = LEVEL_DESCRIPTIONS[self.level_number - 1]
        
        name_font = pygame.font.Font(None, 32)
        desc_font = pygame.font.Font(None, 24)
        
        name_text = name_font.render(level_name, True, (0, 0, 0))
        desc_text = desc_font.render(level_desc, True, (100, 100, 100))
        
        screen.blit(name_text, (10, 50))
        screen.blit(desc_text, (10, 85))

        hint_font = pygame.font.Font(None, 24)
        hint1 = hint_font.render("Серые линии - возможные дороги, числа - их длина", True, (100, 100, 100))
        hint2 = hint_font.render("Выберите город, чтобы увидеть возможные соединения", True, (100, 100, 100))
        screen.blit(hint1, (10, self.height - 60))
        screen.blit(hint2, (10, self.height - 30))

        if self.is_complete:
            overlay = pygame.Surface((self.width, 100), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 200))
            
            if abs(self.total_length - self.optimal_length) < 0.1:
                result_text = "Поздравляем! Вы нашли оптимальное решение!"
                text_color = (0, 200, 0)
            else:
                result_text = "Все города соединены, но решение не оптимально"
                text_color = (200, 0, 0)
            
            result_font = pygame.font.Font(None, 36)
            result_surface = result_font.render(result_text, True, text_color)
            result_rect = result_surface.get_rect(center=(self.width // 2, 50))
            
            screen.blit(overlay, (0, 0))
            screen.blit(result_surface, result_rect) 