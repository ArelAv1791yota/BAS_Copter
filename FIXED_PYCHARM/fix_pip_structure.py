import os
import shutil
import subprocess
import zipfile
from pathlib import Path


def fix_pip_final():
    """Финальное исправление структуры pip"""

    pycharm_helpers = r"D:\Program_File_D\PyCharm 2023.3.4\plugins\python\helpers"
    python_path = r"D:\Program_File_D\My_Python_3.12\python.exe"

    # Имя, которое ожидает PyCharm
    expected_pip_name = "pip-20.3.4-py2.py3-none-any.whl"
    expected_path = os.path.join(pycharm_helpers, expected_pip_name)

    print(f"🔧 Создаем правильную структуру в {expected_pip_name}...")

    # 1. Полностью удаляем старую папку
    if os.path.exists(expected_path):
        print(f"🗑️ Удаляем старую папку...")
        shutil.rmtree(expected_path)

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

    wheel_path = wheel_files[0]
    print(f"✅ Скачан: {wheel_path.name}")

    # 4. Распаковываем wheel в ожидаемую папку
    print(f"📦 Распаковываем в {expected_pip_name}...")
    with zipfile.ZipFile(wheel_path, 'r') as zip_ref:
        zip_ref.extractall(expected_path)

    # 5. Удаляем wheel файл
    wheel_path.unlink()

    # 6. Проверяем структуру
    print("\n🔍 Проверка структуры:")

    # Должна быть папка pip внутри
    pip_inner = os.path.join(expected_path, "pip")
    if os.path.exists(pip_inner) and os.path.isdir(pip_inner):
        print(f"✅ Найдена папка pip/")

        # Проверяем __init__.py
        init_file = os.path.join(pip_inner, "__init__.py")
        if os.path.exists(init_file):
            print(f"✅ Найден pip/__init__.py")
        else:
            print(f"❌ Нет pip/__init__.py")

        # Проверяем setup.py (нужен для установки)
        setup_file = os.path.join(expected_path, "setup.py")
        if not os.path.exists(setup_file):
            # Создаем простой setup.py для совместимости
            with open(setup_file, "w") as f:
                f.write('''from setuptools import setup, find_packages

setup(
    name="pip",
    version="24.0",
    packages=find_packages(),
    description="The PyPA recommended tool for installing Python packages.",
)
''')
            print(f"✅ Создан setup.py")
    else:
        print(f"❌ Не найдена папка pip/ в распакованном архиве")

        # Ищем pip где-то в распакованных файлах
        for root, dirs, files in os.walk(expected_path):
            if 'pip' in dirs:
                found_pip = os.path.join(root, 'pip')
                print(f"🔍 Найдена папка pip в: {found_pip}")
                # Перемещаем её наверх
                shutil.move(found_pip, os.path.join(expected_path, 'pip'))
                break

    # 7. Создаем packaging_tool.py
    packaging_tool_path = os.path.join(pycharm_helpers, "packaging_tool.py")
    with open(packaging_tool_path, "w", encoding="utf-8") as f:
        f.write('''#!/usr/bin/env python
"""Packaging tool for PyCharm"""

import sys
import subprocess
import json
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: packaging_tool.py <command>")
        return 1

    command = sys.argv[1]

    if command == "list":
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=json"],
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
            [sys.executable, "-m", "pip", "install", package],
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
            [sys.executable, "-m", "pip", "uninstall", "-y", package],
            capture_output=True, text=True
        )
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        return result.returncode

    return 0

if __name__ == "__main__":
    sys.exit(main())
''')
    print(f"✅ packaging_tool.py обновлен")

    # 8. Создаем pyproject.toml для совместимости
    pyproject_path = os.path.join(expected_path, "pyproject.toml")
    with open(pyproject_path, "w") as f:
        f.write('''[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "pip"
version = "24.0"
description = "The PyPA recommended tool for installing Python packages."
''')
    print(f"✅ pyproject.toml создан")

    # 9. Создаем символическую ссылку на pip в корне helpers
    pip_link = os.path.join(pycharm_helpers, "pip")
    if os.path.exists(pip_link):
        shutil.rmtree(pip_link)

    # Копируем папку pip из распакованного архива
    source_pip = os.path.join(expected_path, "pip")
    if os.path.exists(source_pip):
        shutil.copytree(source_pip, pip_link)
        print(f"✅ Папка pip скопирована в корень helpers")

    print("\n✅ Готово! Теперь перезапустите PyCharm")
    print("\n📋 Итоговая структура:")
    print(f"   {pycharm_helpers}/")
    print(f"   ├── {expected_pip_name}/")
    print(f"   │   ├── pip/")
    print(f"   │   │   └── __init__.py")
    print(f"   │   ├── setup.py")
    print(f"   │   └── pyproject.toml")
    print(f"   ├── pip/ (копия из {expected_pip_name}/pip)")
    print(f"   └── packaging_tool.py")


if __name__ == "__main__":
    input("⚠️ Убедитесь что PyCharm ЗАКРЫТ и нажмите Enter...")
    fix_pip_final()