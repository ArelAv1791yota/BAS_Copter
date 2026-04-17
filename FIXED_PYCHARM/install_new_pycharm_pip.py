import os
import shutil
import subprocess
import sys
from pathlib import Path


def copy_system_pip_to_pycharm():
    """Копирование системного pip в PyCharm"""

    pycharm_helpers = r"D:\Program_File_D\PyCharm 2023.3.4\plugins\python\helpers"
    python_path = r"D:\Program_File_D\My_Python_3.12\python.exe"

    print("🔍 Находим системный pip...")

    # Получаем путь к системному pip
    result = subprocess.run(
        [python_path, "-c", "import pip; print(pip.__path__[0])"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        system_pip_path = result.stdout.strip()
        print(f"📁 Системный pip находится в: {system_pip_path}")

        # Определяем версию pip
        version_result = subprocess.run(
            [python_path, "-m", "pip", "--version"],
            capture_output=True,
            text=True
        )
        pip_version = version_result.stdout.split()[1] if version_result.stdout else "unknown"
        print(f"📦 Версия pip: {pip_version}")

        # Создаем имя для папки в PyCharm
        pycharm_pip_name = f"pip-{pip_version}-py3-none-any.whl"
        pycharm_pip_path = os.path.join(pycharm_helpers, pycharm_pip_name)

        # Копируем pip в PyCharm
        print(f"📋 Копируем pip в PyCharm...")
        if os.path.exists(pycharm_pip_path):
            shutil.rmtree(pycharm_pip_path)

        shutil.copytree(system_pip_path, pycharm_pip_path)
        print(f"✅ Pip скопирован в: {pycharm_pip_path}")

        # Также копируем pip-кэш если есть
        pip_cache = os.path.join(os.path.dirname(system_pip_path), 'pip')
        if os.path.exists(pip_cache):
            pycharm_pip_cache = os.path.join(pycharm_helpers, 'pip')
            if os.path.exists(pycharm_pip_cache):
                shutil.rmtree(pycharm_pip_cache)
            shutil.copytree(pip_cache, pycharm_pip_cache)
            print(f"✅ Pip cache скопирован")

        print("\n✅ Готово! Теперь перезапустите PyCharm")
    else:
        print("❌ Не удалось найти системный pip")


if __name__ == "__main__":
    input("⚠️ Убедитесь что PyCharm ЗАКРЫТ и нажмите Enter...")
    copy_system_pip_to_pycharm()