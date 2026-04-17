import cv2
import numpy as np
import os
import glob
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QMessageBox,
                               QFileDialog, QProgressDialog, QWidget)
from PySide6.QtCore import Qt, QThread, Signal
from UI_CreateNPY_FREL import Ui_Form
from config import get_cascade_path


class DatabaseCreationThread(QThread):
    """Поток для создания базы данных"""
    progress_signal = Signal(str, int)
    finished_signal = Signal(dict, str)
    error_signal = Signal(str)

    def __init__(self, mode, folder_path=None, person_name=None):
        super().__init__()
        self.mode = mode
        self.folder_path = folder_path
        self.person_name = person_name
        self.running = True

    def run(self):
        try:
            database = {}

            if self.mode == "folder" and self.folder_path:
                self.progress_signal.emit("Обработка изображений из папки...", 0)
                database = self.create_from_folder(self.folder_path, self.person_name)

            elif self.mode == "camera":
                self.progress_signal.emit("Захват изображений с камеры...", 0)
                database = self.create_from_camera()

            elif self.mode == "combined" and self.folder_path:
                self.progress_signal.emit("Комбинированная обработка...", 0)
                db_folder = self.create_from_folder(self.folder_path, self.person_name)
                if self.running:
                    db_camera = self.create_from_camera()
                    database = self.merge_databases(db_folder, db_camera)

            if database and self.running:
                self.finished_signal.emit(database, self.person_name or "Vlad")

        except Exception as e:
            self.error_signal.emit(str(e))

    def create_from_camera(self):
        """Создание базы данных из камеры"""
        os.makedirs("face_database", exist_ok=True)
        database = {}

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Не удалось открыть камеру!")

        count = 0
        max_samples = 30

        # ИСПРАВЛЕНИЕ: Используем нашу функцию для получения пути
        cascade_path = get_cascade_path('haarcascade_frontalface_default.xml')
        face_cascade = cv2.CascadeClassifier(cascade_path)

        if face_cascade.empty():
            raise Exception(f"Не удалось загрузить cascade файл: {cascade_path}")

        while count < max_samples and self.running:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                padding = 15
                x1 = max(0, x - padding)
                y1 = max(0, y - padding)
                x2 = min(frame.shape[1], x + w + padding)
                y2 = min(frame.shape[0], y + h + padding)

                face_roi = frame[y1:y2, x1:x2]

                if face_roi.size == 0:
                    continue

                if count < max_samples:
                    filename = f"face_database/{self.person_name or 'Vlad'}_{count:02d}.jpg"
                    cv2.imwrite(filename, face_roi)

                    try:
                        face_image = cv2.resize(face_roi, (100, 100))
                        face_image = cv2.medianBlur(face_image, 3)
                        hsv = cv2.cvtColor(face_image, cv2.COLOR_BGR2HSV)
                        hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
                        cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
                        hist = hist.flatten()

                        person_name = self.person_name or "Vlad"
                        if person_name not in database:
                            database[person_name] = []
                        database[person_name].append(hist)

                        count += 1
                        progress = int((count / max_samples) * 100)
                        self.progress_signal.emit(f"Собрано образцов: {count}/{max_samples}", progress)
                        QApplication.processEvents()

                    except Exception as e:
                        continue

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return database

    def create_from_folder(self, folder_path, person_name):
        """Создание базы данных из папки"""
        database = {}

        if not os.path.exists(folder_path):
            raise Exception(f"Папка {folder_path} не существует!")

        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
        image_paths = []
        for extension in image_extensions:
            image_paths.extend(glob.glob(os.path.join(folder_path, extension)))

        if not image_paths:
            raise Exception(f"В папке {folder_path} не найдено изображений!")

        # ИСПРАВЛЕНИЕ: Используем нашу функцию для получения пути
        cascade_path = get_cascade_path('haarcascade_frontalface_default.xml')
        face_cascade = cv2.CascadeClassifier(cascade_path)

        if face_cascade.empty():
            raise Exception(f"Не удалось загрузить cascade файл: {cascade_path}")

        count = 0
        database[person_name] = []

        for i, image_path in enumerate(image_paths):
            if not self.running:
                break

            image = cv2.imread(image_path)
            if image is None:
                continue

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) == 0:
                continue

            x, y, w, h = faces[0]
            padding = 15
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(image.shape[1], x + w + padding)
            y2 = min(image.shape[0], y + h + padding)

            face_roi = image[y1:y2, x1:x2]

            if face_roi.size == 0:
                continue

            try:
                face_image = cv2.resize(face_roi, (100, 100))
                face_image = cv2.medianBlur(face_image, 3)
                hsv = cv2.cvtColor(face_image, cv2.COLOR_BGR2HSV)
                hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
                cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
                hist = hist.flatten()

                database[person_name].append(hist)
                count += 1
                progress = int((count / len(image_paths)) * 100)
                self.progress_signal.emit(f"Обработано: {count}/{len(image_paths)}", progress)
                QApplication.processEvents()

            except Exception as e:
                continue

        return database

    def merge_databases(self, db1, db2):
        """Объединение баз данных"""
        merged_db = db1.copy()
        for person, signatures in db2.items():
            if person in merged_db:
                merged_db[person].extend(signatures)
            else:
                merged_db[person] = signatures
        return merged_db

    def stop(self):
        """Остановка потока"""
        self.running = False


class CreateNPYWindow(QMainWindow):  # ИЗМЕНИТЕ НА QMainWindow
    """Окно для создания базы данных лиц"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Настройка основного окна
        self.setWindowTitle("Создание базы данных лиц")
        self.setMaximumSize(250, 350)
        self.setMinimumSize(250, 350)

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Загружаем UI в центральный виджет
        self.ui = Ui_Form()
        self.ui.setupUi(central_widget)

        # Настройка начального состояния
        self.creation_thread = None
        self.progress_dialog = None
        self.setup_connections()

        # Устанавливаем модальность окна
        self.setWindowModality(Qt.ApplicationModal)

    def setup_connections(self):
        """Настройка соединений сигналов и слотов"""
        self.ui.pB_genFaceDB.clicked.connect(self.start_database_creation)
        self.ui.pB_mergeDB.clicked.connect(self.merge_databases)

    def start_database_creation(self):
        """Запуск создания базы данных"""
        # Определяем режим работы
        if self.ui.rB_onlyFolder.isChecked():
            mode = "folder"
        elif self.ui.rB_onlyCam.isChecked():
            mode = "camera"
        elif self.ui.rB_mergeCombo.isChecked():
            mode = "combined"
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите режим создания базы данных!")
            return

        person_name = self.ui.lE_nameDB.text().strip() or "Unknown"

        # Для режимов с папкой запрашиваем путь
        folder_path = ""
        if mode in ["folder", "combined"]:
            folder_path = QFileDialog.getExistingDirectory(
                self,
                "Выберите папку с изображениями",
                ""
            )
            if not folder_path:
                return

        # Создаем диалог прогресса
        self.progress_dialog = QProgressDialog("Создание базы данных...", "Отмена", 0, 100, self)
        self.progress_dialog.setWindowTitle("Создание базы данных")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.canceled.connect(self.cancel_creation)

        # Запускаем поток создания базы данных
        self.creation_thread = DatabaseCreationThread(mode, folder_path, person_name)
        self.creation_thread.progress_signal.connect(self.update_progress)
        self.creation_thread.finished_signal.connect(self.on_creation_finished)
        self.creation_thread.error_signal.connect(self.on_creation_error)
        self.creation_thread.start()

        # Показываем диалог прогресса
        self.progress_dialog.show()

        # Блокируем UI на время обработки
        self.set_ui_enabled(False)

    def update_progress(self, message, value):
        """Обновление прогресса"""
        if self.progress_dialog:
            self.progress_dialog.setLabelText(message)
            self.progress_dialog.setValue(value)

    def on_creation_finished(self, database, person_name):
        """Обработка завершения создания базы данных"""
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None

        self.set_ui_enabled(True)

        # Сохраняем базу данных
        filename = f"{person_name}_face_database.npy"
        np.save(filename, database)

        # Показываем статистику
        total_samples = sum(len(sigs) for sigs in database.values())
        QMessageBox.information(
            self,
            "Успех",
            f"База данных создана успешно!\n"
            f"Файл: {filename}\n"
            f"Всего образцов: {total_samples}"
        )

    def on_creation_error(self, error_message):
        """Обработка ошибки создания базы данных"""
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None

        self.set_ui_enabled(True)
        QMessageBox.critical(self, "Ошибка", f"Ошибка при создании базы данных: {error_message}")

    def cancel_creation(self):
        """Отмена создания базы данных"""
        if self.creation_thread and self.creation_thread.isRunning():
            self.creation_thread.stop()
            self.creation_thread.wait()

        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None

        self.set_ui_enabled(True)

    def set_ui_enabled(self, enabled):
        """Включение/отключение элементов UI"""
        self.ui.pB_genFaceDB.setEnabled(enabled)
        self.ui.pB_mergeDB.setEnabled(enabled)
        self.ui.rB_onlyFolder.setEnabled(enabled)
        self.ui.rB_onlyCam.setEnabled(enabled)
        self.ui.rB_mergeCombo.setEnabled(enabled)
        self.ui.lE_nameDB.setEnabled(enabled)

    def merge_databases(self):
        """Объединение существующих баз данных"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Выберите файлы баз данных для объединения",
            "",
            "NumPy Files (*.npy)"
        )

        if len(files) < 2:
            QMessageBox.warning(self, "Ошибка", "Выберите хотя бы 2 файла для объединения!")
            return

        try:
            merged_db = {}
            for file in files:
                db = np.load(file, allow_pickle=True).item()
                for person, signatures in db.items():
                    if person in merged_db:
                        merged_db[person].extend(signatures)
                    else:
                        merged_db[person] = signatures

            # Сохраняем объединенную базу
            output_name = self.ui.lE_nameDB.text().strip() or "merged_face_database"
            np.save(f"{output_name}.npy", merged_db)

            total_samples = sum(len(sigs) for sigs in merged_db.values())
            QMessageBox.information(
                self,
                "Успех",
                f"Базы данных объединены успешно!\n"
                f"Файл: {output_name}.npy\n"
                f"Всего образцов: {total_samples}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при объединении баз данных: {str(e)}")

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        if self.creation_thread and self.creation_thread.isRunning():
            self.creation_thread.stop()
            self.creation_thread.wait()
        event.accept()


if __name__ == "__main__":
    """Запуск окна как самостоятельного приложения"""
    app = QApplication(sys.argv)
    window = CreateNPYWindow()
    window.show()
    sys.exit(app.exec())