import os
import sys
import subprocess
import json

def diagnose_python():
    """Диагностика Python установки"""
    
    python_path = r"D:\Program_File_D\My_Python_3.12\python.exe"
    
    print("🔍 Диагностика Python:")
    print("-" * 50)
    
    # Проверка 1: Существует ли файл
    if os.path.exists(python_path):
        print(f"✅ Python найден: {python_path}")
    else:
        print(f"❌ Python НЕ найден: {python_path}")
        return
    
    # Проверка 2: Версия Python
    try:
        result = subprocess.run(
            [python_path, "--version"],
            capture_output=True, text=True
        )
        print(f"✅ Версия: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
    
    # Проверка 3: Pip
    try:
        result = subprocess.run(
            [python_path, "-m", "pip", "--version"],
            capture_output=True, text=True
        )
        print(f"✅ Pip: {result.stdout.split()[1]}")
    except Exception as e:
        print(f"❌ Ошибка pip: {e}")
    
    # Проверка 4: Основные модули
    modules = ["sys", "os", "json", "site"]
    for module in modules:
        result = subprocess.run(
            [python_path, "-c", f"import {module}; print(f'✅ {module}')"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print(f"❌ Модуль {module} не импортируется")
    
    print("-" * 50)

def fix_python_sdk():
    """Создание файла конфигурации для PyCharm"""
    
    project_dir = r"/"
    idea_dir = os.path.join(project_dir, ".idea")
    
    if not os.path.exists(idea_dir):
        os.makedirs(idea_dir)
        print(f"✅ Создана папка .idea")
    
    # Создаем файл misc.xml с конфигурацией SDK
    misc_xml = os.path.join(idea_dir, "misc.xml")
    with open(misc_xml, "w", encoding="utf-8") as f:
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectRootManager" version="2" project-jdk-name="Python 3.12 (My_Python_3.12)" project-jdk-type="Python SDK" />
</project>
''')
    print(f"✅ Создан misc.xml")
    
    # Создаем файл modules.xml
    modules_xml = os.path.join(idea_dir, "modules.xml")
    with open(modules_xml, "w", encoding="utf-8") as f:
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectModuleManager">
    <modules>
      <module fileurl="file://$PROJECT_DIR$/.idea/Yolo_FREL_TOP.REL.iml" filepath="$PROJECT_DIR$/.idea/Yolo_FREL_TOP.REL.iml" />
    </modules>
  </component>
</project>
''')
    
    # Создаем .iml файл
    iml_file = os.path.join(idea_dir, "Yolo_FREL_TOP.REL.iml")
    with open(iml_file, "w", encoding="utf-8") as f:
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<module type="PYTHON_MODULE" version="4">
  <component name="NewModuleRootManager">
    <content url="file://$MODULE_DIR$" />
    <orderEntry type="inheritedJdk" />
    <orderEntry type="sourceFolder" forTests="false" />
  </component>
</module>
''')
    
    print(f"✅ Созданы файлы конфигурации проекта")
    print("\n📋 Теперь откройте проект в PyCharm и вручную укажите интерпретатор:")
    print("   File → Settings → Project → Python Interpreter")
    print("   → Add → Existing environment → Выберите python.exe")

if __name__ == "__main__":
    diagnose_python()
    
    print("\n" + "="*50)
    response = input("Хотите создать конфигурационные файлы для PyCharm? (y/n): ")
    if response.lower() == 'y':
        fix_python_sdk()