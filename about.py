import AboutForm
import threading
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget

class AboutWindow(QWidget, AboutForm.Ui_AboutForm):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle("О программе")
        self.labelProgramName.setText("Напоминалка - Версия 2.0")
        self.labelAuthor.setText("Автор - Рожихин Александр")
        self.labelAuthorEmail.setText('<a href="mailto: rozhihin@mail.ru"><span style=" text-decoration: underline; color:#0000ff;">rozhihin@mail.ru</span></a>')

    def closeEvent(self, event):
        self.parent.t2 = threading.Timer(self.parent.interval, self.parent.hide_main_window)
        self.parent.t2.start()
