# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_CreatNPYGnDROW.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
                               QRadioButton, QSizePolicy, QVBoxLayout, QWidget, QHBoxLayout,
                               QFrame, QSpacerItem)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(250, 350)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QSize(250, 350))
        Form.setMinimumSize(QSize(250, 350))


        rB_stule = u"""
            QRadioButton {
                font-size: 11px;
                padding: 5px;
                color: #cccccc;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
        """

        # Основной вертикальный layout
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(10)

        # Заголовок
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setStyleSheet(u"color: #cccccc; margin: 5px;")
        self.verticalLayout.addWidget(self.label_2)

        # Разделительная линия
        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setStyleSheet(u"border: 1px solid #cccccc;")
        self.verticalLayout.addWidget(self.line)

        # Группа радиокнопок
        self.radio_group_layout = QVBoxLayout()
        self.radio_group_layout.setObjectName(u"radio_group_layout")
        self.radio_group_layout.setSpacing(15)

        # Радиокнопка "Только из папки"
        self.rB_onlyFolder = QRadioButton(Form)
        self.rB_onlyFolder.setObjectName(u"rB_onlyFolder")
        self.rB_onlyFolder.setStyleSheet(rB_stule)
        self.radio_group_layout.addWidget(self.rB_onlyFolder)

        # Радиокнопка "Только по камере"
        self.rB_onlyCam = QRadioButton(Form)
        self.rB_onlyCam.setObjectName(u"rB_onlyCam")
        self.rB_onlyCam.setStyleSheet(rB_stule)
        self.radio_group_layout.addWidget(self.rB_onlyCam)

        # Радиокнопка "Комбинированно"
        self.rB_mergeCombo = QRadioButton(Form)
        self.rB_mergeCombo.setObjectName(u"rB_mergeCombo")
        self.rB_mergeCombo.setStyleSheet(rB_stule)
        self.radio_group_layout.addWidget(self.rB_mergeCombo)

        self.verticalLayout.addLayout(self.radio_group_layout)

        # Разделительная линия
        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_2.setStyleSheet(u"border: 1px solid #cccccc;")
        self.verticalLayout.addWidget(self.line_2)

        # Кнопка генерации
        self.pB_genFaceDB = QPushButton(Form)
        self.pB_genFaceDB.setObjectName(u"pB_genFaceDB")
        self.pB_genFaceDB.setMinimumSize(QSize(0, 40))
        self.pB_genFaceDB.setStyleSheet(u"""
            QPushButton {
                background-color: #505050;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #606060;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
            QPushButton:disabled {
                background-color: #aaaaaa;
                color: #888888;
            }
        """)
        self.verticalLayout.addWidget(self.pB_genFaceDB)

        # Поле ввода имени базы данных
        self.lE_nameDB = QLineEdit(Form)
        self.lE_nameDB.setObjectName(u"lE_nameDB")
        self.lE_nameDB.setMinimumSize(QSize(0, 35))
        self.lE_nameDB.setPlaceholderText("Имя базы данных")
        self.lE_nameDB.setStyleSheet(u"""
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 11px;
                background-color: white;
                text-align: center;  # ДОБАВЬТЕ ЭТУ СТРОКУ
            }
            QLineEdit:focus {
                border: 2px solid #05B8CC;
            }
        """)
        self.lE_nameDB.setAlignment(Qt.AlignmentFlag.AlignCenter)  # ДОБАВЬТЕ ЭТУ СТРОКУ
        self.verticalLayout.addWidget(self.lE_nameDB)

        # Кнопка объединения БД
        self.pB_mergeDB = QPushButton(Form)
        self.pB_mergeDB.setObjectName(u"pB_mergeDB")
        self.pB_mergeDB.setMinimumSize(QSize(0, 40))
        self.pB_mergeDB.setStyleSheet(u"""
            QPushButton {
                background-color: #505050;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #606060;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
            QPushButton:disabled {
                background-color: #aaaaaa;
                color: #888888;
            }
        """)
        self.verticalLayout.addWidget(self.pB_mergeDB)

        # Растягивающийся элемент для правильного размещения
        self.verticalLayout.addStretch(1)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Создание базы данных лиц", None))
        self.label_2.setText(
            QCoreApplication.translate("Form", u"\u0421\u043e\u0437\u0434\u0430\u043d\u0438\u0435 "
                                               u"\u0431\u0430\u0437\u044b\n\u0434\u0430\u043d\u043d\u044b\u0445 "
                                               u"\u043b\u0438\u0446", None))
        self.rB_onlyFolder.setText(
            QCoreApplication.translate("Form", u"\u0422\u043e\u043b\u044c\u043a\u043e \u0438\u0437 "
                                               u"\u043f\u0430\u043f\u043a\u0438", None))
        self.rB_onlyCam.setText(
            QCoreApplication.translate("Form", u"\u0422\u043e\u043b\u044c\u043a\u043e \u043f\u043e "
                                               u"\u043a\u0430\u043c\u0435\u0440\u0435", None))
        self.rB_mergeCombo.setText(
            QCoreApplication.translate("Form", u"\u041a\u043e\u043c\u0431\u0438\u043d\u0438\u0440\u043e\u0432\u0430"
                                               u"\u043d\u043d\u043e", None))
        self.pB_genFaceDB.setText(
            QCoreApplication.translate("Form", u"\u041f\u0440\u043e\u0432\u0435\u0441\u0442\u0438 "
                                               u"\u0433\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u044e", None))
        self.pB_mergeDB.setText(
            QCoreApplication.translate("Form", u"\u041e\u0431\u044a\u0435\u0434\u0435\u043d\u0438\u0442\u044c "
                                               u"\u0411\u0414", None))
        self.lE_nameDB.setPlaceholderText(
            QCoreApplication.translate("Form", u"\u0418\u043c\u044f \u0441\u043e\u0437\u0434\u0430\u0432\u0430\u0435"
                                               u"\u043c\u043e\u0439 \u0411\u0414", None))