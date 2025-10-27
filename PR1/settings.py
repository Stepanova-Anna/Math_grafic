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