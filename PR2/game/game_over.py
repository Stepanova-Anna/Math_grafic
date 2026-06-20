import pygame
import sys


class GameOverScreen:
    """Экран окончания игры - текст прямо на игровом фоне"""

    def __init__(self, screen, stats):
        self.screen = screen
        self.stats = stats
        self.screen_rect = screen.get_rect()

        # Шрифты
        self.title_font = pygame.font.Font(None, 80)
        self.big_font = pygame.font.Font(None, 50)
        self.font = pygame.font.Font(None, 36)

        # Кнопки
        self.play_again_button = pygame.Rect(0, 0, 200, 50)
        self.play_again_button.center = (self.screen_rect.centerx - 120, self.screen_rect.centery + 150)

        self.quit_button = pygame.Rect(0, 0, 200, 50)
        self.quit_button.center = (self.screen_rect.centerx + 120, self.screen_rect.centery + 150)

        self.is_hover_play = False
        self.is_hover_quit = False

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                self.is_hover_play = self.play_again_button.collidepoint(event.pos)
                self.is_hover_quit = self.quit_button.collidepoint(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_again_button.collidepoint(event.pos):
                    return 'play_again'
                elif self.quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return 'play_again'
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        return None

    def draw(self):
        """Отрисовывает текст и кнопки поверх игры (без затемнения)"""

        # Затемнение не делаем - текст поверх игры

        # Заголовок
        title = self.title_font.render("GAME OVER", True, (255, 50, 50))
        title_rect = title.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery - 150))
        # Добавляем тень для читаемости
        shadow = self.title_font.render("GAME OVER", True, (0, 0, 0))
        self.screen.blit(shadow, (title_rect.x + 3, title_rect.y + 3))
        self.screen.blit(title, title_rect)

        # Счет
        score_text = self.big_font.render(f"Счет: {self.stats.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery - 50))
        shadow = self.big_font.render(f"Счет: {self.stats.score}", True, (0, 0, 0))
        self.screen.blit(shadow, (score_rect.x + 2, score_rect.y + 2))
        self.screen.blit(score_text, score_rect)

        # Рекорд
        high_score_text = self.big_font.render(f"Рекорд: {self.stats.high_score}", True, (255, 215, 0))
        high_score_rect = high_score_text.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery + 10))
        shadow = self.big_font.render(f"Рекорд: {self.stats.high_score}", True, (0, 0, 0))
        self.screen.blit(shadow, (high_score_rect.x + 2, high_score_rect.y + 2))
        self.screen.blit(high_score_text, high_score_rect)

        # Уровень
        level_text = self.font.render(f"Уровень: {self.stats.ai_settings.level}", True, (200, 200, 200))
        level_rect = level_text.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery + 60))
        shadow = self.font.render(f"Уровень: {self.stats.level}", True, (0, 0, 0))
        self.screen.blit(shadow, (level_rect.x + 2, level_rect.y + 2))
        self.screen.blit(level_text, level_rect)

        # Кнопки
        color_play = (100, 255, 100) if self.is_hover_play else (0, 200, 0)
        pygame.draw.rect(self.screen, color_play, self.play_again_button, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.play_again_button, 2, border_radius=10)
        play_text = self.font.render("Играть", True, (0, 0, 0))
        play_rect = play_text.get_rect(center=self.play_again_button.center)
        self.screen.blit(play_text, play_rect)

        color_quit = (255, 100, 100) if self.is_hover_quit else (200, 50, 50)
        pygame.draw.rect(self.screen, color_quit, self.quit_button, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.quit_button, 2, border_radius=10)
        quit_text = self.font.render("Выход", True, (0, 0, 0))
        quit_rect = quit_text.get_rect(center=self.quit_button.center)
        self.screen.blit(quit_text, quit_rect)

        # Подсказка
        hint_text = self.font.render("ENTER - играть  |  ESC - выход", True, (180, 180, 180))
        hint_rect = hint_text.get_rect(center=(self.screen_rect.centerx, self.screen_rect.bottom - 40))
        shadow = self.font.render("ENTER - играть  |  ESC - выход", True, (0, 0, 0))
        self.screen.blit(shadow, (hint_rect.x + 2, hint_rect.y + 2))
        self.screen.blit(hint_text, hint_rect)

        pygame.display.flip()