import urllib.request
import os


def download_model_direct():
    """Прямое скачивание модели через urllib"""

    url = "https://github.com/akanametov/yolov8-face/releases/download/v0.0.0/yolov8n-face.pt"
    filename = "yolov8n-face.pt"

    print(f"📥 Скачиваем модель с {url}")

    # Скачиваем с прогресс-баром
    def progress_hook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(100, downloaded * 100 / total_size)
            print(f"\rПрогресс: {percent:.1f}%", end="")

    urllib.request.urlretrieve(url, filename, progress_hook)
    print(f"\n✅ Модель скачана: {filename}")

    # Проверяем размер файла
    size = os.path.getsize(filename) / (1024 * 1024)
    print(f"Размер файла: {size:.2f} MB")


if __name__ == "__main__":
    download_model_direct()