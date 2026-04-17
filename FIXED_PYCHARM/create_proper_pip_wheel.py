import os
import shutil
import subprocess
import zipfile
from pathlib import Path

def create_proper_pip_wheel():
    """Создание правильного wheel файла вместо папки"""
    
    pycharm_helpers = r"D:\Program_File_D\PyCharm 2023.3.4\plugins\python\helpers"
    python_path = r"D:\Program_File_D\My_Python_3.12\python.exe"
    
    # Имя, которое ожидает PyCharm (оставим как файл .whl, а не папку)
    expected_pip_name = "pip-20.3.4-py2.py3-none-any.whl"
    expected_path = os.path.join(pycharm_helpers, expected_pip_name)
    
    print(f"🔧 Создаем правильный wheel файл...")
    
    # 1. Удаляем старую папку если она есть
    if os.path.exists(expected_path):
        if os.path.isdir(expected_path):
            print(f"🗑️ Удаляем старую папку...")
            shutil.rmtree(expected_path)
        else:
            print(f"🗑️ Удаляем старый файл...")
            os.remove(expected_path)
    
    # 2. Скачиваем свежий pip wheel
    print("📥 Скачиваем pip 24.0...")
    subprocess.run([
        python_path, "-m", "pip", "download",
        "pip==24.0",
        "--dest", pycharm_helpers,
        "--no-deps"
    ])
    
    # 3. Находим скачанный wheel
    wheel_files = list(Path(pycharm_helpers).glob("pip-*.whl"))
    if not wheel_files:
        print("❌ Не удалось скачать pip")
        return
    
    new_wheel = wheel_files[0]
    print(f"✅ Скачан: {new_wheel.name}")
    
    # 4. Переименовываем его в ожидаемое имя
    expected_file = os.path.join(pycharm_helpers, expected_pip_name)
    print(f"📋 Переименовываем в {expected_pip_name}...")
    
    # Если файл с таким именем уже существует, удаляем
    if os.path.exists(expected_file):
        os.remove(expected_file)
    
    # Переименовываем
    shutil.move(str(new_wheel), expected_file)
    
    # 5. Создаем packaging_tool.py который будет использовать системный pip
    packaging_tool_path = os.path.join(pycharm_helpers, "packaging_tool.py")
    with open(packaging_tool_path, "w", encoding="utf-8") as f:
        f.write('''#!/usr/bin/env python
"""Packaging tool for PyCharm - использует системный pip"""

import sys
import subprocess
import json
import os

# Путь к системному Python
PYTHON_PATH = r"D:\\Program_File_D\\My_Python_3.12\\python.exe"

def main():
    if len(sys.argv) < 2:
        print("Usage: packaging_tool.py <command>")
        return 1
    
    command = sys.argv[1]
    
    if command == "list":
        # Используем системный pip вместо встроенного
        result = subprocess.run(
            [PYTHON_PATH, "-m", "pip", "list", "--format=json"],
            capture_output=True, text=True
        )
        print(result.stdout)
        return result.returncode
    
    elif command == "install":
        if len(sys.argv) < 3:
            print("Package name required")
            return 1
        package = sys.argv[2]
        result = subprocess.run(
            [PYTHON_PATH, "-m", "pip", "install", package],
            capture_output=True, text=True
        )
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        return result.returncode
    
    elif command == "uninstall":
        if len(sys.argv) < 3:
            print("Package name required")
            return 1
        package = sys.argv[2]
        result = subprocess.run(
            [PYTHON_PATH, "-m", "pip", "uninstall", "-y", package],
            capture_output=True, text=True
        )
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        return result.returncode
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
''')
    print(f"✅ packaging_tool.py обновлен (использует системный pip)")
    
    # 6. Проверяем результат
    if os.path.exists(expected_file):
        size = os.path.getsize(expected_file) / (1024 * 1024)
        print(f"\n✅ Файл создан: {expected_pip_name} ({size:.2f} MB)")
    
    print("\n✅ Готово! Теперь перезапустите PyCharm")

if __name__ == "__main__":
    input("⚠️ Убедитесь что PyCharm ЗАКРЫТ и нажмите Enter...")
    create_proper_pip_wheel()