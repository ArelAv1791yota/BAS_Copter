import torch
import ultralytics
import cv2
import numpy as np
import sys

print(f"Python: {sys.version}")
print(f"PyTorch: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Ultralytics: {ultralytics.__version__}")
print(f"OpenCV: {cv2.__version__}")
print(f"NumPy: {np.__version__}")

# Проверка загрузки модели
try:
    from ultralytics import YOLO
    model = YOLO('yolov8n-face.pt')
    print("✅ Модель загружена успешно")
except Exception as e:
    print(f"❌ Ошибка загрузки модели: {e}")