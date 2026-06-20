# Отчет по практической работе №2
## Развитие игры «Инопланетное вторжение»

---

## 1. Цель работы

Дополнить базовую игру «Инопланетное вторжение» функциональностью, которая сделает игровой процесс более увлекательным и технологичным. В ходе работы были добавлены звуковые эффекты, система уровней, сохранение прогресса, интерактивные объекты (бонусы) и создан исполняемый файл игры.

---

## 2. Используемые технологии

- **Язык программирования:** Python 3.12.6
- **Библиотека:** Pygame 2.6.1
- **Сериализация данных:** модуль pickle
- **Сборка исполняемого файла:** PyInstaller
- **Среда разработки:** PyCharm

---

## 3. Структура проекта

```
pythonProject/
├── alien_invasion.py      # Главный файл, запуск игры
├── settings.py            # Настройки игры
├── ship.py                # Класс корабля
├── alien.py               # Класс инопланетянина
├── bullet.py              # Класс пули
├── bonus.py               # Класс бонусов
├── game_functions.py      # Игровые функции
├── game_stats.py          # Статистика игры
├── game_over.py           # Экран окончания игры
├── save_game.py           # Сохранение/загрузка прогресса
├── high_score.txt         # Файл с рекордом
├── savefile.pkl           # Файл сохранения игры
├── images/                # Папка с изображениями
│   ├── fon.jpg            # Фоновое изображение
│   ├── alien.png          # Изображение инопланетянина
│   └── ship.png           # Изображение корабля
└── sounds/                # Папка со звуками
    ├── laser.wav          # Звук выстрела
    ├── explosion.wav      # Звук взрыва пришельца
    ├── game_over.wav      # Звук окончания игры
    └── life_lost.wav      # Звук потери жизни
```

---

## 4. Реализация заданий

### 4.1. Звуковые эффекты

**Реализация:**

1. Подготовлены звуковые файлы в формате `.wav` в папке `sounds/`:
   - `laser.wav` - звук выстрела
   - `explosion.wav` - звук уничтожения пришельца
   - `game_over.wav` - звук окончания игры
   - `life_lost.wav` - звук потери жизни

2. Инициализация звуков в главном файле:
```python
pygame.mixer.init()
gf.laser_sound = pygame.mixer.Sound("sounds/laser.wav")
gf.explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
gf.game_over_sound = pygame.mixer.Sound("sounds/game_over.wav")
gf.life_lost_sound = pygame.mixer.Sound("sounds/life_lost.wav")
```

3. Связь звуков с игровыми событиями:

**Выстрел** (функция `fire_bullet`):
```python
def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        if laser_sound:
            laser_sound.play()
```

**Уничтожение пришельца** (функция `check_bullet_alien_collisions`):
```python
if collisions:
    if explosion_sound:
        explosion_sound.play()
    # ... начисление очков
```

**Потеря жизни** (функция `ship_hit`):
```python
if stats.ships_left > 0:
    stats.ships_left -= 1
    if life_lost_sound:
        life_lost_sound.play()
    # ... сброс позиций
```

**Конец игры** (функция `ship_hit`):
```python
else:
    if game_over_sound:
        game_over_sound.play()
    stats.game_active = False
```

---

### 4.2. Система уровней

**Реализация:**

1. В `settings.py` добавлены настройки уровней:

```python
class Settings():
    def __init__(self):
        # ... другие настройки
        
        # Настройки уровней
        self.level = 1
        self.speedup_scale = 1.1
        
        # Сохранение начальных значений для сброса
        self.initial_alien_speed = self.alien_speed_factor
        self.initial_fleet_drop_speed = self.fleet_drop_speed
        self.initial_bullet_speed = self.bullet_speed_factor
    
    def increase_level(self):
        """Увеличивает сложность при переходе на новый уровень"""
        self.level += 1
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.ship_speed_factor *= self.speedup_scale
    
    def reset_difficulty(self):
        """Сбрасывает сложность к начальным значениям"""
        self.level = 1
        self.alien_speed_factor = self.initial_alien_speed
        self.fleet_drop_speed = self.initial_fleet_drop_speed
        self.bullet_speed_factor = self.initial_bullet_speed
        self.ship_speed_factor = self.initial_ship_speed
        self.fleet_direction = 1
```

2. Переход на новый уровень в `game_functions.py`:

```python
def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, bonuses):
    # ... проверка столкновений
    
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_level()
        create_fleet(ai_settings, screen, ship, aliens)
        sleep(0.5)
```

3. Отображение текущего уровня на экране:

```python
level_str = f"Уровень: {ai_settings.level}"
level_image = font.render(level_str, True, (255, 255, 255))
screen.blit(level_image, (20, 60))
```

---

### 4.3. Сохранение и загрузка прогресса

**Реализация:**

1. Создан модуль `save_game.py`:

```python
import pickle
import os

def save_game(settings, stats):
    """Сохраняет прогресс игры в файл"""
    game_data = {
        'level': settings.level,
        'score': stats.score,
        'ships_left': stats.ships_left,
        'high_score': stats.high_score
    }
    
    try:
        with open('savefile.pkl', 'wb') as f:
            pickle.dump(game_data, f)
        print("✅ Игра сохранена!")
        return True
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")
        return False

def load_game(settings, stats):
    """Загружает прогресс игры из файла"""
    try:
        if not os.path.exists('savefile.pkl'):
            print("❌ Файл сохранения не найден!")
            return False
            
        with open('savefile.pkl', 'rb') as f:
            game_data = pickle.load(f)
        
        settings.level = game_data['level']
        stats.score = game_data['score']
        stats.ships_left = game_data['ships_left']
        
        if 'high_score' in game_data:
            stats.high_score = game_data['high_score']
            stats.save_high_score()
        
        print(f"✅ Игра загружена! Уровень: {settings.level}, Очки: {stats.score}")
        return True
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        return False
```

2. Добавлены клавиши управления:
- **S** - сохранить игру
- **L** - загрузить сохранение

```python
elif event.key == pygame.K_s:
    from save_game import save_game
    save_game(ai_settings, stats)
elif event.key == pygame.K_l:
    from save_game import load_game
    if load_game(ai_settings, stats):
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
```

3. Рекорд сохраняется в отдельный файл `high_score.txt`:

```python
def save_high_score(self):
    try:
        with open('high_score.txt', 'w') as f:
            f.write(str(self.high_score))
    except:
        pass
```

---

### 4.4. Интерактивные объекты (Бонусы)

**Реализация:**

1. Создан класс `Bonus` в файле `bonus.py`:

```python
class Bonus(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen, x, y, bonus_type):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.bonus_type = bonus_type
        
        # Цвета для разных бонусов
        colors = {
            'life': (0, 255, 0),        # Зеленый - жизнь
            'shield': (0, 150, 255),    # Голубой - щит
            'double_damage': (255, 200, 0)  # Золотой - удвоенный урон
        }
        
        # Создание изображения бонуса
        self.image = pygame.Surface((30, 30))
        self.image.fill(colors.get(bonus_type, (255, 255, 255)))
        
        # Символ в центре бонуса
        font = pygame.font.SysFont(None, 24)
        symbols = {
            'life': '❤',
            'shield': '🛡',
            'double_damage': '⚡'
        }
        symbol = symbols.get(self.bonus_type, '?')
        text = font.render(symbol, True, (255, 255, 255))
        text_rect = text.get_rect(center=(15, 15))
        self.image.blit(text, text_rect)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 1.5
        self.lifetime = 600  # 10 секунд при 60 FPS
    
    def update(self):
        self.rect.y += self.speed
        self.lifetime -= 1
        if self.rect.top > self.screen.get_rect().bottom or self.lifetime <= 0:
            self.kill()
```

2. Появление бонусов с вероятностью 20% при уничтожении пришельца:

```python
import random
if random.random() < 0.2:  # 20% вероятность
    bonus_types = ['life', 'shield', 'double_damage']
    bonus_type = random.choice(bonus_types)
    for alien in aliens_list:
        new_bonus = Bonus(ai_settings, screen, alien.rect.centerx, alien.rect.centery, bonus_type)
        bonuses.add(new_bonus)
        break
```

3. Обработка столкновений с бонусами:

```python
def check_bonus_collisions(ship, bonuses, stats, ai_settings):
    collisions = pygame.sprite.spritecollide(ship, bonuses, True)
    
    for bonus in collisions:
        if bonus.bonus_type == 'life':
            stats.ships_left += 1  # Восстановление жизни
            print(f"❤ Восстановлена жизнь! Жизней: {stats.ships_left}")
        
        elif bonus.bonus_type == 'shield':
            stats.shield_active = True  # Активация щита
            stats.shield_timer = 300
            print("🛡 Щит активирован!")
        
        elif bonus.bonus_type == 'double_damage':
            ai_settings.double_damage = True  # Удвоенный урон
            stats.double_damage_timer = 300
            print("⚡ Удвоенный урон!")
```

---

### 4.5. Экран окончания игры

**Реализация:**

Создан класс `GameOverScreen` в файле `game_over.py`:

```python
class GameOverScreen:
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
```

**Функциональность экрана Game Over:**
- Полупрозрачный затемняющий оверлей
- Отображение финального счета
- Отображение лучшего результата (рекорда)
- Отображение достигнутого уровня
- Кнопки "Играть снова" и "Выход" (с наведением)
- Горячие клавиши: ENTER - играть, ESC - выход

---

## 5. Игровой процесс

### 5.1. Управление

| Клавиша | Действие |
|---------|----------|
| ← | Движение влево |
| → | Движение вправо |
| ПРОБЕЛ | Выстрел |
| S | Сохранить игру |
| L | Загрузить игру |
| Q | Выход из игры |

### 5.2. Игровая механика

1. **Уничтожение пришельцев** - за каждого пришельца начисляется 50 очков
2. **Переход на уровень** - после уничтожения всего флота скорость пришельцев увеличивается на 10%
3. **Потеря жизни** - при столкновении с пришельцем или достижении нижней границы
4. **Конец игры** - при потере всех 3 жизней
5. **Бонусы** - выпадают с вероятностью 20% при уничтожении пришельца:
   - ❤ **Жизнь** - восстанавливает 1 жизнь
   - 🛡 **Щит** - защищает от столкновений на 5 секунд
   - ⚡ **Удвоенный урон** - уничтожает 2 пришельцев за 1 выстрел на 5 секунд
6. **Рекорд** - сохраняется в файл `high_score.txt`

---

## 6. Скриншоты игры

### 6.1. Игровой процесс

На скриншоте представлен игровой процесс. В верхней части экрана отображаются:
- Количество жизней (слева)
- Текущий счет (в центре)
- Уровень (под жизнями)
- Флот инопланетян движется горизонтально
- Виден корабль игрока в нижней части экрана



<img width="1499" height="982" alt="image" src="https://github.com/user-attachments/assets/3d481c9b-c9b3-4785-801d-aa292c5bbf44" />

### 6.2. Бонусы на экране

На скриншоте показаны бонусы, выпавшие после уничтожения пришельцев:
- Зеленый бонус (❤) - восстанавливает жизнь
- Голубой бонус (🛡) - активирует щит
- Золотой бонус (⚡) - дает удвоенный урон

<img width="1497" height="979" alt="image" src="https://github.com/user-attachments/assets/36ca5bd6-717f-4b6c-8404-62e243fe20d4" />


### 6.3. Экран Game Over

При окончании игры появляется полупрозрачное затемнение с информацией:
- Заголовок "GAME OVER" красным цветом
- Финальный счет
- Лучший результат (золотым цветом)
- Достигнутый уровень
- Кнопки "Играть снова" и "Выход"

<img width="1499" height="976" alt="image" src="https://github.com/user-attachments/assets/7e8dd57e-9d81-4baf-8465-d7e84369ee54" />


---

## 7. Сборка исполняемого файла

### 7.1. Установка PyInstaller

```bash
pip install pyinstaller
```

### 7.2. Создание исполняемого файла для Windows

Создан файл `build_windows.bat`:

```batch
@echo off
echo Сборка игры для Windows...
pyinstaller --onefile --windowed --add-data "images;images" --add-data "sounds;sounds" alien_invasion.py
echo Готово! Исполняемый файл в папке dist/
pause
```

### 7.3. Результат сборки

После успешной сборки исполняемый файл `alien_invasion.exe` находится в папке `dist/`. Пользователи могут запускать игру без необходимости установки Python и зависимостей.

---

## 8. Дополнительный функционал

### 8.1. Система рекордов

- Рекорд сохраняется в файл `high_score.txt`
- При установлении нового рекорда он автоматически сохраняется
- Рекорд отображается на экране Game Over золотым цветом

### 8.2. Полный сброс игры

При нажатии "Играть снова" выполняется полный сброс:
- Сбрасывается статистика (жизни=3, счет=0)
- Сбрасывается сложность (уровень=1, скорости=начальные)
- Очищаются все группы объектов
- Создается новый флот пришельцев

```python
def reset_all(self):
    self.reset_stats()
    self.ai_settings.reset_difficulty()
```

---

## 9. Выводы

В ходе выполнения практической работы №2 были достигнуты следующие результаты:

### 9.1. Реализованный функционал

1. ✅ **Звуковые эффекты** - добавлены звуки для всех ключевых игровых событий
2. ✅ **Система уровней** - сложность увеличивается с каждым новым уровнем
3. ✅ **Сохранение прогресса** - реализовано сохранение/загрузка с помощью pickle
4. ✅ **Интерактивные объекты** - добавлены 3 типа бонусов с различными механиками
5. ✅ **Экран Game Over** - информативный экран окончания игры
6. ✅ **Система рекордов** - сохранение лучшего результата
7. ✅ **Сборка исполняемого файла** - создан .exe файл с помощью PyInstaller

### 9.2. Полученные навыки

- Работа со звуковыми эффектами в Pygame (`pygame.mixer`)
- Реализация системы уровней и увеличения сложности
- Сериализация данных с помощью модуля `pickle`
- Создание интерактивных объектов с различными механиками
- Разработка пользовательского интерфейса (кнопки, меню)
- Сборка приложения в исполняемый файл

### 9.3. Итог

Разработанная игра представляет собой полноценный игровой проект, включающий все основные элементы современных игр: звуковое сопровождение, систему уровней, сохранение прогресса, бонусы и рекорды. Игра готова к распространению в виде исполняемого файла и может быть запущена на любом компьютере без установки Python.


