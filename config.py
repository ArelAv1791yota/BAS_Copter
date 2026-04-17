# config.py
import os
import sys
import cv2

def setup_environment():
    """Настройка окружения для совместимости"""
    # Отключение torch._numpy для PyInstaller
    os.environ['NUMPY_EXPERIMENTAL_ARRAY_FUNCTION'] = '0'
    os.environ['TORCH_NUMPY_DISABLE'] = '1'
    os.environ['TORCH_DISABLE_NUMPY'] = '1'
    os.environ['USE_TORCH_NUMPY'] = '0'
    
    # Фиксы камеры
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    os.environ['PATH'] = base_path + os.pathsep + os.environ['PATH']
    
    # Принудительная загрузка стандартного numpy
    import numpy as np
    
    # Фикс для torch._numpy
    try:
        import torch._numpy
        if hasattr(torch._numpy, '_ufuncs'):
            try:
                ufuncs_module = torch._numpy._ufuncs
                if not hasattr(ufuncs_module, 'name'):
                    ufuncs_module.name = "torch_numpy_ufuncs"
            except:
                pass
    except ImportError:
        pass

def get_cascade_path(cascade_name='haarcascade_frontalface_default.xml'):
    """Получение пути к cascade файлам"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        possible_paths = [
            os.path.join(base_path, 'cv2', 'data', cascade_name),
            os.path.join(base_path, 'data', cascade_name),
            os.path.join(base_path, cascade_name)
        ]
    else:
        base_path = os.path.dirname(__file__)
        possible_paths = [
            os.path.join(cv2.data.haarcascades, cascade_name),
            os.path.join(base_path, 'data', cascade_name),
            os.path.join(base_path, cascade_name)
        ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return possible_paths[-1]