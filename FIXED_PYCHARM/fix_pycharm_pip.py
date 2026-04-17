import os
import sys
import subprocess


def fix_pycharm_pip():
    """Исправление pip в PyCharm"""

    # Путь к python
    python_path = sys.executable
    print(f"🔍 Используем Python: {python_path}")

    # 1. Обновляем pip глобально
    print("📦 Обновляем pip...")
    subprocess.run([python_path, "-m", "pip", "install", "--upgrade", "pip"])

    # 2. Устанавливаем six явно
    print("📦 Устанавливаем six...")
    subprocess.run([python_path, "-m", "pip", "install", "six==1.16.0"])

    # 3. Проверяем что six установился
    print("🔍 Проверяем six...")
    check_code = """
try:
    import six
    import six.moves
    print("✅ six работает")
except Exception as e:
    print(f"❌ Ошибка: {e}")
"""
    subprocess.run([python_path, "-c", check_code])

    # 4. Устанавливаем PySide6
    print("📦 Устанавливаем PySide6==6.6.0...")
    subprocess.run([python_path, "-m", "pip", "install", "PySide6==6.6.0"])

    print("✅ Готово! Перезапустите PyCharm")


if __name__ == "__main__":
    fix_pycharm_pip()