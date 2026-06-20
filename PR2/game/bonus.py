import pygame
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Bonus(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen, x, y, bonus_type):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.bonus_type = bonus_type

        # Загружаем изображения для бонусов
        images = {
            'life': pygame.image.load(resource_path('images/life_bonus.png')),
            'shield': pygame.image.load(resource_path('images/shield_bonus.png')),
            'double_damage': pygame.image.load(resource_path('images/damage_bonus.png'))
        }

        self.image = images.get(bonus_type)
        if self.image:
            self.image = pygame.transform.scale(self.image, (30, 30))
        else:
            # Запасной вариант - цветной квадрат
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        self.speed = 1.5
        self.lifetime = 600

    def update(self):
        self.rect.y += self.speed
        self.lifetime -= 1
        if self.rect.top > self.screen.get_rect().bottom or self.lifetime <= 0:
            self.kill()