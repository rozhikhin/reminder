"""
Модуль с классом AboutWindow - сообщает информацию о программе
"""
import AboutForm
import threading
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget

class AboutWindow(QWidget, AboutForm.Ui_AboutForm):
    """
    Класс AboutWindow - сообщает информацию о программе и авторе программы
    """
    def __init__(self, parent=None):
        """
        Конструктор класса AboutWindow - создает GUI окна "О программе"
        :param parent:
        """
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # Установить заголовок окна
        self.setWindowTitle("О программе")
        # Указать наменование программы и версию
        self.labelProgramName.setText("Напоминалка - Версия 2.0")
        # Указать автора
        self.labelAuthor.setText("Автор - Рожихин Александр")
        # Указать E-Mail автора
        self.labelAuthorEmail.setText('<a href="mailto: rozhihin@mail.ru"><span style=" text-decoration: underline; '
                                      'color:#0000ff;">rozhihin@mail.ru</span></a>')

    def closeEvent(self, event):
        """
        Функция closeEvent(event) запускает таймеры для главного окна программы при закрытии
        окна "О Программе"
        :param event:
        :return: None
        """
        self.parent.t2 = threading.Timer(self.parent.interval, self.parent.hide_main_window)
        self.parent.t2.start()
