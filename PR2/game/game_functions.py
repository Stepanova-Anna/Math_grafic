import sys
import os
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
from bonus import Bonus

laser_sound = None
explosion_sound = None
game_over_sound = None
life_lost_sound = None


def resource_path(relative_path):
    """Получает абсолютный путь к ресурсу, работает и в .exe и в .py"""
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Если запущено как скрипт (не .exe)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def update_screen(ai_settings, screen, ship, aliens, bullets, stats, background, bonuses):
    """Обновляет изображения на экране и отображает новый экран"""
    # Отрисовка фона
    screen.blit(background, (0, 0))

    # Отрисовка пуль
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    bonuses.draw(screen)

    # Отображение статистики
    font = pygame.font.SysFont(None, 36)
    score_str = f"Жизни: {stats.ships_left}  Очки: {stats.score}"
    score_image = font.render(score_str, True, (255, 255, 255))
    screen.blit(score_image, (20, 20))
    level_str = f"Уровень: {ai_settings.level}"
    level_image = font.render(level_str, True, (255, 255, 255))
    screen.blit(level_image, (20, 60))

    pygame.display.flip()


def check_events(ai_settings, screen, ship, bullets, stats, aliens, bonuses):
    """Обрабатывает нажатия клавиш и события мыши"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats, aliens, bonuses)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, aliens, bonuses):
    """Реагирует на нажатие клавиш"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_s:
        # Сохранение игры (клавиша S)
        from save_game import save_game
        save_game(ai_settings, stats)
    elif event.key == pygame.K_l:
        # Загрузка игры (клавиша L)
        from save_game import load_game
        if load_game(ai_settings, stats):
            # Пересоздаем флот после загрузки
            aliens.empty()
            bullets.empty()
            create_fleet(ai_settings, screen, ship, aliens)
    elif event.key == pygame.K_q:
        # Выход из игры (клавиша Q)
        sys.exit()


def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def fire_bullet(ai_settings, screen, ship, bullets):
    """Выпускает пулю, если максимум еще не достигнут"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        laser_sound.play()


def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, bonuses):
    """Обновляет позиции пуль и удаляет старые пули"""
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, bonuses)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, bonuses):
    """Обработка коллизий пуль с пришельцами"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # Добавляем очки за уничтоженных пришельцев
    if collisions:
        if explosion_sound:
            explosion_sound.play()

        for aliens_list in collisions.values():
            stats.score += 50 * len(aliens_list)

            # Шанс выпадения бонуса (20%)
            import random
            if random.random() < 0.2:
                bonus_types = ['life', 'shield', 'double_damage']
                bonus_type = random.choice(bonus_types)
                # Берем первого пришельца из списка
                for alien in aliens_list:
                    new_bonus = Bonus(ai_settings, screen, alien.rect.centerx, alien.rect.centery, bonus_type)
                    bonuses.add(new_bonus)
                    break

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_level()
        create_fleet(ai_settings, screen, ship, aliens)
        sleep(0.5)


def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количество рядов пришельцев, помещающихся на экране"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Обновляет позиции всех пришельцев во флоте"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Обрабатывает столкновение корабля с пришельцем"""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        life_lost_sound.play()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        if stats.score > stats.high_score:
            stats.high_score = stats.score
            stats.save_high_score()

        if game_over_sound:
            game_over_sound.play()
        stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Проверяет, добрались ли пришельцы до нижнего края экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def check_bonus_collisions(ship, bonuses, stats, ai_settings):
    """Проверяет столкновения корабля с бонусами"""
    collisions = pygame.sprite.spritecollide(ship, bonuses, True)

    for bonus in collisions:
        if bonus.bonus_type == 'life':
            # Восстанавливаем жизнь
            stats.ships_left += 1
            print(f"❤ Восстановлена жизнь! Жизней: {stats.ships_left}")

        elif bonus.bonus_type == 'shield':
            # Активируем щит (игнорируем столкновения на 5 секунд)
            stats.shield_active = True
            stats.shield_timer = 300  # 5 секунд при 60 FPS
            print("🛡 Щит активирован!")

        elif bonus.bonus_type == 'double_damage':
            # Удвоенный урон (каждая пуля уничтожает 2 пришельца)
            ai_settings.double_damage = True
            stats.double_damage_timer = 300  # 5 секунд
            print("⚡ Удвоенный урон!")