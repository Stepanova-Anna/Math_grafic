import pygame
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
import game_functions as gf


def run_game():
    # Инициализация pygame и создание объекта настроек
    pygame.init()
    ai_settings = Settings()

    # Создание игрового окна
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # 🔹 ЗАГРУЗКА ФОНА (добавьте этот код)
    try:
        background = pygame.image.load('images/fon.jpg')
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

    # Главный цикл игры
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, ship, aliens, bullets, stats, background)


if __name__ == "__main__":
    run_game()