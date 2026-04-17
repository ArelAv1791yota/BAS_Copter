# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GUIPfJmnL.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
                               QPushButton, QScrollArea, QSizePolicy, QSlider,
                               QWidget, QVBoxLayout, QHBoxLayout, QProgressBar)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")

        # Настройка основного окна
        Form.resize(1600, 740)  # Оставляем как начальный размер
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(1600, 740))  # Минимальный размер
        Form.setMaximumSize(QSize(1600, 740))   # Убираем фиксированный максимальный размер
        Form.setAutoFillBackground(False)
        Form.setStyleSheet(u"")

        # ==================== ЛЕВАЯ ПАНЕЛЬ (настройки и информация) ====================

        # ============================= Тексты ===============================

        # Заголовок "Фильтры"
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(90, 10, 120, 40))
        font = QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Надпись "Яркость"
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 70, 111, 30))
        font1 = QFont()
        font1.setPointSize(12)
        self.label_3.setFont(font1)
        self.label_3.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Надпись "Контрастность"
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 150, 111, 30))
        self.label_4.setFont(font1)
        self.label_4.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Надпись "Резкость"
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 110, 111, 30))
        self.label_5.setFont(font1)
        self.label_5.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # ============================= Слайдеры ===============================

        # Слайдер резкости
        self.S_rez = QSlider(Form)
        self.S_rez.setObjectName(u"S_rez")
        self.S_rez.setGeometry(QRect(140, 120, 151, 16))
        self.S_rez.setMinimum(-100)
        self.S_rez.setMaximum(100)
        self.S_rez.setOrientation(Qt.Orientation.Horizontal)

        # Слайдер яркости
        self.S_light = QSlider(Form)
        self.S_light.setObjectName(u"S_light")
        self.S_light.setGeometry(QRect(140, 80, 151, 16))
        self.S_light.setMinimum(-100)
        self.S_light.setMaximum(100)
        self.S_light.setOrientation(Qt.Orientation.Horizontal)

        # Слайдер контрастности
        self.S_contrast = QSlider(Form)
        self.S_contrast.setObjectName(u"S_contrast")
        self.S_contrast.setGeometry(QRect(140, 160, 151, 16))
        self.S_contrast.setMinimum(-100)
        self.S_contrast.setMaximum(100)
        self.S_contrast.setOrientation(Qt.Orientation.Horizontal)

        # ============================= Кнопки ===============================

        # Кнопка "DataBase"
        self.pB_DataBase = QPushButton(Form)
        self.pB_DataBase.setObjectName(u"pB_DataBase")
        self.pB_DataBase.setGeometry(QRect(10, 18, 60, 31))

        # Кнопка "Сброс"
        self.pB_clFil = QPushButton(Form)
        self.pB_clFil.setObjectName(u"pB_clFil")
        self.pB_clFil.setGeometry(QRect(230, 18, 61, 31))

        # Кнопка постобработки видео
        self.pB_saveVid = QPushButton(Form)
        self.pB_saveVid.setObjectName(u"pB_saveVid")
        self.pB_saveVid.setGeometry(QRect(155, 690, 135, 40))

        # Кнопка потоковой обработки загруженного видео
        self.pB_translationVid = QPushButton(Form)
        self.pB_translationVid.setObjectName(u"pB_translationVid")
        self.pB_translationVid.setGeometry(QRect(10, 690, 135, 40))

        # Кнопка подключения к камере
        self.pB_translationCam = QPushButton(Form)
        self.pB_translationCam.setObjectName(u"pB_translationCam")
        self.pB_translationCam.setGeometry(QRect(10, 640, 135, 40))

        # Кнопка открытия видео
        self.pB_openVid = QPushButton(Form)
        self.pB_openVid.setObjectName(u"pB_openVid")
        self.pB_openVid.setGeometry(QRect(155, 640, 135, 40))

        # ============================== Линии ================================

        # Разделительные линии
        self.line_main = QFrame(Form)
        self.line_main.setObjectName(u"line_main")
        self.line_main.setGeometry(QRect(300, 0, 1, 740))
        self.line_main.setStyleSheet(u"border-color: rgb(181, 181, 181);")
        self.line_main.setFrameShape(QFrame.Shape.VLine)
        self.line_main.setFrameShadow(QFrame.Shadow.Sunken)

        self.line_filH_1 = QFrame(Form)
        self.line_filH_1.setObjectName(u"line_filH_1")
        self.line_filH_1.setGeometry(QRect(0, 55, 301, 2))
        self.line_filH_1.setStyleSheet(u"border: 1px dashed;\n"
                                       "border-color: rgb(181, 181, 181);")
        self.line_filH_1.setFrameShape(QFrame.Shape.VLine)
        self.line_filH_1.setFrameShadow(QFrame.Shadow.Sunken)

        self.line_filV = QFrame(Form)
        self.line_filV.setObjectName(u"line_filV")
        self.line_filV.setGeometry(QRect(130, 57, 1, 136))
        self.line_filV.setStyleSheet(u"border: 1px dashed;\n"
                                     "border-color: rgb(181, 181, 181);")
        self.line_filV.setFrameShape(QFrame.Shape.VLine)
        self.line_filV.setFrameShadow(QFrame.Shadow.Sunken)

        self.line_filH_2 = QFrame(Form)
        self.line_filH_2.setObjectName(u"line_filH_2")
        self.line_filH_2.setGeometry(QRect(0, 190, 300, 3))
        self.line_filH_2.setStyleSheet(u"border-color: rgb(181, 181, 181);")
        self.line_filH_2.setLineWidth(1)
        self.line_filH_2.setFrameShape(QFrame.Shape.HLine)
        self.line_filH_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.line_filH_3 = QFrame(Form)
        self.line_filH_3.setObjectName(u"line_filH_3")
        self.line_filH_3.setGeometry(QRect(0, 628, 300, 3))
        self.line_filH_3.setStyleSheet(u"border-color: rgb(181, 181, 181);")
        self.line_filH_3.setLineWidth(1)
        self.line_filH_3.setFrameShape(QFrame.Shape.HLine)
        self.line_filH_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.line_filH_4 = QFrame(Form)
        self.line_filH_4.setObjectName(u"line_filH_4")
        self.line_filH_4.setGeometry(QRect(0, 367, 300, 3))
        self.line_filH_4.setStyleSheet(u"border-color: rgb(181, 181, 181);")
        self.line_filH_4.setLineWidth(1)
        self.line_filH_4.setFrameShape(QFrame.Shape.HLine)
        self.line_filH_4.setFrameShadow(QFrame.Shadow.Sunken)

        # ==================== СЕКЦИЯ ПАРАМЕТРЫ ВИДЕОПОТОКА ====================

        # Заголовок "Параметры обработки видеопотока"
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(0, 195, 300, 40))
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Поле ввода ширины видео
        self.lE_WidthVid = QLineEdit(Form)
        self.lE_WidthVid.setObjectName(u"lE_WidthVid")
        self.lE_WidthVid.setEnabled(False)
        self.lE_WidthVid.setGeometry(QRect(120, 240, 75, 30))
        font3 = QFont()
        font3.setPointSize(11)
        self.lE_WidthVid.setFont(font3)
        self.lE_WidthVid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Поле ввода высоты видео
        self.lE_HeightVid = QLineEdit(Form)
        self.lE_HeightVid.setObjectName(u"lE_HeightVid")
        self.lE_HeightVid.setEnabled(False)
        self.lE_HeightVid.setGeometry(QRect(210, 240, 75, 30))
        self.lE_HeightVid.setFont(font3)
        self.lE_HeightVid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Надпись "Разрешение видео"
        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(20, 235, 90, 40))
        self.label_7.setFont(font3)
        self.label_7.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Разделитель ":"
        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(195, 245, 16, 16))
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Надписи для метрик FPS
        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(13, 285, 90, 40))
        font4 = QFont()
        font4.setPointSize(10)
        self.label_9.setFont(font4)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_10 = QLabel(Form)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(100, 285, 90, 40))
        self.label_10.setFont(font4)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_11 = QLabel(Form)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(190, 285, 90, 40))
        self.label_11.setFont(font4)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Поля ввода для FPS
        self.lE_FPS_vid = QLineEdit(Form)
        self.lE_FPS_vid.setObjectName(u"lE_FPS_vid")
        self.lE_FPS_vid.setEnabled(False)
        self.lE_FPS_vid.setGeometry(QRect(28, 325, 60, 30))
        self.lE_FPS_vid.setFont(font3)
        self.lE_FPS_vid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lE_FPS_code_AVG = QLineEdit(Form)
        self.lE_FPS_code_AVG.setObjectName(u"lE_FPS_code_AVG")
        self.lE_FPS_code_AVG.setEnabled(False)
        self.lE_FPS_code_AVG.setGeometry(115, 325, 60, 30)
        self.lE_FPS_code_AVG.setFont(font3)
        self.lE_FPS_code_AVG.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lE_FaceCol = QLineEdit(Form)
        self.lE_FaceCol.setObjectName(u"lE_FaceCol")
        self.lE_FaceCol.setEnabled(False)
        self.lE_FaceCol.setGeometry(205, 325, 60, 30)
        self.lE_FaceCol.setFont(font3)
        self.lE_FaceCol.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ==================== СПИСОК ОБНАРУЖЕННЫХ ЦЕЛЕЙ ====================

        # ScrollArea для списка целей
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(10, 380, 280, 240))
        self.scrollArea.setWidgetResizable(True)

        # Содержимое ScrollArea
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 50, 50))

        # Вертикальный layout для содержимого ScrollArea
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 0, 5, 5)

        # Заголовок для списка целей
        self.label_targets = QLabel(self.scrollAreaWidgetContents)
        self.label_targets.setObjectName(u"label_targets")
        self.label_targets.setFont(font1)
        self.label_targets.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label_targets)

        # Контейнер для виджетов целей
        self.targets_container = QWidget(self.scrollAreaWidgetContents)
        self.targets_container.setObjectName(u"targets_container")
        self.targets_layout = QVBoxLayout(self.targets_container)
        self.targets_layout.setObjectName(u"targets_layout")
        self.targets_layout.setContentsMargins(0, 0, 0, 0)
        self.targets_layout.setSpacing(5)
        self.verticalLayout.addWidget(self.targets_container)

        # Растягивающийся элемент для правильного размещения
        self.verticalLayout.addStretch(1)

        # Установка содержимого ScrollArea
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # ==================== ПРАВАЯ ПАНЕЛЬ (ВИДЕО) ====================

        # QLabel для отображения видео
        self.l_video = QLabel(Form)
        self.l_video.setObjectName(u"l_video")
        self.l_video.setEnabled(True)
        self.l_video.setGeometry(QRect(310, 10, 1280, 720))
        self.l_video.setMinimumSize(QSize(1280, 720))
        self.l_video.setMaximumSize(QSize(1280, 720))
        font2 = QFont()
        font2.setPointSize(28)
        self.l_video.setFont(font2)
        self.l_video.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ========================= PROGRESS_BAR ===========================

        # Прогресс-бар для обработки видео
        self.progressBar = QProgressBar(Form)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(310, 350, 1280, 40))  # Центрируем по вертикали
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)
        # Увеличиваем шрифт прогресс-бара
        font_progress = QFont()
        font_progress.setPointSize(14)
        font_progress.setBold(True)
        self.progressBar.setFont(font_progress)
        # Стилизация прогресс-бара
        self.progressBar.setStyleSheet("""
                    QProgressBar {
                        border: 2px solid grey;
                        border-radius: 5px;
                        text-align: center;
                        background-color: #757575;
                    }
                    QProgressBar::chunk {
                        background-color: #05B8CC;
                        width: 10px;
                    }
                """)

        # Label для статуса обработки
        self.lbl_processing_status = QLabel(Form)
        self.lbl_processing_status.setObjectName(u"lbl_processing_status")
        self.lbl_processing_status.setGeometry(QRect(310, 400, 1280, 30))  # Под прогресс-баром
        # Увеличиваем шрифт статуса
        font_status = QFont()
        font_status.setPointSize(12)
        font_status.setBold(True)
        self.lbl_processing_status.setFont(font_status)
        self.lbl_processing_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_processing_status.setVisible(False)
        # Стилизация текста статуса
        self.lbl_processing_status.setStyleSheet("color: #757575;")

        # Перевод интерфейса
        self.retranslateUi(Form)

        # Соединение слотов и сигналов
        QMetaObject.connectSlotsByName(Form)

        # ==================== ПАНЕЛЬ УПРАВЛЕНИЯ ВИДЕО ====================

        # Контейнер для панели управления видео
        self.video_control_container = QWidget(Form)
        self.video_control_container.setObjectName(u"video_control_container")
        self.video_control_container.setGeometry(QRect(310, 650, 1280, 80))
        self.video_control_container.setVisible(False)  # Скрыта по умолчанию
        # Затемненный фон
        self.video_control_container.setStyleSheet("background-color: rgba(0, 0, 0, 150); border-radius: 5px;")

        # Вертикальный layout для панели управления
        self.video_control_layout = QVBoxLayout(self.video_control_container)
        self.video_control_layout.setContentsMargins(10, 5, 10, 5)
        self.video_control_layout.setSpacing(5)

        # Слайдер перемотки
        self.video_slider = QSlider(self.video_control_container)
        self.video_slider.setObjectName(u"video_slider")
        self.video_slider.setOrientation(Qt.Orientation.Horizontal)
        self.video_slider.setMinimum(0)
        self.video_slider.setMaximum(1000)
        self.video_slider.setValue(0)
        self.video_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
        """)
        self.video_control_layout.addWidget(self.video_slider)

        # Горизонтальный layout для кнопок и времени
        self.controls_bottom_layout = QHBoxLayout()
        self.controls_bottom_layout.setSpacing(10)

        # Растягивающийся элемент для центрирования кнопок
        self.controls_bottom_layout.addStretch(1)

        # Кнопка перемотки назад на 10 секунд
        self.pB_rewind_10s = QPushButton(self.video_control_container)
        self.pB_rewind_10s.setObjectName(u"pB_rewind_10s")
        self.pB_rewind_10s.setFixedSize(40, 30)
        self.pB_rewind_10s.setStyleSheet("""
            QPushButton {
                background-color: #505050;
                color: white;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #606060;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
        """)
        self.controls_bottom_layout.addWidget(self.pB_rewind_10s)

        # Кнопка перемотки назад на 5 секунд
        self.pB_rewind_5s = QPushButton(self.video_control_container)
        self.pB_rewind_5s.setObjectName(u"pB_rewind_5s")
        self.pB_rewind_5s.setFixedSize(40, 30)
        self.pB_rewind_5s.setStyleSheet("""
            QPushButton {
                background-color: #505050;
                color: white;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #606060;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
        """)
        self.controls_bottom_layout.addWidget(self.pB_rewind_5s)

        # Кнопка воспроизведения/паузы
        self.pB_play_pause = QPushButton(self.video_control_container)
        self.pB_play_pause.setObjectName(u"pB_play_pause")
        self.pB_play_pause.setFixedSize(60, 30)
        self.pB_play_pause.setCheckable(True)
        self.pB_play_pause.setChecked(True)  # Изначально воспроизведение
        self.pB_play_pause.setStyleSheet("""
            QPushButton {
                background-color: #505050;
                color: white;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #606060;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
            QPushButton:checked {
                background-color: #707070;
            }
        """)
        self.controls_bottom_layout.addWidget(self.pB_play_pause)

        # Кнопка перемотки вперед на 5 секунд
        self.pB_forward_5s = QPushButton(self.video_control_container)
        self.pB_forward_5s.setObjectName(u"pB_forward_5s")
        self.pB_forward_5s.setFixedSize(40, 30)
        self.pB_forward_5s.setStyleSheet("""
            QPushButton {
                background-color: #505050;
                color: white;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #606060;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
        """)
        self.controls_bottom_layout.addWidget(self.pB_forward_5s)

        # Кнопка перемотки вперед на 10 секунд
        self.pB_forward_10s = QPushButton(self.video_control_container)
        self.pB_forward_10s.setObjectName(u"pB_forward_10s")
        self.pB_forward_10s.setFixedSize(40, 30)
        self.pB_forward_10s.setStyleSheet("""
            QPushButton {
                background-color: #505050;
                color: white;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #606060;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
        """)
        self.controls_bottom_layout.addWidget(self.pB_forward_10s)

        # Еще один растягивающийся элемент для симметрии
        self.controls_bottom_layout.addStretch(1)

        # Метка времени (справа от кнопок)
        self.lbl_video_time = QLabel(self.video_control_container)
        self.lbl_video_time.setObjectName(u"lbl_video_time")
        self.lbl_video_time.setFixedSize(120, 30)
        self.lbl_video_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_video_time.setStyleSheet(
            "color: white; font-weight: bold; background-color: rgba(80, 80, 80, 150); border-radius: 3px;")
        self.controls_bottom_layout.addWidget(self.lbl_video_time)

        # Добавляем нижний layout к основному
        self.video_control_layout.addLayout(self.controls_bottom_layout)

        # ========================= СИСТЕМНОЕ ===========================

        # Перевод интерфейса
        self.retranslateUi(Form)

        # Соединение слотов и сигналов
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        """Настройка текстовых значений всех элементов интерфейса"""
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.l_video.setText(
            QCoreApplication.translate("Form", u"\u0418\u043d\u0438\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446"
                                               u"\u0438\u044f "
                                               u"\u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f",
                                       None))
        self.pB_DataBase.setText(QCoreApplication.translate("Form", u"DB", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u0424\u0438\u043b\u044c\u0442\u0440\u044b", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u042f\u0440\u043a\u043e\u0441\u0442\u044c", None))
        self.label_4.setText(
            QCoreApplication.translate("Form", u"\u041a\u043e\u043d\u0442\u0440\u0430\u0441\u0442\u043d\u043e\u0441"
                                               u"\u0442\u044c", None))
        self.label_5.setText(
            QCoreApplication.translate("Form", u"\u0420\u0435\u0437\u043a\u043e\u0441\u0442\u044c", None))

        self.label_6.setText(
            QCoreApplication.translate("Form", u"\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b "
                                               u"\u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0438 "
                                               u"\u0432\u0438\u0434\u0435\u043e\u043f\u043e\u0442\u043e\u043a\u0430",
                                       None))
        self.label_7.setText(
            QCoreApplication.translate("Form", u"\u0420\u0430\u0437\u0440\u0435\u0448\u0435\u043d\u0438\u0435\n\u0432"
                                               u"\u0438\u0434\u0435\u043e", None))
        self.label_8.setText(QCoreApplication.translate("Form", u":", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"FPS vid", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"FPS code avg", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"Face", None))
        self.l_video.setText(
            QCoreApplication.translate("Form", u"\u041e\u0436\u0438\u0434\u0430\u043d\u0438\u0435 "
                                               u"\u0432\u0438\u0434\u0435\u043e\u043f\u043e\u0442\u043e\u043a\u0430",
                                       None))
        self.pB_clFil.setText(QCoreApplication.translate("Form", u"\u0421\u0431\u0440\u043e\u0441", None))
        self.pB_translationCam.setText(
            QCoreApplication.translate("Form", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435\n"
                                               u"\u043a \u043a\u0430\u043c\u0435\u0440\u0435", None))
        self.pB_openVid.setText(QCoreApplication.translate("Form", u"\u041e\u0442\u043a\u0440\u044b\u0442\u0438\u0435 "
                                                                   u"\u0432\u0438\u0434\u0435\u043e", None))
        self.pB_translationVid.setText(
            QCoreApplication.translate("Form", u"\u041f\u043e\u0442\u043e\u043a\u043e\u0432\u0430\u044f "
                                               u"\u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430\n"
                                               "\u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u043d\u043e\u0433"
                                               "\u043e \u0432\u0438\u0434\u0435\u043e", None))
        self.pB_saveVid.setText(
            QCoreApplication.translate("Form", u"\u0424\u043e\u043d\u043e\u0432\u0430\u044f "
                                               u"\u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430\n\u0437\u0430"
                                               u"\u0433\u0440\u0443\u0436\u0435\u043d\u043d\u043e\u0433\u043e "
                                               u"\u0432\u0438\u0434\u0435\u043e", None))
        self.lbl_processing_status.setText(QCoreApplication.translate("Form", u"", None))
