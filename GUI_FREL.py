from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QFrame, QFileDialog, QProgressBar, QMessageBox)
import sys
import os
import numpy as np
import time
import cv2
from UI_GUI_FREL import Ui_Form
from AI_YOLO_FREL import FaceDetector, VideoProcessor
import threading
from collections import deque
from CreateNPY_FREL import CreateNPYWindow
from config import setup_environment
setup_environment()


class TargetWidget(QFrame):
    """Виджет для отображения информации об отдельной цели (лице)"""

    def __init__(self, target_id, x, y, width, height, color, name="", parent=None):
        super().__init__(parent)
        self.target_id = target_id

        # Настройка внешнего вида рамки
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(1)
        self.setMaximumHeight(100)  # Увеличиваем высоту для имени

        # Основной layout виджета
        layout = QVBoxLayout(self)

        # Заголовок с ID цели и именем
        header_layout = QHBoxLayout()
        if name:
            self.id_label = QLabel(f"{name}")
        else:
            self.id_label = QLabel(f"Цель ID: {target_id}")
        self.id_label.setStyleSheet(f"color: rgb{color}; font-weight: bold; font-size: 12pt;")
        header_layout.addWidget(self.id_label)
        layout.addLayout(header_layout)

        # Строка с координаты
        coords_layout = QHBoxLayout()
        coords_layout.addWidget(QLabel("Координаты:"))
        self.coords_label = QLabel(f"({x}, {y})")
        coords_layout.addWidget(self.coords_label)
        layout.addLayout(coords_layout)

        # Строка с размерами
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Размер:"))
        self.size_label = QLabel(f"{width}×{height} px")
        size_layout.addWidget(self.size_label)
        layout.addLayout(size_layout)


class MainWindow(QWidget):
    """Главное окно приложения с видеопотоком и информацией о целях"""

    # Новые сигналы
    processing_complete_signal = Signal(str)
    processing_error_signal = Signal(str)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Загрузка пользовательского интерфейса
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("BAS_ARELERIO")

        # Добавьте этот атрибут в __init__ после инициализации UI
        self.database_window = None

        # Устанавливаем минимальный размер вместо фиксированного
        self.setMinimumSize(1600, 740)  # Минимальный размер
        self.setMaximumSize(1600, 740)  # Убираем фиксированный максимальный размер

        # Добавляем обработку двойного клика для полноэкранного режима
        self.ui.l_video.mouseDoubleClickEvent = self.toggle_fullscreen

        # Добавляем горячую клавишу Esc для выхода из полноэкранного режима
        self.setFocusPolicy(Qt.StrongFocus)

        # Инициализация переменных для фильтра
        self.sharpness = 0
        self.brightness = 0
        self.contrast = 0

        # Инициализация переменных для хранения данных
        self.current_fps = "0"
        self.fps_AVG = "0"
        self.camera_width = "0"
        self.camera_height = "0"
        self.camera_fps = "0"

        # Словарь для хранения виджетов целей
        self.target_widgets = {}

        # Инициализация детектора как None
        self.face_detector = None
        self.video_processor = None
        self.processing_thread = None
        self.video_capture = None  # Для воспроизведения видео файлов
        self.current_video_path = None
        self.video_processing_timer = None

        # Создаем layout для l_video
        self.video_layout = QVBoxLayout()
        self.ui.l_video.setLayout(self.video_layout)

        # Флаг для отслеживания состояния камеры
        self.camera_active = False

        # Подключение кнопок
        self.ui.pB_DataBase.clicked.connect(self.open_database_creator)
        self.ui.pB_clFil.clicked.connect(self.reset_filters)
        self.ui.pB_translationCam.clicked.connect(self.toggle_camera)
        self.ui.pB_saveVid.clicked.connect(self.process_video_file)
        self.ui.pB_openVid.clicked.connect(self.open_video_file)
        self.ui.pB_translationVid.clicked.connect(self.start_video_stream_processing)

        # Настройка слайдеров фильтров
        self.setup_sliders()

        # Установка начального текста
        self.show_waiting_message()

        # Таймер для проверки состояния камеры
        self.camera_check_timer = QTimer(self)
        self.camera_check_timer.timeout.connect(self.check_camera_status)
        self.camera_check_timer.start(1000)

        # Таймер для воспроизведения видео файлов
        self.video_timer = QTimer(self)
        self.video_timer.timeout.connect(self.play_video_frame)

        # Подключение сигналов
        self.processing_complete_signal.connect(self.processing_complete)
        self.processing_error_signal.connect(self.show_processing_error)

        # Таймер для обновления прогресса
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress_display)

        # Переменные для управления видео
        self.is_video_playing = False
        self.video_duration = 0
        self.video_position = 0
        self.current_mode = None  # 'camera', 'video_playback', 'video_processing'
        self.retry_mode = False  # Флаг режима повторного воспроизведения

        # Подключение кнопок управления видео
        self.ui.pB_play_pause.clicked.connect(self.toggle_play_pause)
        self.ui.pB_rewind_5s.clicked.connect(lambda: self.seek_video(-5))
        self.ui.pB_rewind_10s.clicked.connect(lambda: self.seek_video(-10))
        self.ui.pB_forward_5s.clicked.connect(lambda: self.seek_video(5))
        self.ui.pB_forward_10s.clicked.connect(lambda: self.seek_video(10))
        self.ui.pB_rewind_10s.setText("⏪")
        self.ui.pB_rewind_5s.setText("◀◀")
        self.ui.pB_forward_5s.setText("▶▶")
        self.ui.pB_forward_10s.setText("⏩")

        # Обработчики для слайдера
        self.ui.video_slider.sliderPressed.connect(self.slider_pressed)
        self.ui.video_slider.sliderReleased.connect(self.slider_released)
        self.ui.video_slider.valueChanged.connect(self.slider_changed)

    def open_database_creator(self):
        """Открытие окна создания базы данных"""
        # Закрываем предыдущее окно если оно открыто
        if self.database_window is not None:
            self.database_window.close()
            self.database_window = None

        # Создаем новое окно
        self.database_window = CreateNPYWindow(self)
        self.database_window.setWindowFlags(Qt.Window)  # Делаем полноценным окном
        self.database_window.show()
    def toggle_fullscreen(self, event=None):
        """Переключение полноэкранного режима"""
        if self.isFullScreen():
            self.showNormal()
            # Восстанавливаем кнопки управления при выходе из полноэкранного режима
            if hasattr(self, 'fullscreen_controls_visible'):
                self.show_video_controls(self.fullscreen_controls_visible)
        else:
            # Запоминаем видимость контролов перед переходом в полноэкранный режим
            self.fullscreen_controls_visible = self.ui.video_control_container.isVisible()
            self.showFullScreen()
            # Скрываем контролы в полноэкранном режиме (появляются при наведении)
            self.show_video_controls(False)

    def keyPressEvent(self, event):
        """Обработка нажатий клавиш"""
        if event.key() == Qt.Key_Escape and self.isFullScreen():
            self.showNormal()
            # Восстанавливаем видимость контролов
            if hasattr(self, 'fullscreen_controls_visible'):
                self.show_video_controls(self.fullscreen_controls_visible)
        elif event.key() == Qt.Key_F11:
            self.toggle_fullscreen()
        else:
            super().keyPressEvent(event)

    def enterEvent(self, event):
        """Показываем контролы при наведении в полноэкранном режиме"""
        if self.isFullScreen():
            self.show_video_controls(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Скрываем контролы при уходе курсора в полноэкранном режиме"""
        if self.isFullScreen():
            # Небольшая задержка перед скрытием
            QTimer.singleShot(1000, self.hide_fullscreen_controls)
        super().leaveEvent(event)

    def hide_fullscreen_controls(self):
        """Скрытие контролов в полноэкранном режиме"""
        if self.isFullScreen() and not self.ui.video_control_container.underMouse():
            self.show_video_controls(False)

    def start_video_stream_processing(self):
        """Запуск обработки видео файла в реальном времени (как поток с камеры)"""
        # Останавливаем камеру если она активна
        if self.camera_active:
            self.stop_camera()

        # Очищаем интерфейс перед обработкой
        self.clear_interface()
        # НЕ показываем панель управления сразу - только после выбора файла
        self.show_video_controls(False)
        # Разблокируем фильтры
        self.set_filters_enabled(True)

        # Останавливаем все другие процессы
        self.stop_all_processing()
        self.current_mode = None  # Пока не установлен режим

        # Выбираем файл для обработки
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите видео файл для потоковой обработки",
            "",
            "Video Files (*.mp4)"
        )

        if file_path:
            self.current_video_path = file_path
            self.current_mode = 'video_processing'  # Устанавливаем режим только после выбора файла
            self.setup_video_stream_processing()
            # Теперь показываем панель управления после успешного выбора файла
            self.show_video_controls(True)
        else:
            # Если пользователь отменил выбор файла, возвращаем в исходное состояние
            self.show_waiting_message()

    def save_detector_state(self):
        """Сохранение состояния детектора"""
        if not self.face_detector:
            return None, 1

        return self.face_detector.trajectories.copy(), self.face_detector.next_face_id

    def restore_detector_state(self, trajectories, next_face_id):
        """Восстановление состояния детектора"""
        if not self.face_detector:
            return

        self.face_detector.trajectories = trajectories
        self.face_detector.next_face_id = next_face_id

    def setup_video_stream_processing(self):
        """Настройка обработки видео файла в реальном времени с адаптивным таймером"""
        try:
            # Открываем видео файл
            self.video_capture = cv2.VideoCapture(self.current_video_path)
            if not self.video_capture.isOpened():
                raise Exception("Не удалось открыть видео файл")

            # Получаем параметры видео
            width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(self.video_capture.get(cv2.CAP_PROP_FPS))

            # Сохраняем оригинальный FPS видео
            self.original_video_fps = fps

            # Обновляем информацию о видео в интерфейсе
            self.ui.lE_WidthVid.setText(str(width))
            self.ui.lE_HeightVid.setText(str(height))
            self.ui.lE_FPS_vid.setText(str(fps))

            # Создаем детектор лиц для обработки видео
            self.face_detector = FaceDetector(
                self.update_video_frame,
                self.update_fps_values,
                lambda w, h, f: None,
                self.update_targets_list
            )

            # Останавливаем стандартный захват камеры в детекторе
            if self.face_detector.cap and self.face_detector.cap.isOpened():
                self.face_detector.cap.release()

            # Заменяем захват камеры на захват видео файла
            self.face_detector.cap = self.video_capture

            # Применяем текущие значения фильтров
            self.update_filters()

            # Переменные для измерения производительности
            self.frame_processing_times = deque(maxlen=30)
            self.adaptive_interval = 33  # Начальный интервал

            if self.video_processing_timer:
                self.video_processing_timer.stop()

            self.video_processing_timer = QTimer(self)
            self.video_processing_timer.timeout.connect(self.process_video_frame)
            self.video_processing_timer.start(self.adaptive_interval)

            self.retry_mode = False
            self.ui.pB_play_pause.setText("⏸")
            self.ui.pB_play_pause.setChecked(True)
            self.ui.pB_play_pause.setText("⏸")
            self.is_video_playing = True
            self.ui.pB_play_pause.setToolTip("Пауза")

            # Создаем таймер если его еще нет
            if not hasattr(self, 'video_processing_timer') or self.video_processing_timer is None:
                self.video_processing_timer = QTimer(self)

            self.video_processing_timer.timeout.connect(self.process_video_frame)
            self.video_processing_timer.start(self.adaptive_interval)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при запуске обработки видео: {str(e)}")
            self.show_waiting_message()
            self.ui.pB_play_pause.setChecked(False)
            self.ui.pB_play_pause.setText("▶")
            self.is_video_playing = False

    def process_video_frame(self):
        """Обработка одного кадра видео с адаптивным управлением FPS"""
        if not self.is_video_playing or not self.video_capture or not self.video_capture.isOpened():
            return

        start_time = time.perf_counter()  # Более точное время

        if self.face_detector:
            # Обрабатываем кадр через детектор лиц
            self.face_detector.next_frame()

            # Измеряем время обработки
            processing_time = (time.perf_counter() - start_time) * 1000  # в миллисекундах
            self.frame_processing_times.append(processing_time)

            # Адаптивно регулируем интервал таймера
            self._adjust_timer_interval(processing_time)

            # Обновляем информацию о времени и слайдере
            self.update_video_info()

            # Проверяем, достигнут ли конец видео
            current_pos = self.video_capture.get(cv2.CAP_PROP_POS_FRAMES)
            total_frames = self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)

            if current_pos >= total_frames - 1:
                self.handle_video_end()

    def _adjust_timer_interval(self, processing_time):
        """Адаптивная регулировка интервала таймера"""
        if len(self.frame_processing_times) < 5:
            return

        avg_processing_time = sum(self.frame_processing_times) / len(self.frame_processing_times)

        # Целевое время кадра для достижения оригинального FPS видео
        target_frame_time = 1000 / self.original_video_fps if self.original_video_fps > 0 else 33

        # Вычисляем оптимальный интервал
        if avg_processing_time < target_frame_time:
            # Можем увеличить FPS
            self.adaptive_interval = max(1, int(target_frame_time - avg_processing_time))
        else:
            # Нужно уменьшить FPS чтобы избежать лагов
            self.adaptive_interval = int(avg_processing_time + 1)

        # Ограничиваем максимальный интервал (мин. 5 FPS)
        self.adaptive_interval = min(self.adaptive_interval, 200)

        # Обновляем интервал таймера
        if self.video_processing_timer.isActive():
            self.video_processing_timer.setInterval(self.adaptive_interval)

    def handle_video_end(self):
        """Обработка завершения видео - переход в режим повторного воспроизведения"""
        self.retry_mode = True
        self.ui.pB_play_pause.setChecked(False)
        self.ui.pB_play_pause.setText("🔄")  # Иконка повторного запуска
        self.ui.pB_play_pause.setToolTip("Воспроизвести заново")

        # Останавливаем только таймер, но НЕ детектор
        if self.video_processing_timer and self.video_processing_timer.isActive():
            self.video_processing_timer.stop()

        self.is_video_playing = False

        # НЕ останавливаем детектор!
        # if self.face_detector:
        #     self.face_detector.stop()
        #     self.face_detector = None

    def stop_video_stream_processing(self):
        """Остановка обработки видео в реальном времени"""
        if self.video_processing_timer and self.video_processing_timer.isActive():
            self.video_processing_timer.stop()

        # Сбрасываем состояние кнопки воспроизведения
        self.is_video_playing = False
        self.ui.pB_play_pause.setChecked(False)
        self.ui.pB_play_pause.setText("▶")

    def slider_changed(self, value):
        """Обработка изменения значения слайдера"""
        if not self.video_capture or self.video_duration == 0 or not self.ui.video_slider.isSliderDown():
            return

        # Вычисляем новую позицию в секундах
        new_position = (value / self.ui.video_slider.maximum()) * self.video_duration
        self.video_capture.set(cv2.CAP_PROP_POS_MSEC, new_position * 1000)

        # Сохраняем текущие траектории перед сбросом
        saved_trajectories = {}
        saved_next_face_id = 1
        if self.face_detector:
            saved_trajectories = self.face_detector.trajectories.copy()
            saved_next_face_id = self.face_detector.next_face_id

        # Сбрасываем трекер лиц при перемотке
        if self.face_detector:
            self.face_detector.trajectories = {}
            self.face_detector.next_face_id = 1

        # Очищаем список целей в интерфейсе
        self.clear_targets_list()

        # Восстанавливаем сохраненные траектории
        if self.face_detector:
            self.face_detector.trajectories = saved_trajectories
            self.face_detector.next_face_id = saved_next_face_id

        self.update_video_info()

    def slider_pressed(self):
        """Обработка нажатия на слайдер"""
        # Запоминаем состояние воспроизведения
        self.was_playing_before_seek = self.is_video_playing
        if self.is_video_playing:
            if self.current_mode == 'video_processing' and self.video_processing_timer:
                self.video_processing_timer.stop()
            elif self.current_mode == 'video_playback' and self.video_timer:
                self.video_timer.stop()
            self.is_video_playing = False

    def slider_released(self):
        """Обработка отпускания слайдера"""
        # Восстанавливаем состояние воспроизведения
        if self.was_playing_before_seek and self.ui.pB_play_pause.isChecked():
            self.is_video_playing = True
            if self.current_mode == 'video_processing' and self.video_processing_timer:
                self.video_processing_timer.start()
            elif self.current_mode == 'video_playback' and self.video_timer:
                self.video_timer.start()

    def show_video_controls(self, show=True):
        """Показать/скрыть панель управления видео"""
        self.ui.video_control_container.setVisible(show)

    def toggle_play_pause(self):
        """Переключение воспроизведения/паузы/повтора"""
        if self.current_mode is None:
            return

        # Обработка режима повторного воспроизведения
        if self.retry_mode:
            self.retry_playback()
            return

        if self.ui.pB_play_pause.isChecked():
            # Состояние воспроизведения
            self.ui.pB_play_pause.setText("⏸")
            self.is_video_playing = True

            # Запускаем соответствующий таймер в зависимости от режима
            if self.current_mode == 'video_processing' and self.video_processing_timer:
                self.video_processing_timer.start()
            elif self.current_mode == 'video_playback' and self.video_timer:
                self.video_timer.start()
            elif self.current_mode == 'camera' and hasattr(self, 'timer'):
                self.timer.start()

        else:
            # Состояние паузы
            self.ui.pB_play_pause.setText("▶")
            self.is_video_playing = False

            # Останавливаем соответствующий таймер
            if self.current_mode == 'video_processing' and self.video_processing_timer:
                self.video_processing_timer.stop()
            elif self.current_mode == 'video_playback' and self.video_timer:
                self.video_timer.stop()
            elif self.current_mode == 'camera' and hasattr(self, 'timer'):
                self.timer.stop()

    def retry_playback(self):
        """Повторное воспроизведение текущего видео"""
        self.retry_mode = False
        self.ui.pB_play_pause.setChecked(True)
        self.ui.pB_play_pause.setText("⏸")
        self.ui.pB_play_pause.setToolTip("Пауза")

        # Перематываем видео в начало
        if self.video_capture:
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # Очищаем трекер лиц
        if self.face_detector:
            self.face_detector.trajectories = {}
            self.face_detector.next_face_id = 1

        # Очищаем список целей
        self.clear_targets_list()

        # Запускаем воспроизведение
        if self.current_mode == 'video_processing':
            # Просто перезапускаем таймер, не пересоздавая детектор
            self.is_video_playing = True
            self.video_processing_timer.start()
        elif self.current_mode == 'video_playback':
            self.play_video()

    def seek_video(self, seconds):
        """Перемотка видео на указанное количество секунд"""
        if not self.video_capture:
            return

        current_pos = self.video_capture.get(cv2.CAP_PROP_POS_MSEC) / 1000  # текущая позиция в секундах
        new_pos = max(0, min(self.video_duration, current_pos + seconds))

        # Устанавливаем новую позицию
        self.video_capture.set(cv2.CAP_PROP_POS_MSEC, new_pos * 1000)

        # Сбрасываем трекер лиц при перемотке
        if self.face_detector:
            self.face_detector.trajectories = {}
            self.face_detector.next_face_id = 1

        # Очищаем список целей в интерфейсе
        self.clear_targets_list()

        self.update_video_info()

    def update_video_info(self):
        """Обновление информации о видео (время, слайдер)"""
        if not self.video_capture:
            return

        # Получаем текущую позицию и длительность
        current_pos_ms = self.video_capture.get(cv2.CAP_PROP_POS_MSEC)
        total_frames = self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = self.video_capture.get(cv2.CAP_PROP_FPS)

        if fps > 0 and total_frames > 0:
            self.video_duration = total_frames / fps
            current_time = current_pos_ms / 1000  # в секундах

            # Обновляем слайдер (только если пользователь не взаимодействует с ним)
            if not self.ui.video_slider.isSliderDown():
                self.ui.video_slider.blockSignals(True)
                slider_value = int((
                                               current_time / self.video_duration) * self.ui.video_slider.maximum()) if self.video_duration > 0 else 0
                self.ui.video_slider.setValue(slider_value)
                self.ui.video_slider.blockSignals(False)

            # Обновляем метку времени
            current_str = self.format_time(current_time)
            duration_str = self.format_time(self.video_duration)
            self.ui.lbl_video_time.setText(f"{current_str} / {duration_str}")

    def format_time(self, seconds):
        """Форматирование времени в MM:SS"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def clear_targets_list(self):
        """Очистка списка целей"""
        for target_id in list(self.target_widgets.keys()):
            widget = self.target_widgets.pop(target_id)
            widget.deleteLater()

    def stop_all_processing(self):
        """Остановка всех процессов"""
        self.stop_video_processing()
        self.stop_video_playback()
        self.stop_video_stream_processing()

        if self.face_detector:
            self.face_detector.stop()
            self.face_detector = None

        if hasattr(self, 'timer'):
            self.timer.stop()

    def setup_sliders(self):
        """Настройка слайдеров фильтров"""
        # Установка диапазонов для слайдеров
        self.ui.S_rez.setRange(-100, 100)
        self.ui.S_light.setRange(-100, 100)
        self.ui.S_contrast.setRange(-100, 100)

        # Установка начальных значений
        self.ui.S_rez.setValue(0)
        self.ui.S_light.setValue(0)
        self.ui.S_contrast.setValue(0)

        # Подключение сигналов
        self.ui.S_rez.valueChanged.connect(self.on_sharpness_changed)
        self.ui.S_light.valueChanged.connect(self.on_brightness_changed)
        self.ui.S_contrast.valueChanged.connect(self.on_contrast_changed)

    def on_sharpness_changed(self, value):
        """Обработка изменения резкости"""
        self.sharpness = value
        self.update_filters()

    def on_brightness_changed(self, value):
        """Обработка изменения яркости"""
        self.brightness = value
        self.update_filters()

    def on_contrast_changed(self, value):
        """Обработка изменения контрастности"""
        self.contrast = value
        self.update_filters()

    def update_filters(self):
        """Обновление фильтров в детекторе"""
        if self.face_detector:
            self.face_detector.update_filters(self.sharpness, self.brightness, self.contrast)

    def reset_filters(self):
        """Сброс всех фильтров к нулевым значениям"""
        # Блокируем сигналы чтобы избежать множественных вызовов
        self.ui.S_rez.blockSignals(True)
        self.ui.S_light.blockSignals(True)
        self.ui.S_contrast.blockSignals(True)

        # Сбрасываем значения слайдеров
        self.ui.S_rez.setValue(0)
        self.ui.S_light.setValue(0)
        self.ui.S_contrast.setValue(0)

        # Разблокируем сигналы
        self.ui.S_rez.blockSignals(False)
        self.ui.S_light.blockSignals(False)
        self.ui.S_contrast.blockSignals(False)

        # Обновляем локальные переменные
        self.sharpness = 0
        self.brightness = 0
        self.contrast = 0

        # Обновляем фильтры в детекторе
        self.update_filters()

    def set_filters_enabled(self, enabled):
        """Блокировка/разблокировка слайдеров фильтров"""
        self.ui.S_rez.setEnabled(enabled)
        self.ui.S_light.setEnabled(enabled)
        self.ui.S_contrast.setEnabled(enabled)

    def show_processing_error(self, error_message):
        """Показать ошибку обработки"""
        self.stop_video_processing()
        QMessageBox.critical(self, "Ошибка", f"Ошибка при обработке видео: {error_message}")
        self.show_waiting_message()

    def show_waiting_message(self):
        """Показать сообщение об ожидании"""
        # Убеждаемся, что кнопка камеры в правильном состоянии
        self.ui.pB_translationCam.setText("Подключение\nк камере")
        self.camera_active = False

        # Заблокируем фильтры при возврате в ожидание
        self.set_filters_enabled(False)

        self.clear_video_display()
        self.ui.l_video.setText("Ожидание видеопотока")
        self.ui.l_video.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def clear_video_display(self):
        """Очистить отображение видео"""
        self.ui.l_video.clear()
        self.ui.l_video.setPixmap(QPixmap())

        # Удаляем все виджеты из layout
        for i in reversed(range(self.video_layout.count())):
            widget = self.video_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

    def clear_interface(self):
        """Полная очистка интерфейса: видео и целей"""
        # Очистка видео
        self.clear_video_display()

        self.show_video_controls(False)

        # Сброс текстовой информации
        self.ui.lE_FPS_vid.setText("")
        self.ui.lE_FPS_code_AVG.setText("")
        self.ui.lE_FaceCol.setText("")
        self.ui.lE_WidthVid.setText("")
        self.ui.lE_HeightVid.setText("")

        # Сброс фильтров
        self.reset_filters()

        # Очистка целей
        for target_id in list(self.target_widgets.keys()):
            widget = self.target_widgets.pop(target_id)
            widget.deleteLater()

        # Сброс прогресса
        self.ui.progressBar.setValue(0)
        self.ui.lbl_processing_status.setVisible(False)

    def toggle_camera(self):
        """Переключение состояния камеры (вкл/выкл)"""
        if self.camera_active:
            self.stop_camera()
        else:
            self.start_camera()

    def start_camera(self):
        """Запуск камеры"""
        # Устанавливаем флаг активности камеры
        self.camera_active = True

        # Обновляем текст кнопки
        self.ui.pB_translationCam.setText("Остановить камеру")

        # Разблокируем фильтры
        self.set_filters_enabled(True)

        # Очищаем интерфейс перед запуском
        self.clear_interface()
        self.show_video_controls(False)

        # Останавливаем все другие процессы
        self.stop_video_processing()
        self.stop_video_playback()

        # Очищаем отображение
        self.clear_video_display()

        if self.face_detector is not None:
            self.face_detector.stop()
            self.face_detector = None

        try:
            # Создание детектора лиц с callback-функциями
            self.face_detector = FaceDetector(
                self.update_video_frame,  # Обновление кадра видео
                self.update_fps_values,  # Обновление значений FPS
                self.update_camera_info,  # Обновление информации о камере
                self.update_targets_list  # Обновление списка целей
            )

            # Применение текущих значений фильтров
            self.update_filters()

            # Таймер для обработки кадров
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.process_frame)
            self.timer.start(30)  # ~33 FPS

        except Exception as e:
            print(f"Ошибка при запуске камеры: {e}")
            self.show_camera_error("Камера не обнаружена")
            if self.face_detector:
                self.face_detector.stop()
                self.face_detector = None
            # Сбрасываем флаг активности при ошибке
            self.camera_active = False
            self.ui.pB_translationCam.setText("Запустить камеру")

    def stop_camera(self):
        """Остановка камеры"""
        # Сбрасываем флаг активности камеры
        self.camera_active = False

        # Очищаем интерфейс перед запуском
        self.clear_interface()
        self.show_video_controls(False)

        # Обновляем текст кнопки
        self.ui.pB_translationCam.setText("Запустить камеру")

        # Останавливаем все процессы камеры
        if hasattr(self, 'timer'):
            self.timer.stop()

        if self.face_detector:
            self.face_detector.stop()
            self.face_detector = None

        # Переходим в состояние ожидания
        self.show_waiting_message()

    def show_camera_error(self, message):
        """Показать сообщение об ошибке камеры"""
        self.clear_video_display()
        self.ui.l_video.setText(message)
        self.ui.l_video.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Таймер для возврата к исходному тексту через 5 секунд
        QTimer.singleShot(5000, self.show_waiting_message)

    def check_camera_status(self):
        """Проверка статуса камеры"""
        if self.face_detector is None:
            return

        if not self.face_detector.cap.isOpened():
            self.show_camera_error("Камера отключена")
            if self.face_detector:
                self.face_detector.stop()
                self.face_detector = None
            if hasattr(self, 'timer'):
                self.timer.stop()

    def open_video_file(self):
        """Открытие видео файла из проводника для воспроизведения"""
        # Останавливаем камеру если она активна
        if self.camera_active:
            self.stop_camera()

        # Блокируем фильтры
        self.set_filters_enabled(False)

        # Очищаем интерфейс перед открытием
        self.clear_interface()

        # Останавливаем все другие процессы
        self.stop_video_processing()
        if self.face_detector:
            self.face_detector.stop()
            self.face_detector = None
        if hasattr(self, 'timer'):
            self.timer.stop()
        self.stop_video_playback()

        # Скрываем панель управления (на всякий случай)
        self.show_video_controls(False)

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите видео файл",
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv *.wmv)"
        )

        if file_path:
            self.current_video_path = file_path

            # Получаем информацию о видео
            try:
                cap = cv2.VideoCapture(file_path)
                if cap.isOpened():
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = int(cap.get(cv2.CAP_PROP_FPS))

                    # Обновляем информацию в интерфейсе
                    self.ui.lE_WidthVid.setText(str(width))
                    self.ui.lE_HeightVid.setText(str(height))
                    self.ui.lE_FPS_vid.setText(str(fps))

                    cap.release()
            except Exception as e:
                print(f"Ошибка при получении информации о видео: {e}")

            # Устанавливаем режим воспроизведения видео
            self.current_mode = 'video_playback'
            # Показываем панель управления
            self.show_video_controls(True)
            self.play_video()  # Сразу начинаем воспроизведение

    def play_video(self):
        """Воспроизведение выбранного видео файла"""
        if not self.current_video_path:
            QMessageBox.warning(self, "Предупреждение", "Сначала выберите видео файл")
            return

        # Останавливаем все другие процессы
        self.stop_video_processing()
        if self.face_detector:
            self.face_detector.stop()
            self.face_detector = None
        if hasattr(self, 'timer'):
            self.timer.stop()

        try:
            # Открываем видео файл
            self.video_capture = cv2.VideoCapture(self.current_video_path)
            if not self.video_capture.isOpened():
                raise Exception("Не удалось открыть видео файл")

            # Получаем FPS видео для правильного воспроизведения
            fps = self.video_capture.get(cv2.CAP_PROP_FPS)
            interval = int(1000 / fps) if fps > 0 else 33  # 33 мс по умолчанию (30 FPS)

            # Обновляем информацию о времени сразу после открытия
            self.update_video_info()

            # Устанавливаем кнопку в состояние воспроизведения (пауза)
            self.ui.pB_play_pause.setChecked(True)
            self.ui.pB_play_pause.setText("⏸")
            self.is_video_playing = True

            # Запускаем таймер для воспроизведения
            self.video_timer.start(interval)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при воспроизведении видео: {str(e)}")
            self.show_waiting_message()
            # Сбрасываем состояние кнопки при ошибке
            self.ui.pB_play_pause.setChecked(False)
            self.ui.pB_play_pause.setText("▶")
            self.is_video_playing = False

    # Замените метод play_video_frame на этот:
    def play_video_frame(self):
        """Воспроизведение одного кадра видео"""
        if self.video_capture and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if ret:
                # Конвертируем BGR в RGB для отображения
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Отображаем кадр
                self.display_frame(rgb_frame)
                # Обновляем информацию о времени и слайдере
                self.update_video_info()

                # Проверяем, достигнут ли конец видео
                current_pos = self.video_capture.get(cv2.CAP_PROP_POS_FRAMES)
                total_frames = self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)

                if current_pos >= total_frames - 1:  # Конец видео
                    self.handle_video_end()
            else:
                # Достигнут конец видео
                self.handle_video_end()

    def stop_video_playback(self):
        """Остановка воспроизведения видео"""
        # Разблокируем фильтры при остановке воспроизведения
        # self.set_filters_enabled(False)

        if self.video_timer.isActive():
            self.video_timer.stop()
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
        self.ui.lbl_processing_status.setVisible(False)
        # Сбрасываем состояние кнопки воспроизведения
        self.is_video_playing = False
        self.ui.pB_play_pause.setChecked(False)
        self.ui.pB_play_pause.setText("▶")

    def process_video_file(self):
        """Обработка видео файла (фоновая обработка с детекцией)"""
        # Останавливаем камеру если она активна
        if self.camera_active:
            self.stop_camera()

        # Блокируем фильтры
        self.set_filters_enabled(False)

        # Очищаем интерфейс перед обработкой
        self.clear_interface()
        self.show_video_controls(False)

        # Останавливаем все другие процессы
        self.stop_video_playback()
        if self.face_detector:
            self.face_detector.stop()
            self.face_detector = None
        if hasattr(self, 'timer'):
            self.timer.stop()

        # Выбираем файл для обработки
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите видео файл для обработки",
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv *.wmv)"
        )

        if file_path:
            self.start_video_processing(file_path)

    def start_video_processing(self, video_path):
        """Запуск обработки видео"""
        try:
            # Создаем процессор видео
            self.video_processor = VideoProcessor(video_path)

            # Показываем прогресс-бар и статус
            self.ui.progressBar.setVisible(True)
            self.ui.lbl_processing_status.setVisible(True)
            self.ui.progressBar.setValue(0)
            self.ui.lbl_processing_status.setText("Обработка видео...")

            # Запускаем обработку в отдельном потоке
            self.processing_thread = threading.Thread(target=self.process_video_thread, daemon=True)
            self.processing_thread.start()

            # Запускаем таймер для обновления прогресса
            self.progress_timer.start(100)  # Обновляем каждые 100 мс

        except Exception as e:
            self.stop_video_processing()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обработке видео: {str(e)}")
            self.show_waiting_message()

    def process_video_thread(self):
        """Поток для обработки видео"""
        try:
            if self.video_processor:
                output_path = self.video_processor.process_video()
                # Сигнализируем о завершении обработки
                self.processing_complete_signal.emit(output_path)
        except Exception as e:
            print(f"Ошибка в потоке обработки: {e}")
            self.processing_error_signal.emit(str(e))

    def update_progress_display(self):
        """Обновление отображения прогресса"""
        if self.video_processor and hasattr(self.video_processor, 'processing'):
            progress = self.video_processor.get_progress()
            # progressBar
            self.ui.progressBar.setValue(progress)
            # lbl_processing_statu
            current = self.video_processor.processed_frames
            total = self.video_processor.total_frames
            status_text = f"Обработка: {current}/{total} кадров"
            self.ui.lbl_processing_status.setText(status_text)

            # Если прогресс 100%, останавливаем таймер и показываем завершение
            if progress >= 100:
                self.progress_timer.stop()
                self.ui.lbl_processing_status.setText("Обработка завершена!")
                # Автоматически скрываем через 3 секунды
                QTimer.singleShot(3000, self.hide_processing_elements)
        else:
            self.progress_timer.stop()

    def hide_processing_elements(self):
        """Скрыть элементы прогресса после завершения"""
        self.ui.progressBar.setVisible(False)
        self.ui.lbl_processing_status.setVisible(False)

    def processing_complete(self, output_path):
        """Обработка завершения обработки видео"""
        # Разблокируем фильтры после завершения обработки
        self.set_filters_enabled(False)

        # Убеждаемся, что прогресс = 100%
        self.ui.progressBar.setValue(100)
        self.ui.lbl_processing_status.setText("Обработка завершена!")

        # Останавливаем таймер прогресса
        self.progress_timer.stop()

        # Скрываем элементы прогресса через 3 секунды
        QTimer.singleShot(3000, self.hide_processing_elements)
        QTimer.singleShot(3000, self.show_waiting_message)

    def stop_video_processing(self):
        """Остановка обработки видео"""
        if self.video_processor:
            self.video_processor.stop_processing()
            self.video_processor = None

        # Ожидаем завершения потока (с таймаутом)
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=2.0)  # Ждем до 2 секунд

        self.progress_timer.stop()
        self.hide_processing_elements()

    def update_targets_list(self, targets):
        """Обновление списка обнаруженных целей в интерфейсе"""
        for target_id in list(self.target_widgets.keys()):
            if target_id not in targets:
                widget = self.target_widgets.pop(target_id)
                widget.deleteLater()

        for target_id, target_data in targets.items():
            x, y, w, h = target_data['bbox']
            color = target_data['color']
            name = target_data.get('name', '')  # Получаем имя если есть

            if target_id in self.target_widgets:
                widget = self.target_widgets[target_id]
                widget.coords_label.setText(f"({x}, {y})")
                widget.size_label.setText(f"{w}×{h} px")
                if name:
                    widget.id_label.setText(name)
            else:
                widget = TargetWidget(target_id, x, y, w, h, color, name)
                self.target_widgets[target_id] = widget
                self.ui.targets_layout.addWidget(widget)

    def display_frame(self, rgb_frame):
        """Отображение кадра в QLabel с сохранением соотношения сторон"""
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w

        # Создание QImage из данных кадра
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Масштабирование изображения под размер QLabel с сохранением соотношения сторон
        scaled_pixmap = QPixmap.fromImage(qt_image).scaled(
            self.ui.l_video.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        # Установка изображения в QLabel
        self.ui.l_video.setPixmap(scaled_pixmap)

    def update_video_frame(self, frame):
        """Оптимизированное обновление QLabel с масштабированием"""
        # Конвертируем BGR (OpenCV) в RGB (Qt)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Создаем QImage из данных кадра
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Масштабируем изображение под размер QLabel с сохранением соотношения сторон
        scaled_pixmap = QPixmap.fromImage(qt_image).scaled(
            self.ui.l_video.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        # Установка изображения в QLabel
        self.ui.l_video.setPixmap(scaled_pixmap)

    def update_fps_values(self, fps_avg, faces_count):
        """Обновление значений FPS в интерфейсе"""
        self.fps_AVG = fps_avg
        self.ui.lE_FPS_code_AVG.setText(fps_avg)
        self.ui.lE_FaceCol.setText(faces_count)

    def update_camera_info(self, width, height, fps):
        """Обновление информации о камере в интерфейсе"""
        self.camera_width = str(width)
        self.camera_height = str(height)
        self.camera_fps = str(fps)
        self.ui.lE_WidthVid.setText(self.camera_width)
        self.ui.lE_HeightVid.setText(self.camera_height)
        self.ui.lE_FPS_vid.setText(self.camera_fps)

    def process_frame(self):
        """Обработка одного кадра"""
        if self.face_detector:
            self.face_detector.next_frame()

    def closeEvent(self, event):
        """Обработка закрытия окна приложения"""
        # Останавливаем камеру при закрытии
        if self.camera_active:
            self.stop_camera()

        self.stop_all_processing()

        # Останавливаем все таймеры с проверкой на существование
        if hasattr(self, 'timer') and self.timer:
            self.timer.stop()

        if hasattr(self, 'video_processing_timer') and self.video_processing_timer:
            self.video_processing_timer.stop()

        if hasattr(self, 'video_timer') and self.video_timer:
            self.video_timer.stop()

        if hasattr(self, 'progress_timer') and self.progress_timer:
            self.progress_timer.stop()

        if hasattr(self, 'camera_check_timer') and self.camera_check_timer:
            self.camera_check_timer.stop()

        # Останавливаем детектор
        if self.face_detector:
            self.face_detector.stop()
            self.face_detector = None

        # Останавливаем обработку видео
        self.stop_video_processing()

        # Освобождаем видеозахват
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None

        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())