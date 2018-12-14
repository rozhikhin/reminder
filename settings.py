"""
Модуль окна настроек
"""
import SettingForm, SQLiteAPI, platform
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QFontDialog, QColorDialog
from RBase import RBase


class SettingsWindow(QtWidgets.QWidget, SettingForm.Ui_settingsForm, RBase):
    """
    Класс SettingsWindow содержит функции для взаимодействия с окном настроек программы
    """
    def __init__(self, parent=None):
        """
        Конструктор - инициализирует UI, назначает обработчики для кнопок,
        вызывает функции для настройки интерфейса
        :param parent: default: None
        """
        QtWidgets.QWidget.__init__(self, parent=None)
        self.setupUi(self)
        self.setFixedSize(500, 500)
        if platform.system() == "Darwin":
            self.buttonFont.setDisabled(True)
            self.buttonFont.setVisible(False)
        self.buttonFont.clicked.connect(self.change_font)
        self.buttonColorText.clicked.connect(self.change_text_color)
        self.buttonSaveSettings.clicked.connect(self.save_settings)
        self.buttonCancel.clicked.connect(self.close_setting_window)
        self.clearCounterButton.clicked.connect(self.clear_counter)
        self.resetTodefaultButton.clicked.connect(self.reset_to_default)
        self.setStyleSheet("QPushButton{font-size: 12px}")
        self.sql_api = SQLiteAPI.DB()
        self.changed_settings = {}
        self.changed_font_and_color = {}
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
        )
        self.set_font_and_color()
        self.set_settings()
        self.messageTextEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.messageTextEdit.textChanged.connect(self.text_changed)

    def text_changed(self):
        self.messageTextEdit.setTextColor(QColor(self.changed_font_and_color["text_color"] ))

    def close_setting_window(self):
        """
        Функция close_setting_window()
        """
        self.close()
        self.parent.show_main_window()

    def set_settings(self):
        """
        Функция set_settings() получает настройки из базы и применяет их к соответсвующим компонентам
        """
        message, interval, counter, time_dont_show_after, time_start_show_since, time_repeat_show_reminder = self.sql_api.get_settings()
        self.add_text_to_text_edit(self.messageTextEdit, message)
        self.lineEditTimeCountShowMsg.setText(str(interval))
        self.lineEditTimeRepeat.setText(str(int(time_repeat_show_reminder / 60)))
        self.timeEditStartShowSince.setTime(QtCore.QTime.fromString(time_start_show_since))
        self.timeEditDontShowAfter.setTime(QtCore.QTime.fromString(time_dont_show_after))

    def set_font_and_color(self):
        """
        Функция set_font_and_color() получает настройки шрифта и цвет текста из базы и применяет их к компоненту TextEdit
        """
        size, family, bold, italic, strikeout, color = self.sql_api.get_font_and_color_text()
        self.set_font_to_text_edit(self.messageTextEdit, size, family, bold, italic, strikeout, color)
        self.changed_font_and_color["text_color"] = color

    def change_font(self):
        """
        Функция change_font() получает шрифт текста с помощью диалогового окна QFontDialog и применяет их к тексту
        """
        self.deselect_text(self.messageTextEdit)
        # font, ok = QFontDialog.getFont(QFont("Tahoma", 16), parent=self, caption="Выбор шрифта", options=QFontDialog.DontUseNativeDialog)
        font, ok = QFontDialog.getFont(self.messageTextEdit.font(), parent=self, caption="Выбор шрифта", options=QFontDialog.DontUseNativeDialog)
        if ok:
            text = self.messageTextEdit.toPlainText()
            pointSize = font.pointSizeF()
            self.messageTextEdit.setFontPointSize(pointSize)
            family = font.family()
            self.messageTextEdit.setFontFamily(family)
            bold = font.bold()
            italic = font.italic()
            underline = font.underline()
            strikeOut = font.strikeOut()

            if italic:
                self.messageTextEdit.setFontItalic(True)
            else:
                self.messageTextEdit.setFontItalic(False)

            if bold:
                self.messageTextEdit.setFontWeight(600)
            else:
                self.messageTextEdit.setFontWeight(0)

            if underline:
                self.messageTextEdit.setFontUnderline(True)
            else:
                self.messageTextEdit.setFontUnderline(False)

            font = self.messageTextEdit.font()
            if strikeOut:
                font.setStrikeOut(True)
            else:
                font.setStrikeOut(False)
            self.messageTextEdit.setFont(font)
            self.add_text_to_text_edit(self.messageTextEdit, text)

    def change_text_color(self):
        """
        Функция change_text_color() получает цвет текста с помощью диалогового окна QColorDialog и применяет его к тексту
        """
        # Если выделить текст и затем устанавливать цвет, то вылетает с ошибкой.
        # Для этого сначала снимаем выделение с текста
        self.deselect_text(self.messageTextEdit)
        # text_color = QColorDialog.getColor()
        text_color = QColorDialog.getColor(self.messageTextEdit.textColor())
        if text_color.isValid():
            text = self.messageTextEdit.toPlainText()
            self.messageTextEdit.setTextColor(text_color)
            self.changed_font_and_color["text_color"] = text_color.name()
            self.add_text_to_text_edit(self.messageTextEdit, text)

    def save_settings(self):
        """
        Функция save_settings() сохраняет настройки в базе данных
        """
        font = self.messageTextEdit.currentFont()
        self.changed_font_and_color["font_size"] = font.pointSize()
        self.changed_font_and_color["font_family"] = font.family()
        self.changed_font_and_color["font_italic"] = int(font.italic())
        self.changed_font_and_color["font_bold"] = int(font.bold())
        self.changed_font_and_color["font_underline"] = int(font.underline())
        self.changed_font_and_color["font_strikeout"] = int(font.strikeOut())
        self.changed_font_and_color["text_color"] = self.messageTextEdit.textColor().name()

        self.changed_settings["main_text"] = self.messageTextEdit.toPlainText()
        self.changed_settings["time_out"] = self.lineEditTimeCountShowMsg.text()
        self.changed_settings["time_dont_show_after"] = self.timeEditDontShowAfter.time().toString("hh:mm")
        self.changed_settings["time_start_show_since"] = self.timeEditStartShowSince.time().toString("hh:mm")
        self.changed_settings["time_repeat_show_reminder"] = int(self.lineEditTimeRepeat.text()) * 60

        self.sql_api.save_settings(self.changed_settings, self.changed_font_and_color)
        self.parent.set_font_and_color()
        self.parent.set_settings()
        self.close()
        self.close_setting_window()

    def clear_counter(self):
        """
        Функция clear_counter() обнуляет счетчик, сохраняет в базе данных новое значение и выводит его в главном окне
        """
        counter = 0
        self.sql_api.change_counter(counter)
        self.parent.labelCounter.setText(str(counter))
        self.parent.labelCounter.setStyleSheet(" QLabel {color: #91bbd1 }")
        self.close_setting_window()

    def reset_to_default(self):
        """
        Функция reset_to_default() изменяет все настройки к первоначальным
        """
        self.sql_api.reset_to_default_settings()
        self.parent.set_font_and_color()
        self.parent.set_settings()
        self.set_font_and_color()
        self.set_settings()
        self.parent.labelCounter.setStyleSheet(" QLabel {color: #91bbd1 }")
        self.close_setting_window()



