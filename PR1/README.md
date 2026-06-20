# Отчет по практической работе №1
## «Инопланетное вторжение» - базовая 2D-игра на Pygame

---

## 1. Цель работы

Разработать базовую 2D-игру «Инопланетное вторжение» с использованием библиотеки Pygame, в которой игрок управляет космическим кораблем и уничтожает флот инопланетян. В ходе работы необходимо освоить основы разработки игр на Python, включая работу с графикой, анимацией, обработкой событий и организацией игрового цикла.

---

## 2. Используемые технологии

- **Язык программирования:** Python 3.12.6
- **Библиотека:** Pygame 2.6.1
- **Среда разработки:** PyCharm

---

## 3. Структура проекта

Проект организован по модульному принципу для повышения читаемости и управляемости кода:

```
pythonProject/
├── alien_invasion.py      # Главный файл, запуск игры
├── settings.py            # Настройки игры
├── ship.py                # Класс корабля
├── alien.py               # Класс инопланетянина
├── bullet.py              # Класс пули
├── game_functions.py      # Игровые функции
├── game_stats.py          # Статистика игры
├── images/                # Папка с изображениями
│   ├── fon.jpg            # Фоновое изображение
│   ├── alien.png          # Изображение инопланетянина
│   └── ship.png           # Изображение корабля
└── sounds/                # Папка со звуками (для дальнейшего расширения)
```

---

## 4. Описание классов и функций

### 4.1. Класс `Settings` (`settings.py`)

Класс отвечает за хранение всех настроек игры в одном месте.

**Основные атрибуты:**

| Группа | Параметр | Значение | Описание |
|--------|----------|----------|----------|
| **Экран** | `screen_width` | 1200 | Ширина окна |
| | `screen_height` | 800 | Высота окна |
| **Корабль** | `ship_speed_factor` | 1.5 | Скорость перемещения |
| | `ship_limit` | 3 | Количество жизней |
| **Пули** | `bullet_speed_factor` | 3 | Скорость пули |
| | `bullet_width` | 3 | Ширина пули |
| | `bullet_height` | 15 | Высота пули |
| | `bullet_color` | (60,60,60) | Цвет пули |
| | `bullets_allowed` | 3 | Максимум пуль на экране |
| **Инопланетяне** | `alien_speed_factor` | 1 | Скорость движения |
| | `fleet_drop_speed` | 10 | Скорость спуска |
| | `fleet_direction` | 1 | Направление (1/-1) |
| **Уровни** | `level` | 1 | Текущий уровень |
| | `speedup_scale` | 1.1 | Множитель увеличения скорости |

**Ключевые методы:**

```python
def increase_level(self):
    """Увеличивает сложность при переходе на новый уровень"""
    self.level += 1
    self.alien_speed_factor *= self.speedup_scale
    self.fleet_drop_speed *= self.speedup_scale
    self.bullet_speed_factor *= self.speedup_scale
```

---

### 4.2. Класс `Ship` (`ship.py`)

Класс представляет игровой корабль.

**Основные атрибуты:**
- `screen` - поверхность для отрисовки
- `image` - загруженное изображение корабля
- `rect` - прямоугольник для позиционирования
- `centerx` - точная координата по X (для плавного движения)
- `moving_right` / `moving_left` - флаги движения

**Ключевые методы:**

```python
def update(self):
    """Обновляет позицию корабля"""
    if self.moving_right and self.rect.right < self.screen_rect.right:
        self.centerx += self.ai_settings.ship_speed_factor
    if self.moving_left and self.rect.left > 0:
        self.centerx -= self.ai_settings.ship_speed_factor
    self.rect.centerx = self.centerx

def center_ship(self):
    """Центрирует корабль на экране"""
    self.centerx = self.screen_rect.centerx
```

---

### 4.3. Класс `Bullet` (`bullet.py`)

Класс представляет снаряд, выпущенный кораблем.

**Основные атрибуты:**
- `rect` - прямоугольник пули
- `color` - цвет пули
- `speed_factor` - скорость движения

**Ключевые методы:**

```python
def update(self):
    """Перемещает пулю вверх"""
    self.rect.y -= self.speed_factor

def draw_bullet(self):
    """Рисует пулю на экране"""
    pygame.draw.rect(self.screen, self.color, self.rect)
```

---

### 4.4. Класс `Alien` (`alien.py`)

Класс представляет инопланетянина.

**Основные атрибуты:**
- `image` - изображение инопланетянина
- `rect` - прямоугольник для позиционирования
- `x` - точная координата по X

**Ключевые методы:**

```python
def check_edges(self):
    """Проверяет, достиг ли инопланетянин края экрана"""
    screen_rect = self.screen.get_rect()
    if self.rect.right >= screen_rect.right:
        return True
    elif self.rect.left <= 0:
        return True
    return False

def update(self):
    """Обновляет позицию инопланетянина"""
    self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
    self.rect.x = self.x
```

---

### 4.5. Модуль `game_functions.py`

Содержит основные игровые функции.

**Основные функции:**

| Функция | Назначение |
|---------|------------|
| `check_events()` | Обработка событий клавиатуры |
| `fire_bullet()` | Создание новой пули |
| `update_bullets()` | Обновление позиций пуль |
| `check_bullet_alien_collisions()` | Проверка столкновений пуль с пришельцами |
| `create_fleet()` | Создание флота пришельцев |
| `update_aliens()` | Обновление позиций пришельцев |
| `ship_hit()` | Обработка попадания по кораблю |
| `update_screen()` | Обновление экрана |

---

### 4.6. Класс `GameStats` (`game_stats.py`)

Хранит статистику игры.

**Атрибуты:**
- `game_active` - активна ли игра
- `ships_left` - оставшиеся жизни
- `score` - текущий счет

---

## 5. Реализация игровой логики

### 5.1. Основной игровой цикл

```python
while True:
    gf.check_events(ai_settings, screen, ship, bullets)
    
    if stats.game_active:
        ship.update()
        gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats)
        gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
    
    gf.update_screen(ai_settings, screen, ship, aliens, bullets, stats, background)
```

**Этапы цикла:**
1. **Обработка событий** - проверка нажатий клавиш и закрытия окна
2. **Обновление состояния** - движение корабля, пуль, пришельцев
3. **Отрисовка** - вывод всех объектов на экран
4. **Управление FPS** - задержка для контроля скорости

### 5.2. Управление кораблем

- **←** - движение влево
- **→** - движение вправо
- **Пробел** - выстрел

```python
def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
```

### 5.3. Движение флота пришельцев

Пришельцы движутся горизонтально и при достижении края экрана:
1. Меняют направление движения
2. Опускаются вниз на одну позицию

```python
def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
```

### 5.4. Система жизней

- Игрок начинает с 3 жизнями
- При столкновении с пришельцем или достижении нижней границы теряется 1 жизнь
- При потере всех жизней игра завершается

```python
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
```

### 5.5. Система уровней

При уничтожении всех пришельцев:
1. Уровень увеличивается на 1
2. Увеличивается скорость пришельцев
3. Создается новый флот

```python
if len(aliens) == 0:
    bullets.empty()
    ai_settings.increase_level()
    create_fleet(ai_settings, screen, ship, aliens)
    sleep(0.5)
```

---

## 6. Скриншоты игры

### 6.1. Игровой процесс

На скриншоте представлен игровой процесс. В верхней части экрана отображаются:
- Количество жизней (слева)
- Текущий счет (в центре)
- Уровень (слева под жизнями)

В центре экрана располагается флот инопланетян, движущихся по горизонтали и постепенно опускающихся вниз.

<img width="1498" height="1013" alt="image" src="https://github.com/user-attachments/assets/5aebe220-4dd9-4a8f-835d-e749a7846771" />


### 6.2. Конец игры

При потере всех жизней игра переходит в состояние Game Over. Игрок видит экран завершения игры с финальным счетом.

<img width="1496" height="978" alt="image" src="https://github.com/user-attachments/assets/f3ffda8b-3e30-4a45-8ba7-ad9847f6f3d8" />


---

## 7. Выводы

В ходе выполнения практической работы были достигнуты следующие результаты:

1. **Освоена работа с библиотекой Pygame** - создание игрового окна, обработка событий, управление спрайтами.
2. **Реализована полноценная 2D-игра** со следующей механикой:
   - Управление кораблем с помощью клавиш-стрелок
   - Стрельба по пришельцам пробелом
   - Движущийся флот инопланетян
   - Система жизней
   - Система уровней с увеличением сложности
   - Подсчет очков
3. **Создана модульная структура проекта** для удобства поддержки и расширения.
4. **Применены основные принципы ООП** - инкапсуляция, наследование, полиморфизм.

**Полученные навыки:**
- Работа с графикой и анимацией в Pygame
- Обработка пользовательского ввода
- Обнаружение столкновений
- Управление игровым циклом
- Организация кода в модули

