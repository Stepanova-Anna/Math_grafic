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
            print("❌ Файл сохранения не найден! Нажмите S чтобы сохранить.")
            return False

        with open('savefile.pkl', 'rb') as f:
            game_data = pickle.load(f)

        settings.level = game_data['level']
        stats.score = game_data['score']
        stats.ships_left = game_data['ships_left']

        if 'high_score' in game_data:
            stats.high_score = game_data['high_score']
            stats.save_high_score()

        print(f"✅ Игра загружена! Уровень: {settings.level}, Очки: {stats.score}, Жизней: {stats.ships_left}")
        return True
    except FileNotFoundError:
        print("❌ Файл сохранения не найден!")
        return False
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        return False