import os
import shutil
import subprocess
import sys
from pathlib import Path

def fix_pycharm_helpers():
    """Полное исправление helpers для PyCharm"""
    
    pycharm_helpers = r"D:\Program_File_D\PyCharm 2023.3.4\plugins\python\helpers"
    python_path = r"D:\Program_File_D\My_Python_3.12\python.exe"
    
    print("🔧 Начинаем полное восстановление helpers...")
    
    # 1. Проверяем существование папки helpers
    if not os.path.exists(pycharm_helpers):
        os.makedirs(pycharm_helpers)
    
    # 2. Устанавливаем правильную версию pip через системный pip
    print("📦 Устанавливаем pip 24.0...")
    subprocess.run([
        python_path, "-m", "pip", "install", "pip==24.0"
    ])
    
    # 3. Получаем путь к установленному pip
    result = subprocess.run(
        [python_path, "-c", 
         "import pip; import os; print(os.path.dirname(pip.__file__))"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        system_pip_path = result.stdout.strip()
        print(f"📁 Системный pip: {system_pip_path}")
        
        # 4. Создаем правильную структуру в helpers
        # PyCharm ожидает папку с именем pip-{version}-py3-none-any.whl
        pip_version = "24.0"
        pycharm_pip_name = f"pip-{pip_version}-py3-none-any.whl"
        pycharm_pip_path = os.path.join(pycharm_helpers, pycharm_pip_name)
        
        # Удаляем старую если есть
        if os.path.exists(pycharm_pip_path):
            shutil.rmtree(pycharm_pip_path)
        
        # Копируем системный pip
        print(f"📋 Копируем pip в {pycharm_pip_path}...")
        shutil.copytree(system_pip_path, pycharm_pip_path)
        
        # 5. Создаем символическую ссылку или копию для packaging_tool.py
        # Находим packaging_tool.py в системных пакетах PyCharm? Нет, его нужно создать
        
        # Создаем простой packaging_tool.py
        packaging_tool_content = '''#!/usr/bin/env python
"""Packaging tool for PyCharm"""

import sys
import subprocess
import json

def main():
    """Main function for packaging tool"""
    if len(sys.argv) < 2:
        print("Usage: packaging_tool.py <command>")
        return 1
    
    command = sys.argv[1]
    
    if command == "list":
        # Get list of installed packages
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=json"],
            capture_output=True,
            text=True
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
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        return result.returncode
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
        
        packaging_tool_path = os.path.join(pycharm_helpers, "packaging_tool.py")
        with open(packaging_tool_path, "w", encoding="utf-8") as f:
            f.write(packaging_tool_content)
        print(f"✅ Создан {packaging_tool_path}")
        
        # 6. Создаем ссылку на pip в корне helpers для обратной совместимости
        pip_link_path = os.path.join(pycharm_helpers, "pip")
        if os.path.exists(pip_link_path):
            shutil.rmtree(pip_link_path)
        
        # Копируем вместо ссылки для надежности
        shutil.copytree(system_pip_path, pip_link_path)
        print(f"✅ Создан {pip_link_path}")
        
        print("\n✅ Готово! Теперь перезапустите PyCharm")
        print("\n📋 Итоговая структура папок:")
        print(f"   {pycharm_helpers}/")
        print(f"   ├── {pycharm_pip_name}/")
        print(f"   ├── pip/")
        print(f"   └── packaging_tool.py")
        
    else:
        print("❌ Не удалось найти системный pip")

if __name__ == "__main__":
    input("⚠️ Убедитесь что PyCharm ЗАКРЫТ и нажмите Enter...")
    fix_pycharm_helpers()