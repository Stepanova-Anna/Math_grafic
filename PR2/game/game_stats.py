class GameStats:
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = True
        self.shield_active = False
        self.shield_timer = 0
        self.double_damage_timer = 0
        self.high_score = self.load_high_score()

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        self.shield_active = False
        self.shield_timer = 0
        self.double_damage_timer = 0

    def reset_all(self):
        """Полный сброс игры (статистика + настройки сложности)"""
        # Сбрасываем статистику
        self.reset_stats()
        # Сбрасываем настройки сложности
        self.ai_settings.reset_difficulty()

    def load_high_score(self):
        """Загружает рекорд из файла"""
        try:
            with open('high_score.txt', 'r') as f:
                return int(f.read())
        except FileNotFoundError:
            # Если файла нет - создаем
            self.save_high_score()
            return 0
        except:
            return 0

    def save_high_score(self):
        """Сохраняет рекорд в файл"""
        try:
            with open('high_score.txt', 'w') as f:
                f.write(str(self.high_score))
        except:
            pass