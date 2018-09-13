"""
Модуль с классом MainWindow
"""

import MainForm, settings
import threading
import os
import time
import sys
import SQLiteAPI
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMenu, QAction
from RBase import RBase

class MainWindow(QtWidgets.QMainWindow, MainForm.Ui_mainForm, RBase):
    """
    Класс MainWindow содержит функции для взаимодействия с главным окном программы
    """
    def __init__(self, parent=None):
        """
        Конструктор - инициализирует UI, назначает обработчики для кнопок,
        вызывает функции для настройки интерфейса
        :param parent: default: None
        """

        self.pid_file = os.path.join(os.getcwd(), "reminder.pid")
        self.exit_app_if_running(self.pid_file)
        self.interval = 0
        self.time_repeat_show_reminder = 0

        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setFixedSize(400, 300)
        self.setWindowTitle("Напоминалка")
        self.setWindowFlags(
            # Показать окно поверх всех окон
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint
        )

        self.setStyleSheet("QMainWindow {background: #00356a} ")
        self.buttonMinus.setStyleSheet("QPushButton {background: #3286aa} ")
        self.buttonPlus.setStyleSheet("QPushButton {background: #3286aa} ")
        self.labelCounter.setStyleSheet("QLabel {color: #91bbd1} ")
        # Экземпляр класса DB() из модуля SQLiteAPI
        self.sql_api = SQLiteAPI.DB()
        # Получить настройки из базы и применить их к главному окну приложения
        # или создать базу, заполнить ее значениями по-умолчанию и затем применить настройки по-умолчанию
        self.sql_api.init_db()
        # Экземпляр класса SettingsWindow из модуля settings
        self.window_settings = None
        # Увеличить счетчик
        self.buttonPlus.clicked.connect(self.increase_counter)
        # Уменьшить счетчик
        self.buttonMinus.clicked.connect(self.decrease_counter)
        # Получить из базы и применить настройки шрифта и цвет текста
        self.set_font_and_color()
        # Получить из базы и применить общие настройки
        self.set_settings()

        self.set_hot_key()

    def contextMenuEvent(self, event):
        """
        Функции contextMenuEvent(event) для создания контекстного меню
        :param event:
        :return: None
        """
        cmenu = QMenu(self)
        # При нажатии на кнопку "Скрыть окно" - скрыть главное окно приложения
        cmenu.addAction("Скрыть окно", self.hide_main_window)
        # При нажатии на кнопку Выход - закрыть главное окно приложения
        cmenu.addAction("Выход", self.close_main_window)
        # При нажатии на кнопку Настройки - открыть окно настроек
        cmenu.addAction("Настройки", self.show_settings_window)
        cmenu.exec_(self.mapToGlobal(event.pos()))

    # Получить настройки из базы и применить их к соответсвующим компонентам
    # interval сделать свойством класса, чтобы можно было получить доступ из другого окна
    def set_settings(self):
        """
        Функция set_settings() получает общие настройки для оформления главного окна программы из базы данных и применяет их
        """
        message, self.interval, counter, time_dont_show_after, time_start_show_since, self.time_repeat_show_reminder = self.sql_api.get_settings()
        # print(self.sql_api.get_settings())
        # return

        self.add_text_to_text_edit(self.messageTextEdit, message)
        if counter < 0:
            self.labelCounter.setStyleSheet(" QLabel {color: red }")
        self.labelCounter.setText(str(counter))
        self.start_timer()
        self.messageTextEdit.setDisabled(True)

    def set_font_and_color(self):
        """
        Функция set_font_and_color() получает настройки шрифта и цвет текста для оформления главного окна программы
        из базы данных и применяет их
        """
        size, family, bold, italic, strikeout, color = self.sql_api.get_font_and_color_text()
        self.set_font_to_text_edit(self.messageTextEdit, size, family, bold, italic, strikeout, color)
        # self.messageTextEdit.setStyleSheet("QTextEdit {color: " + color + "; background: #00356a; border: 0 }")
        self.messageTextEdit.setStyleSheet("QTextEdit {background: #00356a; border: 0 }")

    def start_timer(self):
        """
        Функция создает и запускает таймер, который отсчитывает время показа главного окна
        :param interval: integer - время показа главного окна программы
        :param time_repeat_show_reminder
        :param function: - функция - вызывается по завершении интервала, т.е. срабатывания таймера
        """
        if self.isVisible():
            self.hide_main_window()
        else:
            self.show_main_window()
        self.t = threading.Timer(self.interval, self.start_timer)
        self.t.start()

    def show_settings_window(self):
        """
        Функция show_settings_window() показывает окно настроек, останавливает таймер и передает окну настроек ссылку на главное окно
        """
        self.hide()
        self.window_settings = settings.SettingsWindow()
        self.t.cancel()
        self.window_settings.parent = self
        self.window_settings.show()

    def close_main_window(self):
        """ Функция closeMainWindow() останавливает таймер и закрывает главное окно"""
        self.t.cancel()
        self.close()

    def hide_main_window(self):
        self.hide()
        time.sleep(self.time_repeat_show_reminder)
    #

    def show_main_window(self):
        self.show()

    def set_hot_key(self):
        self.quitAct = QAction(self.tr("&Quit"), self)
        self.quitAct.setShortcut(self.tr("Ctrl+Q"))
        self.quitAct.setStatusTip(self.tr("Quit the application"))
        self.quitAct.triggered.connect(self.hide_main_window)

        self.addAction(self.quitAct)


    def increase_counter(self):
        """
        Функция increase_counter() увеличивает значение счетчика, отображает новое значение на форме
        и сохраняет его в базе данных
        """
        counter = int(self.labelCounter.text())
        counter += 1
        if counter >= 0:
            self.labelCounter.setStyleSheet(" QLabel {color: #91bbd1 }")
        self.labelCounter.setText(str(counter))
        self.sql_api.change_counter(counter)

    def decrease_counter(self):
        """
        Функция decrease_counter() уменьшает значение счетчика, отображает новое значение на форме
        и сохраняет его в базе данных
        """
        counter = int(self.labelCounter.text())
        counter -= 1
        if counter < 0:
            self.labelCounter.setStyleSheet(" QLabel {color: red }")
        self.labelCounter.setText(str(counter))
        self.sql_api.change_counter(counter)

    #
    def move_to_right_bottom_corner(self):
        """
        Функция помещает окно в правый нижний угол экрана. Чтобы точно разместить окно в правом нижнем углу,
        сначала отображается окно, потом сдвигается.
        """
        screen_geometry = QApplication.desktop().availableGeometry()
        screen_size = (screen_geometry.width(), screen_geometry.height())
        win_size = (self.frameSize().width(), self.frameSize().height())
        x = screen_size[0] - win_size[0]
        y = screen_size[1] - win_size[1]
        self.move(x, y)

    def closeEvent(self, event):
        if os.path.exists(self.pid_file):
            if os.path.isfile(self.pid_file):
                os.unlink(self.pid_file)

    def exit_app_if_running(self, pid_file):
        self.pid_file = os.path.join(os.getcwd(), "reminder.pid")
        if os.path.exists(self.pid_file):
            if os.path.isfile(self.pid_file):
                sys.exit()
        f = open(self.pid_file, 'tw', encoding='utf-8')
        f.close()

if __name__ == "__main__":

    app = QApplication(sys.argv)




    mainWindow = MainWindow()

    # pid_file = os.path.join(os.getcwd(), "reminder.pid")
    # if os.path.exists(pid_file):
    #     if os.path.isfile(pid_file):
    #         mainWindow.t.cancel()
    #         sys.exit()
    # f = open(pid_file, 'tw', encoding='utf-8')
    # f.close()


    # Чтобы исключить мелькание, нужно изначально сместить окно за рамки экрана
    mainWindow.move(mainWindow.width() * -3, 0)
    mainWindow.show()

    # Разместить окно в правом нижнем углу
    mainWindow.move_to_right_bottom_corner()
    sys.exit(app.exec_())


