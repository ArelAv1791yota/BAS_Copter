import os
import subprocess


def verify_final():
    """Финальная проверка"""

    helpers = r"D:\Program_File_D\PyCharm 2023.3.4\plugins\python\helpers"
    expected_pip = os.path.join(helpers, "pip-20.3.4-py2.py3-none-any.whl")

    print("🔍 Финальная проверка:")
    print("-" * 50)

    # Проверяем наличие всех необходимых файлов
    required_files = [
        (os.path.join(expected_pip, "pip", "__init__.py"), "pip/__init__.py"),
        (os.path.join(expected_pip, "setup.py"), "setup.py"),
        (os.path.join(expected_pip, "pyproject.toml"), "pyproject.toml"),
        (os.path.join(helpers, "packaging_tool.py"), "packaging_tool.py"),
        (os.path.join(helpers, "pip", "__init__.py"), "корневой pip/__init__.py")
    ]

    all_ok = True
    for file_path, description in required_files:
        if os.path.exists(file_path):
            print(f"✅ {description} - найден")
        else:
            print(f"❌ {description} - НЕ найден")
            all_ok = False

    if all_ok:
        print("\n✅ Все необходимые файлы на месте!")

        # Проверяем что pip работает
        try:
            result = subprocess.run(
                [r"D:\Program_File_D\My_Python_3.12\python.exe", "-c",
                 "import pip; print(f'Pip версия: {pip.__version__}')"],
                capture_output=True, text=True
            )
            print(f"\n📦 {result.stdout.strip()}")
        except:
            pass
    else:
        print("\n❌ Некоторые файлы отсутствуют")


if __name__ == "__main__":
    verify_final()