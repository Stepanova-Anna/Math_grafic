class Settings:
    def __init__(self):
        # Настройки экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)


        # Настройки корабля
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Настройки пуль
        self.bullet_speed_factor = 1
        self.bullet_width = 10
        self.bullet_height = 25
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 3

        # Настройки пришельцев
        self.alien_speed_factor = 0.3
        self.fleet_drop_speed = 10
        # fleet_direction = 1 обозначает движение вправо; -1 - влево
        self.fleet_direction = 1

        # Настройка уровней
        self.level = 1
        self.game_speed = 1.4
        self.alien_points = 50
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        # Начальные скорости
        self.alien_speed_factor = 1
        self.alien_drop_speed = 10
        self.bullet_speed_factor = 3

        self.initial_alien_speed = self.alien_speed_factor
        self.initial_fleet_drop_speed = self.fleet_drop_speed
        self.initial_bullet_speed = self.bullet_speed_factor
        self.initial_ship_speed = self.ship_speed_factor


    def increase_level(self):
        """Увеличивает сложность при переходе на новый уровень"""
        self.level += 1
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale

    def reset_difficulty(self):
        """Сбрасывает сложность к начальным значениям"""
        self.level = 1
        self.alien_speed_factor = self.initial_alien_speed
        self.fleet_drop_speed = self.initial_fleet_drop_speed
        self.bullet_speed_factor = self.initial_bullet_speed
        self.ship_speed_factor = self.initial_ship_speed
        self.fleet_direction = 1