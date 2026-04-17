import os
import shutil

def fix_packaging_tool():
    """Исправление packaging_tool.py для обработки None значений"""
    
    pycharm_helpers = r"D:\Program_File_D\PyCharm 2023.3.4\plugins\python\helpers"
    packaging_tool_path = os.path.join(pycharm_helpers, "packaging_tool.py")
    
    # Создаем бэкап
    backup_path = packaging_tool_path + ".backup"
    if os.path.exists(packaging_tool_path):
        shutil.copy2(packaging_tool_path, backup_path)
        print(f"✅ Создан бэкап: {backup_path}")
    
    # Читаем текущий файл
    with open(packaging_tool_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Находим функцию do_list и заменяем проблемную строку
    old_line = "    sys.stdout.write('\\t'.join([pkg.name, pkg.version, str(pkg._path.parent), requires])+chr(10))"
    new_line = "    sys.stdout.write('\\t'.join([str(pkg.name or ''), str(pkg.version or ''), str(pkg._path.parent if hasattr(pkg, '_path') else ''), requires or ''])+chr(10))"
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        print("✅ Проблемная строка заменена")
    else:
        print("⚠️ Проблемная строка не найдена, ищем альтернативу...")
        # Ищем похожую строку
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'pkg.name' in line and 'pkg.version' in line:
                print(f"🔍 Найдена строка {i+1}: {line.strip()}")
                # Заменяем эту строку
                indent = ' ' * (len(line) - len(line.lstrip()))
                lines[i] = indent + "sys.stdout.write('\\t'.join([str(pkg.name or ''), str(pkg.version or ''), str(pkg._path.parent if hasattr(pkg, '_path') else ''), requires or ''])+chr(10))"
                content = '\n'.join(lines)
                print("✅ Строка заменена")
                break
    
    # Добавляем обработку ошибок в начало файла
    if 'import sys' in content:
        # Добавляем импорт traceback если его нет
        if 'import traceback' not in content:
            content = content.replace('import sys', 'import sys\nimport traceback')
    
    # Добавляем try-except в main
    if 'def main():' in content:
        main_start = content.find('def main():')
        next_line = content.find('\n', main_start) + 1
        indent = content[next_line:].split('(')[0].count(' ') if content[next_line:].strip() else 4
        
        # Вставляем try-except
        try_block = f"""def main():
    try:
        return _main()
    except Exception as e:
        sys.stderr.write(f"Error in packaging tool: {{e}}\\n")
        traceback.print_exc()
        return 1

def _main():
"""
        content = content.replace('def main():', try_block, 1)
        print("✅ Добавлена обработка ошибок")
    
    # Сохраняем исправленный файл
    with open(packaging_tool_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Файл {packaging_tool_path} исправлен")
    print("🔄 Перезапустите PyCharm")

if __name__ == "__main__":
    input("⚠️ Убедитесь что PyCharm ЗАКРЫТ и нажмите Enter...")
    fix_packaging_tool()