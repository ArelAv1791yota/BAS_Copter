import cv2
import numpy as np
import os
from collections import deque


class FaceRecognitionIntegrator:
    def __init__(self, database_path="face_database.npy"):
        self.known_faces = {}
        self.face_cache = {}
        self.recognition_history = {}  # История распознаваний для каждого face_id
        self.load_database(database_path)

    def load_database(self, path):
        """Загрузка базы данных лиц"""
        self.known_faces = {}
        self.face_cache = {}

        if not os.path.exists(path):
            print(f"❌ База данных не найдена по пути: {os.path.abspath(path)}")
            print("💡 Запустите create_face_database_improved.py для создания базы")
            return {}

        try:
            known_faces = np.load(path, allow_pickle=True).item()
            print(f"✅ База данных загружена успешно!")
            print(f"📊 Загружено категорий лиц: {len(known_faces)}")

            total_signatures = 0
            for label, signatures in known_faces.items():
                print(f"   {label}: {len(signatures)} сигнатур")
                # Убедимся, что все сигнатуры имеют одинаковый размер
                processed_signatures = []
                for sig in signatures:
                    if sig is not None and sig.size > 0:
                        # Проверяем размер и при необходимости преобразуем
                        if len(sig.shape) == 2:  # Если это 2D гистограмма
                            sig = sig.flatten()
                        processed_signatures.append(sig)
                self.face_cache[label] = processed_signatures
                total_signatures += len(processed_signatures)

            print(f"📈 Всего сигнатур: {total_signatures}")
            self.known_faces = known_faces
            return known_faces

        except Exception as e:
            print(f"❌ Ошибка загрузки базы данных: {e}")
            return {}

    def get_face_signature(self, face_image):
        """Создание сигнатуры лица с улучшенной обработкой"""
        if face_image is None or face_image.size == 0:
            return None

        try:
            # Нормализуем размер
            face_image = cv2.resize(face_image, (100, 100))

            # Улучшаем качество изображения
            face_image = cv2.medianBlur(face_image, 3)

            # Конвертируем в HSV для лучшей инвариантности к освещению
            hsv = cv2.cvtColor(face_image, cv2.COLOR_BGR2HSV)

            # Создаем гистограмму с фиксированными параметрами
            hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
            cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)

            # Преобразуем в 1D массив фиксированного размера
            hist = hist.flatten()

            # Добавляем небольшую проверку на размер
            expected_size = 50 * 60  # 3000 элементов
            if hist.size != expected_size:
                print(f"⚠️  Неожиданный размер гистограммы: {hist.size}, ожидалось: {expected_size}")
                # Создаем гистограмму правильного размера
                hist = np.zeros(expected_size, dtype=np.float32)

            return hist

        except Exception as e:
            print(f"❌ Ошибка создания сигнатуры: {e}")
            return None

    def recognize_face(self, face_roi, face_id):
        """Улучшенное распознавание лица с историей"""
        if not self.known_faces or face_roi is None:
            return "unknown", 0.0, face_id

        current_signature = self.get_face_signature(face_roi)
        if current_signature is None:
            return "unknown", 0.0, face_id

        best_match = "unknown"
        best_score = 0.0

        # Сравниваем со всеми сигнатурами в базе
        for label, signatures in self.face_cache.items():
            for signature in signatures:
                try:
                    # Проверяем размеры сигнатур
                    if signature.size != current_signature.size:
                        print(f"⚠️  Размеры не совпадают: база={signature.size}, текущая={current_signature.size}")
                        # Приводим к одинаковому размеру
                        min_size = min(signature.size, current_signature.size)
                        signature = signature[:min_size]
                        current_sig = current_signature[:min_size]
                    else:
                        current_sig = current_signature

                    # Используем корреляцию для сравнения гистограмм
                    score = cv2.compareHist(signature.astype(np.float32), current_sig.astype(np.float32), cv2.HISTCMP_CORREL)

                    # Нормализуем score от 0 до 1
                    score = (score + 1) / 2

                    if score > best_score:
                        best_score = score
                        best_match = label

                except Exception as e:
                    print(f"❌ Ошибка сравнения гистограмм: {e}")
                    continue

        # Учет истории распознаваний для улучшения стабильности
        if face_id not in self.recognition_history:
            self.recognition_history[face_id] = deque(maxlen=10)

        self.recognition_history[face_id].append((best_match, best_score))

        # Используем majority voting из истории
        if len(self.recognition_history[face_id]) >= 3:
            matches = [match for match, score in self.recognition_history[face_id]]
            from collections import Counter
            most_common = Counter(matches).most_common(1)

            if most_common and most_common[0][0] != "unknown":
                best_match = most_common[0][0]
                # Берем средний score для наиболее частого match
                scores = [score for match, score in self.recognition_history[face_id]
                          if match == best_match]
                best_score = sum(scores) / len(scores) if scores else best_score

        # Порог распознавания (можно настроить)
        recognition_threshold = 0.8

        if best_score > recognition_threshold and best_match != "unknown":
            return best_match, best_score, face_id
        else:
            return "unknown", best_score, face_id

    def debug_recognition(self, face_roi, face_id):
        """Отладочная информация о распознавании"""
        name, score, fid = self.recognize_face(face_roi, face_id)
        print(f"🔍 Распознавание: ID={face_id}, Name={name}, Score={score:.3f}")
        return name, score, fid