@echo off
echo ========================================
echo   Сборка игры Alien Invasion для Windows
echo ========================================
echo.

echo Удаляем старую сборку...
rmdir /s /q dist 2>nul
rmdir /s /q build 2>nul
del /q *.spec 2>nul

echo.
echo Начинаем сборку...
pyinstaller --onefile --windowed --add-data "images;images" --add-data "sounds;sounds" alien_invasion.py

echo.
echo ========================================
echo   СБОРКА ЗАВЕРШЕНА!
echo   Исполняемый файл: dist\alien_invasion.exe
echo ========================================
pause