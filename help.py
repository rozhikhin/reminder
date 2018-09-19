"""
Модуль с классом HelpWindow
"""
import helpForm
import threading
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget


class HelpWindow(QWidget, helpForm.Ui_Form):
    """
    Класс HelpWindow - создает окно со справкой
    """
    def __init__(self, parent=None):
        """
        Конструктор класса AboutWindow - создает GUI окна "Справка"
        :param parent:
        """
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # Установить заголовок окна
        self.setWindowTitle("Справка")

    def closeEvent(self, event):
        """
        Функция closeEvent(event) запускает таймеры для главного окна программы при закрытии
        окна "Справка"
        :param event:
        :return: None
        """
        self.parent.t2 = threading.Timer(self.parent.interval, self.parent.hide_main_window)
        self.parent.t2.start()

