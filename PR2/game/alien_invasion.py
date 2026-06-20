import pygame
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
import game_functions as gf
from time import sleep
from game_over import GameOverScreen
import os
import sys

def resource_path(relative_path):
    """Получает абсолютный путь к ресурсу, работает и в .exe и в .py"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def run_game():
    # Инициализация pygame и создание объекта настроек
    pygame.init()
    ai_settings = Settings()

    # Создание игрового окна
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    pygame.mixer.init()
    gf.laser_sound = pygame.mixer.Sound(resource_path("sounds/laser.wav"))
    gf.explosion_sound = pygame.mixer.Sound(resource_path("sounds/explosion.wav"))
    gf.game_over_sound = pygame.mixer.Sound(resource_path("sounds/game_over.wav"))
    gf.life_lost_sound = pygame.mixer.Sound(resource_path("sounds/life_lost.wav"))



    # 🔹 ЗАГРУЗКА ФОНА
    try:
        background = pygame.image.load(resource_path('images/fon.jpg'))
        background = pygame.transform.scale(background, (ai_settings.screen_width, ai_settings.screen_height))
        print("Фон загружен успешно!")
    except pygame.error as e:
        print(f"Ошибка загрузки фона: {e}")
        # Создаем черный фон если изображение не загружено
        background = pygame.Surface((ai_settings.screen_width, ai_settings.screen_height))
        background.fill((0, 0, 0))

    # Создание экземпляра для хранения игровой статистики
    stats = GameStats(ai_settings)

    # Создание корабля
    ship = Ship(ai_settings, screen)

    # Создание группы для хранения пуль
    bullets = pygame.sprite.Group()

    # Создание флота пришельцев
    aliens = pygame.sprite.Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    bonuses = pygame.sprite.Group()
    game_over_screen = GameOverScreen(screen, stats)

    # Главный цикл игры
    while True:
        if stats.game_active:
            # ИГРОВОЙ РЕЖИМ
            gf.check_events(ai_settings, screen, ship, bullets, stats, aliens, bonuses)

            if stats.game_active:
                ship.update()
                gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, bonuses)
                gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
                bonuses.update()
                gf.check_bonus_collisions(ship, bonuses, stats, ai_settings)

            gf.update_screen(ai_settings, screen, ship, aliens, bullets, stats, background, bonuses)

        else:
            # РЕЖИМ GAME OVER
            action = game_over_screen.check_events()

            if action == 'play_again':
                # Перезапуск игры
                stats.reset_all()
                stats.game_active = True
                aliens.empty()
                bullets.empty()
                bonuses.empty()
                gf.create_fleet(ai_settings, screen, ship, aliens)
                ship.center_ship()
                pygame.mouse.set_visible(False)
            else:
                # Показываем экран Game Over
                game_over_screen.draw()
                pygame.mouse.set_visible(True)


if __name__ == "__main__":
    run_game()