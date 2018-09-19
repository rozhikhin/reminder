"""
Модуль с классом MainWindow
"""

import MainForm, settings, help, about
import threading
import os
import sys
import SQLiteAPI
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QSystemTrayIcon, QStyle, QMessageBox
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
        # Переменая pid_file указывает путь к файлу, который создается приложением при первом запуске
        # При запуске приложение проверяет наличие данного файла и, если он существует, то второй экземпляр
        # приложения не запускается
        self.pid_file = os.path.join(os.getcwd(), "reminder.pid")
        # Инициализация переменной interval - количество секунд, в течении который показывается окно напоминалки
        self.interval = 0
        # Инициализация переменной time_repeat_show_reminder - количество секунд, в течении которых окно скрыто
        self.time_repeat_show_reminder = 0
        # Инициализация переменной time_repeat_show_reminder - время суток, ПОСЛЕ которого окно приложения не показывается
        self.time_dont_show_after = None
        # Инициализация переменной time_start_show_since - время суток, ДО которого окно приложения не показывается
        self.time_start_show_since = None
        # Инициализация переменной t1 - первый таймер
        self.t1 = None
        # Инициализация переменной t2 - второй таймер
        self.t2 = None

        # Консструктор
        QtWidgets.QMainWindow.__init__(self, parent)
        # Инициализация GUI
        self.setupUi(self)
        # Установка фиксированного размера окна
        self.setFixedSize(400, 300)
        # Установка заголовка окна
        self.setWindowTitle("Напоминалка")
        # Установка флагов
        self.setWindowFlags(
            # Показать окно поверх всех окон
            QtCore.Qt.WindowStaysOnTopHint |
            # Показать окно без заголовка и рамок
            QtCore.Qt.FramelessWindowHint
        )

        # Цвет фона главного окна
        self.setStyleSheet("QMainWindow {background: #00356a} ")
        # Цвет фона кнопки счетчика - buttonMinus
        self.buttonMinus.setStyleSheet("QPushButton {background: #3286aa} ")
        # Цвет фона кнопки счетчика - buttonPlus
        self.buttonPlus.setStyleSheet("QPushButton {background: #3286aa} ")
        # Цвет текста надписи - счетчика
        self.labelCounter.setStyleSheet("QLabel {color: #91bbd1} ")
        # Экземпляр класса DB() из модуля SQLiteAPI для доступа к БД
        self.sql_api = SQLiteAPI.DB()
        # Получить настройки из базы и применить их к главному окну приложения
        # или создать базу, заполнить ее значениями по-умолчанию и затем применить настройки по-умолчанию
        self.sql_api.init_db()
        # Экземпляр класса SettingsWindow из модуля settings
        self.window_settings = None
        # Привязка метода increase_counter к событию click кнопки buttonPlus.
        # Метод увеличивает значение счетчика
        self.buttonPlus.clicked.connect(self.increase_counter)
        # Привязка метода decrease_counter к событию click кнопки buttonMinus.
        # Метод уменьшает значение счетчика
        self.buttonMinus.clicked.connect(self.decrease_counter)
        # Получить из базы и применить настройки шрифта и цвет текста
        self.set_font_and_color()
        # Получить из базы и применить общие настройки
        self.set_settings()
        # Созать иконку с меню в системном трее
        self.create_tray_icon()
        # Функция проверяет, не запущен ли уже экземпляр приложения путем проверки наличия файла по пути
        # указанному в переменной класса pid_file. Если файл существует - это означает, что уже запущен один экземпляр
        # приложения и осуществляется завершение работы второго экземпляра
        self.exit_app_if_running(self.pid_file)
        # Иконка приложения
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_BrowserReload))

    def contextMenuEvent(self, event):
        """
        Функции contextMenuEvent(event) для создания контекстного меню главного окна
        :param event:
        :return: None
        """
        cmenu = QMenu(self)
        # При нажатии на кнопку "Скрыть окно" - скрыть главное окно приложения
        cmenu.addAction("Скрыть окно", self.hide_main_window)
        # При нажатии на кнопку Настройки - открыть окно настроек
        cmenu.addAction("Настройки", self.show_settings_window)
        # При нажатии на кнопку Справка - показать справку
        cmenu.addAction("Справка", self.show_help)
        # При нажатии на кнопку О программе - показать окно "О программе"
        cmenu.addAction("О программе", self.show_about)
        # При нажатии на кнопку Выход - закрыть главное окно приложения
        cmenu.addAction("Выход", self.close_main_window)
        cmenu.exec_(self.mapToGlobal(event.pos()))



    def not_show_window_from_to(self):
        """
        Функция not_show_window_from_to() проверяет, не находится ли текущее время суток в диапазоне времени,
        определяемом параметрами
        time_dont_show_after - время, после кторого не показывать окно
        time_start_show_since - время, до которого не показывать окно (или с которого начинать показывать)
        :return: None
        """
        # Текущее время
        curtime = QtCore.QTime.currentTime()
        # Если время начала запрета показа окна меньше времени окончания запрета (например, не показывать с 01:00 по 09:00)
        if QtCore.QTime.fromString(self.time_dont_show_after) < QtCore.QTime.fromString(self.time_start_show_since):
            if curtime > QtCore.QTime.fromString(self.time_dont_show_after) and curtime < QtCore.QTime.fromString(self.time_start_show_since):
                self.hide()
        # Если время начала запрета показа окна больше времени окончания запрета (например, не показывать с 23:00 по 09:00)
        else:
            if curtime > QtCore.QTime.fromString(self.time_dont_show_after) and curtime > QtCore.QTime.fromString(self.time_start_show_since):
                self.hide()

    # Получить настройки из базы и применить их к соответсвующим компонентам
    # сделать свойством класса, чтобы можно было получить доступ из другого окна
    def set_settings(self):
        """
        Функция set_settings() получает общие настройки для оформления главного окна программы из базы данных
        и применяет их.
        message - основное сообщение, которое выводится в окне
        interval - переменная класса (чтобы быть доступной другим методам класса) - время, в течении которого показывать
            окно
        counter - значение счетчика
        time_dont_show_after - переменная класса - время суток, после кторого не показывать окно
        time_start_show_since -  переменная класса - время суток, до кторого не показывать окно
            (или с которого начинать показывать)
        time_repeat_show_reminder - переменная класса - время в секундах (в форме настроек задается в минутах),
            через которое повторять показ окна
        :return: None
        """
        message, self.interval, counter, self.time_dont_show_after, self.time_start_show_since, self.time_repeat_show_reminder = self.sql_api.get_settings()
        # Вызов функции, которая разивает сообщение на строки и применяет к каждой строке стиль
        self.add_text_to_text_edit(self.messageTextEdit, message)
        # Если счетчик меньше нуля, то применить соответствующий стиль
        if counter < 0:
            self.labelCounter.setStyleSheet(" QLabel {color: red }")
        # Вывести значение счетчика на форме
        self.labelCounter.setText(str(counter))
        # Отключить TextEdit главной формы, чтобы не было возможности редактировать, минуя форму настроек
        self.messageTextEdit.setDisabled(True)

    def set_font_and_color(self):
        """
        Функция set_font_and_color() получает настройки шрифта и цвет текста для оформления главного окна программы
        из базы данных и применяет их
        size - размер шрифта
        family - семейство шрифта,
        bold - boolean - вес (жирность) шрифта
        italic - boolean - курсив
        italic - boolean - курсив
        strikeout - boolean - перечеркнутый
        color - цвет текста
        На MACOS доступна только кнопка выбора цвета шрифта
        """
        size, family, bold, italic, strikeout, color = self.sql_api.get_font_and_color_text()
        # Применяем получанные настройки к тексту. Функция set_font_to_text_edit определена в классе RBase
        # модуля RBase. Класс RBase наследуется данным классом
        self.set_font_to_text_edit(self.messageTextEdit, size, family, bold, italic, strikeout, color)
        # Применяем стиль к TextEdit - меняем фон и убираем границы
        self.messageTextEdit.setStyleSheet("QTextEdit {background: #00356a; border: 0 }")

    def show_settings_window(self):
        """
        Функция show_settings_window() показывает окно настроек, останавливает таймер и передает окну настроек
        ссылку на главное окно
        """
        # Скрываем главное окно
        self.hide()
        # Переменной window_settings назначаем ссылку на объект класса SettingsWindow
        self.window_settings = settings.SettingsWindow()
        # Останавливаем таймер, запущенный в данный момент. По таймерам срабатывают функции скрытия
        # и показа главнонго окна
        self.stop_timers()
        # Переменной класса window_settings - parent - устанавливаем ссылку на главное окно для последующего доступа
        # из окна настроек к методам и атрибутам главного окна
        self.window_settings.parent = self
        # Показываем окно настроек
        self.window_settings.show()

    def stop_timers(self):
        """
        Функция stop_timers() останавливает таймер, запущенный в момент ее вызова
        :return: None
        """
        if self.t1:
            self.t1.cancel()
        if self.t2:
            self.t2.cancel()

    def close_main_window(self):
        """
        Функция closeMainWindow() останавливает таймеры и закрывает главное окно
        :return: None
        """
        self.stop_timers()
        self.close()

    def hide_main_window(self):
        """
        Функция hide_main_window() скрывает по таймеру главное окно через time_repeat_show_reminder секунд
        :return: None
        """
        # Проверяем, не скрыто ли окно в данный момент. Если скрыто, то выходим из функции, ничего не выполняя
        if self.isHidden():
            return
        # Если окно не скрыто, скрываем его
        self.hide()
        # Создаем таймер, который покажет окно через time_repeat_show_reminder секунд
        self.t1 = threading.Timer(self.time_repeat_show_reminder, self.show_main_window)
        # И запускаем таймер
        self.t1.start()
        # Останавливаем таймер, срабатывающий для сокрытия окна
        if self.t2:
            self.t2.cancel()

    def show_main_window(self):
        """
        Функция show_main_window() показывает по таймеру главное окно через interval секунд
        :return: None
        """
        # Проверяем, не показано ли окно в данный момент. Если показано, то выходим из функции, ничего не выполняя
        if self.isVisible():
            return
        # Если окно не показано, плказываем его
        self.show()
        # Создаем таймер, который скроет окно через interval секунд
        self.t2 = threading.Timer(self.interval, self.hide_main_window)
        # И запускаем таймер
        self.t2.start()
        # Останавливаем таймер, срабатывающий для показа окна
        if self.t1:
            self.t1.cancel()
        self.not_show_window_from_to()

    def show_help(self):
        """
        Функция show_help показывает окно со справкой по программе
        :return:
        """
        if self.isHidden():
            self.show()
        self.help_window = help.HelpWindow()
        # Останавливаем таймер, запущенный в данный момент. По таймерам срабатывают функции скрытия
        # и показа главнонго окна
        self.stop_timers()
        # Переменной класса help_window - parent - устанавливаем ссылку на главное окно для последующего доступа
        # из окна настроек к методам и атрибутам главного окна
        self.help_window.parent = self
        # Показываем окно

        self.help_window.show()

    def show_about(self):
        """
        Функция show_help показывает окно со справкой по программе
        :return:
        """
        if self.isHidden():
            self.show()
        self.about_window = about.AboutWindow()
        # Останавливаем таймер, запущенный в данный момент. По таймерам срабатывают функции скрытия
        # и показа главнонго окна
        self.stop_timers()
        # Переменной класса help_window - parent - устанавливаем ссылку на главное окно для последующего доступа
        # из окна настроек к методам и атрибутам главного окна
        self.about_window.parent = self
        # Показываем окно

        self.about_window.show()

    def increase_counter(self):
        """
        Функция increase_counter() увеличивает значение счетчика, отображает новое значение на форме
        и сохраняет его в базе данных
        """
        # Получаем текущее значения счетчика, отображенное на форме
        counter = int(self.labelCounter.text())
        # Увеличиваем его на 1
        counter += 1
        # Если счетчик больше нуля, устанавливаем соответсвующий стиль
        if counter >= 0:
            self.labelCounter.setStyleSheet(" QLabel {color: #91bbd1 }")
        # Отображваем обновленное значение счетчика на форме
        self.labelCounter.setText(str(counter))
        # Сохраняем новое значение счетчика в базе
        self.sql_api.change_counter(counter)

    def decrease_counter(self):
        """
        Функция decrease_counter() уменьшает значение счетчика, отображает новое значение на форме
        и сохраняет его в базе данных
        """
        # Получаем текущее значения счетчика, отображенное на форме
        counter = int(self.labelCounter.text())
        # Уменьшаем его на 1
        counter -= 1
        # Если счетчик меньше нуля, устанавливаем соответсвующий стиль
        if counter < 0:
            self.labelCounter.setStyleSheet(" QLabel {color: red }")
        # Отображваем обновленное значение счетчика на форме
        self.labelCounter.setText(str(counter))
        # Сохраняем новое значение счетчика в базе
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
        """
        Функция closeEvent() - событие закрытия окна - проверяет, существует ли по указанному пути файл - pid_file,
         и, если существует, то удаляет его.
        :param event:
        :return:
        """
        if os.path.exists(self.pid_file):
            if os.path.isfile(self.pid_file):
                os.unlink(self.pid_file)

    def exit_app_if_running(self, pid_file):
        """
        Функция exit_app_if_running(pid_file) - обеспечивает запуск только одного экземпляра программы.
        При запуске самый первый экземпляр создает файл - pid_file. Также при запуске программа проверяет
        наличие данного файла. Если данный файл обнаружен, то данный экземпляр завершает работу.
        :param pid_file: str - путь к файлу
        :return: None
        """
        # pid_file - путь к файлу
        self.pid_file = os.path.join(os.getcwd(), "reminder.pid")
        # Если файл существует, завершить экземпляр приложения
        if os.path.exists(self.pid_file):
            if os.path.isfile(self.pid_file):
                sys.exit()
        # Если файл не существует, т.е. это первый экземпляр приложения, то созать фал pid_file
        f = open(self.pid_file, 'tw', encoding='utf-8')
        f.close()

    def create_tray_icon(self):
        """
        Функция tray_icon создает иконку приложения в системном трее с собственным контектсным меню
        :return: None
        """
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        # Создание пунктов меню
        show_action = QAction("Показать окно", self)
        hide_action = QAction("Скрыть окно", self)
        setting_action = QAction("Настройки", self)
        help_action = QAction("Справка", self)
        about_action = QAction("О программе", self)
        quit_action = QAction("Выход", self)
        # Подключение обработчиков нажатия на кнопки меню
        show_action.triggered.connect(self.show_main_window)
        hide_action.triggered.connect(self.hide_main_window)
        help_action.triggered.connect(self.show_help)
        setting_action.triggered.connect(self.show_settings_window)
        about_action.triggered.connect(self.show_about)
        quit_action.triggered.connect(self.close_main_window)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(help_action)
        tray_menu.addAction(about_action)
        tray_menu.addAction(setting_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    # Чтобы исключить мелькание, нужно изначально сместить окно за рамки экрана
    mainWindow.move(mainWindow.width() * -3, 0)
    # Показывать окно приложения только в определнное время суток
    mainWindow.not_show_window_from_to()
    # Показать главное окно
    mainWindow.show_main_window()
    # Разместить окно в правом нижнем углу
    mainWindow.move_to_right_bottom_corner()
    sys.exit(app.exec_())


