import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship):
        super().__init__()
        self.screen = screen

        # Создание энергетической пули
        self.image = pygame.Surface((ai_settings.bullet_width,
                                     ai_settings.bullet_height), pygame.SRCALPHA)
        # Градиент от желтого к красному
        pygame.draw.ellipse(self.image, (255, 255, 0),
                            [0, 0, ai_settings.bullet_width, ai_settings.bullet_height])
        pygame.draw.ellipse(self.image, (255, 100, 0),
                            [2, 2, ai_settings.bullet_width - 4, ai_settings.bullet_height - 4])

        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)