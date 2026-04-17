import cv2
import torch
from ultralytics import YOLO
import time
from collections import deque
import numpy as np
import sys
import os
from pathlib import Path
from TheFace_FREL import FaceRecognitionIntegrator  # Импорт модуля распознавания лиц
from LinerDasher_FREL import DrawingUtils  # Импорт утилит
from config import setup_environment
setup_environment()


class FaceDetector:
    """Класс для детекции и распознавания лиц в реальном времени с использованием YOLO"""

    def __init__(self, ui_callback=None, fps_callback=None, camera_info_callback=None, targets_callback=None):
        # Инициализация устройства (GPU/CPU)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")

        # Загрузка модели YOLO для детекции лиц
        self.model_face = YOLO('yolov8n-face.pt')
        self.model_face.to(self.device)

        # Инициализация модуля распознавания лиц
        self.face_recognizer = FaceRecognitionIntegrator("face_database.npy")
        self.recognized_faces = {}  # Словарь для хранения распознанных лиц

        # Словарь для хранения траекторий обнаруженных лиц
        self.trajectories = {}
        self.max_trajectory_length = 20  # Максимальная длина траектории
        self.next_face_id = 1  # Счетчик для присвоения уникальных ID

        # Цвета в формате BGR (для OpenCV) и RGB (для UI)
        self.colors_bgr = [
            (0, 0, 255), (0, 255, 0), (255, 255, 0),
            (0, 255, 255), (255, 0, 255), (0, 165, 255), (128, 0, 128)
        ]
        self.colors_rgb = [
            (255, 0, 0), (0, 255, 0), (0, 255, 255),
            (255, 255, 0), (255, 0, 255), (255, 165, 0), (128, 0, 128)
        ]

        # Переменные для расчета FPS
        self.prev_frame_time = 0
        self.frame_times = deque(maxlen=30)
        self.fps_avg = 0
        self.fps_current = 0
        self.frame_count = 0

        # Параметры фильтров изображения
        self.contrast = 0
        self.brightness = 0
        self.sharpness = 0

        # Колбэки для взаимодействия с UI
        self.fps_callback = fps_callback
        self.camera_info_callback = camera_info_callback
        self.ui_callback = ui_callback
        self.targets_callback = targets_callback

        # Инициализация захвата видео с камеры с обработкой ошибок
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                # Пробуем альтернативные индексы камер
                for i in range(5):  # Проверяем первые 5 камер
                    self.cap = cv2.VideoCapture(i)
                    if self.cap.isOpened():
                        break
        except Exception as e:
            print(f"Ошибка инициализации камеры: {e}")
            self.cap = None

        if not self.cap or not self.cap.isOpened():
            print("Предупреждение: Камера не доступна, но приложение продолжит работу")
            # Создаем заглушку для cap чтобы избежать ошибок
            self.cap = type('DummyCap', (), {
                'isOpened': lambda: False,
                'read': lambda: (False, None),
                'release': lambda: None,
                'get': lambda x: 0
            })()

        # Получение параметров камеры
        self.camera_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.camera_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.camera_fps = int(self.cap.get(cv2.CAP_PROP_FPS))

        # Передача информации о камере через колбэк
        if self.camera_info_callback:
            self.camera_info_callback(self.camera_width, self.camera_height, self.camera_fps)

        self.running = True  # Флаг для управления работой детектора

    def update_filters(self, sharpness, brightness, contrast):
        """Обновление значений фильтров из GUI"""
        self.sharpness = sharpness
        self.brightness = brightness
        self.contrast = contrast

    def apply_filters(self, frame):
        """Применение фильтров к кадру с оптимизацией"""
        # Быстрая проверка - если фильтры не активны, возвращаем исходный кадр
        if self.sharpness == 0 and self.brightness == 0 and self.contrast == 0:
            return frame

        # Применение яркости и контрастности
        if self.brightness != 0 or self.contrast != 0:
            frame = self.adjust_brightness_contrast_fast(frame, self.brightness, self.contrast)

        # Применение резкости
        if self.sharpness != 0:
            frame = self.adjust_sharpness_fast(frame, self.sharpness)

        return frame

    def adjust_brightness_contrast_fast(self, frame, brightness, contrast):
        """Быстрая коррекция яркости и контрастности с использованием LUT"""
        brightness = brightness / 100 * 255
        contrast = (contrast + 100) / 100

        # Создаем Look-Up Table для быстрого преобразования
        lut = np.arange(256, dtype=np.float32)
        lut = lut * contrast + brightness
        lut = np.clip(lut, 0, 255).astype(np.uint8)

        return cv2.LUT(frame, lut)

    def adjust_sharpness_fast(self, frame, sharpness):
        """Оптимизированная коррекция резкости"""
        if sharpness > 0:
            # Упрощенное ядро для увеличения резкости
            kernel = np.array([[0, -1, 0],
                               [-1, 5 + sharpness / 25, -1],
                               [0, -1, 0]], dtype=np.float32)
            return cv2.filter2D(frame, -1, kernel)
        else:
            # Быстрое размытие
            return cv2.GaussianBlur(frame, (5, 5), abs(sharpness) / 50)

    def _get_face_id(self, bbox, current_frame):
        """Присваивает ID лицу на основе его позиции и траектории"""
        x1, y1, x2, y2 = bbox
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        min_distance = float('inf')
        closest_id = None

        # Поиск ближайшего существующего лица по траектории
        for face_id, trajectory in self.trajectories.items():
            if trajectory['positions']:
                last_pos = trajectory['positions'][-1]
                last_center_x = (last_pos[0] + last_pos[2]) / 2
                last_center_y = (last_pos[1] + last_pos[3]) / 2

                distance = np.sqrt((center_x - last_center_x) ** 2 + (center_y - last_center_y) ** 2)

                if distance < 100 and distance < min_distance:
                    min_distance = distance
                    closest_id = face_id

        # Если нашли подходящее существующее лицо - возвращаем его ID
        if closest_id is not None:
            return closest_id

        # Создание нового ID для нового лица
        new_id = self.next_face_id
        self.next_face_id += 1

        # Инициализация данных для нового лица
        self.trajectories[new_id] = {
            'positions': deque(maxlen=self.max_trajectory_length),
            'color_bgr': self.colors_bgr[new_id % len(self.colors_bgr)],
            'color_rgb': self.colors_rgb[new_id % len(self.colors_rgb)],
            'last_seen': current_frame
        }

        return new_id

    def _cleanup_old_faces(self, current_frame):
        """Удаление лиц, которые не обнаруживались в течение длительного времени"""
        faces_to_remove = []
        for face_id, data in self.trajectories.items():
            if current_frame - data['last_seen'] > 30:
                faces_to_remove.append(face_id)

        for face_id in faces_to_remove:
            del self.trajectories[face_id]

    def next_frame(self):
        """Обработка следующего кадра с распознаванием лиц"""
        if not self.cap.isOpened() or not self.running:
            return

        # Чтение кадра
        ret, frame = self.cap.read()
        if not ret:
            return

        # Применение фильтров к кадру
        filtered_frame = self.apply_filters(frame)

        # Детекция лиц
        results = self.model_face(filtered_frame, conf=0.5, verbose=False)# imgsz=640

        # Отладочная информация
        if not self.face_recognizer.known_faces:
            print("⚠️  База данных лиц не загружена!")

        current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        self._cleanup_old_faces(current_frame)

        detected_faces = []
        current_targets = {}

        # Обработка результатов детекции
        if results and results[0].boxes is not None and len(results[0].boxes) > 0:
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                detected_faces.append((x1, y1, x2, y2))

        # Обработка каждого обнаруженного лица
        for bbox in detected_faces:
            x1, y1, x2, y2 = bbox
            face_id = self._get_face_id(bbox, current_frame)

            # Вырезаем область лица для распознавания
            padding = 20
            x1_p = max(0, x1 - padding)
            y1_p = max(0, y1 - padding)
            x2_p = min(filtered_frame.shape[1], x2 + padding)
            y2_p = min(filtered_frame.shape[0], y2 + padding)

            face_roi = filtered_frame[y1_p:y2_p, x1_p:x2_p]

            if face_roi.size == 0:
                continue

            # Распознаем лицо
            name, recognition_score, final_face_id = self.face_recognizer.debug_recognition(face_roi, face_id)

            # Определяем цвет и стиль рамки
            color_bgr = self.trajectories[face_id]['color_bgr']

            if name != "unknown" and recognition_score > 0:
                self.recognized_faces[face_id] = name
                display_name = f"{name} (ID: {face_id})"
                # Используем утилиту для рисования пунктирной рамки
                DrawingUtils.printer_punktirnoy_linii(filtered_frame, x1, y1, x2, y2, color_bgr)
            else:
                display_name = f"ID: {face_id}"
                cv2.rectangle(filtered_frame, (x1, y1), (x2, y2), color_bgr, 2)

            # Добавление позиции в траекторию
            self.trajectories[face_id]['positions'].append(bbox)
            self.trajectories[face_id]['last_seen'] = current_frame

            # Подготовка данных для UI
            current_targets[face_id] = {
                'bbox': (x1, y1, x2 - x1, y2 - y1),
                'color': self.trajectories[face_id]['color_rgb'],
                'name': display_name
            }

            # Отображение имени/ID
            cv2.putText(filtered_frame, display_name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_bgr, 2)

            # Отрисовка траектории
            positions = list(self.trajectories[face_id]['positions'])
            for i in range(1, len(positions)):
                prev_x1, prev_y1, prev_x2, prev_y2 = positions[i - 1]
                curr_x1, curr_y1, curr_x2, curr_y2 = positions[i]
                prev_center = ((prev_x1 + prev_x2) // 2, (prev_y1 + prev_y2) // 2)
                curr_center = ((curr_x1 + curr_x2) // 2, (curr_y1 + curr_y2) // 2)
                cv2.line(filtered_frame, prev_center, curr_center, color_bgr, 2)

        # Передача данных в UI
        if self.targets_callback:
            self.targets_callback(current_targets)

        # Расчет FPS
        current_time = time.time()
        if self.prev_frame_time > 0:
            frame_time = current_time - self.prev_frame_time
            self.fps_current = 1.0 / frame_time if frame_time > 0 else 0
            self.frame_times.append(frame_time)

            if self.frame_times:
                self.fps_avg = len(self.frame_times) / sum(self.frame_times)

            if self.fps_callback:
                self.fps_callback(f"{self.fps_avg:.1f}", str(len(detected_faces)))

        self.prev_frame_time = current_time
        self.frame_count += 1

        if self.ui_callback:
            self.ui_callback(filtered_frame)

    def stop(self):
        """Остановка детектора и освобождение ресурсов"""
        self.running = False
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()


class VideoProcessor:
    """Класс для обработки видео файлов с распознаванием лиц"""

    def __init__(self, video_path):
        self.video_path = video_path
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model_face = YOLO('yolov8n-face.pt')
        self.model_face.to(self.device)
        self.face_recognizer = FaceRecognitionIntegrator("face_database.npy")
        self.recognized_faces = {}
        self.processing = False
        self.progress = 0
        self.processed_frames = 0
        self.total_frames = 0
        self.cap = None
        self.out = None

    def process_video(self):
        """Обработка видео файла"""
        if not os.path.exists(self.video_path):
            raise Exception("Файл не найден")

        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            raise Exception("Не удалось открыть видео файл")

        # Получение параметров видео
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Создание выходного файла
        output_path = self._get_output_path()
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        self.processing = True
        self.progress = 0
        self.processed_frames = 0

        # Обрабатываем кадры
        while self.processing:
            ret, frame = self.cap.read()
            if not ret:
                break

            # Обработка кадра
            processed_frame = self._process_frame(frame)
            self.out.write(processed_frame)
            self.processed_frames += 1

            # Расчет прогресса
            if self.total_frames > 0:
                self.progress = min(100, int((self.processed_frames / self.total_frames) * 100))
            else:
                self.progress = 0

            if self.progress >= 100:
                self.processing = False
                break

        self.progress = 100
        self.stop_processing()
        return output_path

    def stop_processing(self):
        """Остановить обработку"""
        self.processing = False
        if self.cap:
            self.cap.release()
        if self.out:
            self.out.release()

    def get_progress(self):
        """Получить текущий прогресс"""
        return self.progress

    def _process_frame(self, frame):
        """Обработка одного кадра с распознаванием лиц"""
        results = self.model_face(frame, conf=0.5, verbose=False)

        if results and results[0].boxes is not None:
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                confidence = box.conf[0].cpu().numpy()

                # Вырезаем область лица для распознавания
                padding = 20
                x1_p = max(0, x1 - padding)
                y1_p = max(0, y1 - padding)
                x2_p = min(frame.shape[1], x2 + padding)
                y2_p = min(frame.shape[0], y2 + padding)

                face_roi = frame[y1_p:y2_p, x1_p:x2_p]

                if face_roi.size > 0:
                    # Распознаем лицо
                    name, score, _ = self.face_recognizer.recognize_face(face_roi, 0)
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2

                    if name != "unknown" and score > 0:
                        color = (94, 255, 0)  # Зеленый цвет
                        label = f"{name}: {score:.2f}"
                        # Используем утилиту для рисования пунктирной рамки
                        DrawingUtils.printer_punktirnoy_linii(frame, x1, y1, x2, y2, color)

                    else:
                        color = (250, 0, 170)  # Фиолетовый для нераспознанных
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        label = f"Face: {confidence:.2f}"

                    # Добавление текста и меток
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    coord_label = f"Center: ({center_x}px, {center_y}px)"
                    cv2.putText(frame, coord_label, (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.circle(frame, (center_x, center_y), 5, color, -1)

        return frame

    def _get_output_path(self):
        """Генерация пути для выходного файла"""
        path = Path(self.video_path)
        output_path = path.parent / f"{path.stem}_processed{path.suffix}"
        return str(output_path)
